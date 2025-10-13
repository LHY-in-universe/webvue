"""
任务调度器 - 管理训练任务的并发控制和队列调度
"""

import asyncio
import logging
import traceback
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from database.edgeai import get_db, Project, TaskQueue
from database.edgeai.database import SessionLocal
# 延迟导入以避免循环导入
# from ..api.training import start_training_with_api
from ..config.scheduler_config import get_config
from ..monitoring.task_monitor import task_monitor


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 移除本地配置类，使用全局配置


class TaskScheduler:
    """
    任务调度器 - 单例模式
    负责管理训练任务的排队、调度和执行
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskScheduler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.config = get_config()
            self.running_tasks: Dict[str, Dict[str, Any]] = {}  # 当前运行的任务
            self.scheduler_task: Optional[asyncio.Task] = None
            self.cleanup_task: Optional[asyncio.Task] = None
            self.monitor_task: Optional[asyncio.Task] = None
            self._is_running = False
            TaskScheduler._initialized = True
            logger.info("TaskScheduler initialized with config")

    async def start(self):
        """启动任务调度器"""
        if self._is_running:
            logger.warning("TaskScheduler is already running")
            return

        self._is_running = True
        logger.info("Starting TaskScheduler...")

        # 启动主调度循环
        self.scheduler_task = asyncio.create_task(self._scheduler_loop())

        # 启动清理任务
        self.cleanup_task = asyncio.create_task(self._cleanup_loop())

        # 启动监控
        await task_monitor.start(self.config.METRICS_EXPORT_INTERVAL)

        logger.info("TaskScheduler started successfully")

    async def stop(self):
        """停止任务调度器"""
        if not self._is_running:
            return

        self._is_running = False
        logger.info("Stopping TaskScheduler...")

        # 取消调度任务
        if self.scheduler_task and not self.scheduler_task.done():
            self.scheduler_task.cancel()
            try:
                await self.scheduler_task
            except asyncio.CancelledError:
                pass

        # 取消清理任务
        if self.cleanup_task and not self.cleanup_task.done():
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass

        # 停止监控
        await task_monitor.stop()

        logger.info("TaskScheduler stopped")

    def can_start_new_task(self) -> bool:
        """检查是否可以启动新任务"""
        return len(self.running_tasks) < self.config.MAX_CONCURRENT_TASKS

    def add_task_to_queue(self, project_id: int, priority: int = 5,
                         task_config: Dict[str, Any] = None,
                         db: Session = None) -> TaskQueue:
        """将任务添加到队列"""
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False

        try:
            # 检查项目是否存在
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                raise ValueError(f"Project {project_id} not found")

            # 检查是否已有相同项目的排队或运行中的任务
            existing_task = db.query(TaskQueue).filter(
                and_(
                    TaskQueue.project_id == project_id,
                    TaskQueue.status.in_(['queued', 'running'])
                )
            ).first()

            if existing_task:
                raise ValueError(f"Project {project_id} already has a task in queue or running")

            # 创建新的队列任务
            queue_task = TaskQueue(
                project_id=project_id,
                status='queued',
                priority=priority,
                task_config=task_config or {},
                retry_count=0,
                max_retries=self.config.MAX_RETRY_COUNT
            )

            db.add(queue_task)
            db.commit()
            db.refresh(queue_task)

            logger.info(f"Task added to queue: Project {project_id}, Queue ID {queue_task.id}, Priority {priority}")

            # 记录监控事件
            task_monitor.record_task_event('task_queued', queue_task.id,
                                           project_id=project_id, priority=priority)

            return queue_task

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to add task to queue: {e}")
            raise
        finally:
            if should_close:
                db.close()

    def get_next_task(self, db: Session = None) -> Optional[TaskQueue]:
        """获取下一个要执行的任务 (按优先级和创建时间排序)"""
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False

        try:
            task = db.query(TaskQueue).filter(
                TaskQueue.status == 'queued'
            ).order_by(
                TaskQueue.priority.asc(),  # 优先级升序 (数字小的先执行)
                TaskQueue.created_at.asc()  # 创建时间升序 (先创建的先执行)
            ).first()

            return task
        finally:
            if should_close:
                db.close()

    async def _scheduler_loop(self):
        """主调度循环"""
        logger.info("Scheduler loop started")

        while self._is_running:
            try:
                await self._process_queue()
                await self._check_running_tasks()
                await asyncio.sleep(self.config.QUEUE_CHECK_INTERVAL)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                logger.error(traceback.format_exc())
                await asyncio.sleep(self.config.QUEUE_CHECK_INTERVAL)

    async def _process_queue(self):
        """处理队列中的任务"""
        if not self.can_start_new_task():
            return

        db = SessionLocal()
        try:
            next_task = self.get_next_task(db)
            if next_task:
                await self._start_task(next_task, db)
        finally:
            db.close()

    async def _start_task(self, queue_task: TaskQueue, db: Session):
        """启动任务执行"""
        try:
            # 更新任务状态为运行中
            queue_task.status = 'running'
            queue_task.started_at = datetime.utcnow()
            db.commit()

            # 记录运行中的任务
            self.running_tasks[str(queue_task.id)] = {
                'queue_task_id': queue_task.id,
                'project_id': queue_task.project_id,
                'started_at': datetime.utcnow(),
                'timeout_at': datetime.utcnow() + timedelta(seconds=self.config.TASK_TIMEOUT)
            }

            logger.info(f"Starting task: Queue ID {queue_task.id}, Project ID {queue_task.project_id}")

            # 异步执行训练任务
            task_coroutine = self._execute_training_task(queue_task)
            asyncio.create_task(task_coroutine)

        except Exception as e:
            logger.error(f"Failed to start task {queue_task.id}: {e}")

            # 更新任务状态为失败
            queue_task.status = 'failed'
            queue_task.error_message = str(e)
            queue_task.completed_at = datetime.utcnow()
            db.commit()

            # 从运行中任务移除
            self.running_tasks.pop(str(queue_task.id), None)

    async def _execute_training_task(self, queue_task: TaskQueue):
        """执行训练任务"""
        db = SessionLocal()
        task_id = str(queue_task.id)

        try:
            logger.info(f"Executing training task: Queue ID {queue_task.id}")

            # 调用实际的训练API - 使用延迟导入避免循环导入
            from ..api.training import start_training_with_api
            result = await start_training_with_api(str(queue_task.project_id), db)

            if result.success:
                # 任务成功完成
                queue_task.status = 'completed'
                queue_task.external_task_id = result.task_id if hasattr(result, 'task_id') else None
                queue_task.completed_at = datetime.utcnow()
                logger.info(f"Training task completed successfully: Queue ID {queue_task.id}")

            else:
                # 任务失败，检查是否需要重试
                if queue_task.retry_count < queue_task.max_retries:
                    queue_task.retry_count += 1
                    queue_task.status = 'queued'  # 重新入队
                    queue_task.error_message = getattr(result, 'message', 'Training failed')
                    logger.warning(f"Training task failed, retrying ({queue_task.retry_count}/{queue_task.max_retries}): Queue ID {queue_task.id}")
                else:
                    queue_task.status = 'failed'
                    queue_task.error_message = getattr(result, 'message', 'Training failed - max retries exceeded')
                    queue_task.completed_at = datetime.utcnow()
                    logger.error(f"Training task failed permanently: Queue ID {queue_task.id}")

        except Exception as e:
            logger.error(f"Exception in training task {queue_task.id}: {e}")
            logger.error(traceback.format_exc())

            # 处理异常，检查是否需要重试
            if queue_task.retry_count < queue_task.max_retries:
                queue_task.retry_count += 1
                queue_task.status = 'queued'  # 重新入队
                queue_task.error_message = str(e)
            else:
                queue_task.status = 'failed'
                queue_task.error_message = str(e)
                queue_task.completed_at = datetime.utcnow()

        finally:
            # 保存任务状态变更
            try:
                db.commit()
            except Exception as e:
                logger.error(f"Failed to save task status: {e}")
                db.rollback()
            finally:
                db.close()

            # 从运行中任务移除
            self.running_tasks.pop(task_id, None)

    async def _check_running_tasks(self):
        """检查运行中的任务状态"""
        current_time = datetime.utcnow()

        for task_id, task_info in list(self.running_tasks.items()):
            # 检查任务是否超时
            if current_time > task_info['timeout_at']:
                logger.warning(f"Task {task_id} timed out")
                await self._handle_timeout_task(task_id, task_info)

    async def _handle_timeout_task(self, task_id: str, task_info: Dict[str, Any]):
        """处理超时的任务"""
        db = SessionLocal()

        try:
            queue_task = db.query(TaskQueue).filter(TaskQueue.id == task_info['queue_task_id']).first()
            if queue_task and queue_task.status == 'running':
                # 检查是否需要重试
                if queue_task.retry_count < queue_task.max_retries:
                    queue_task.retry_count += 1
                    queue_task.status = 'queued'
                    queue_task.error_message = "Task timed out - retrying"
                    logger.info(f"Task {task_id} timed out, retrying ({queue_task.retry_count}/{queue_task.max_retries})")
                else:
                    queue_task.status = 'failed'
                    queue_task.error_message = "Task timed out - max retries exceeded"
                    queue_task.completed_at = datetime.utcnow()
                    logger.error(f"Task {task_id} timed out permanently")

                db.commit()

        except Exception as e:
            logger.error(f"Error handling timeout task {task_id}: {e}")
            db.rollback()
        finally:
            db.close()

        # 从运行中任务移除
        self.running_tasks.pop(task_id, None)

    async def _cleanup_loop(self):
        """清理循环 - 定期清理完成的任务记录"""
        logger.info("Cleanup loop started")

        while self._is_running:
            try:
                await self._cleanup_completed_tasks()
                await asyncio.sleep(self.config.CLEANUP_INTERVAL)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(self.config.CLEANUP_INTERVAL)

    async def _cleanup_completed_tasks(self):
        """清理旧的已完成任务记录"""
        db = SessionLocal()

        try:
            # 清理7天前的已完成任务
            cutoff_time = datetime.utcnow() - timedelta(days=7)

            deleted_count = db.query(TaskQueue).filter(
                and_(
                    TaskQueue.status.in_(['completed', 'failed', 'cancelled']),
                    TaskQueue.completed_at < cutoff_time
                )
            ).delete()

            if deleted_count > 0:
                db.commit()
                logger.info(f"Cleaned up {deleted_count} old task records")

        except Exception as e:
            logger.error(f"Error in cleanup: {e}")
            db.rollback()
        finally:
            db.close()

    def get_queue_status(self, db: Session = None) -> Dict[str, Any]:
        """获取队列状态"""
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False

        try:
            # 统计各状态的任务数量
            queued_count = db.query(TaskQueue).filter(TaskQueue.status == 'queued').count()
            running_count = db.query(TaskQueue).filter(TaskQueue.status == 'running').count()
            completed_count = db.query(TaskQueue).filter(TaskQueue.status == 'completed').count()
            failed_count = db.query(TaskQueue).filter(TaskQueue.status == 'failed').count()

            # 获取队列中的任务列表
            queued_tasks = db.query(TaskQueue).filter(
                TaskQueue.status == 'queued'
            ).order_by(
                TaskQueue.priority.asc(),
                TaskQueue.created_at.asc()
            ).all()

            # 获取运行中的任务
            running_tasks = db.query(TaskQueue).filter(
                TaskQueue.status == 'running'
            ).all()

            return {
                'scheduler_status': 'running' if self._is_running else 'stopped',
                'concurrent_limit': self.config.MAX_CONCURRENT_TASKS,
                'queue_stats': {
                    'queued': queued_count,
                    'running': running_count,
                    'completed': completed_count,
                    'failed': failed_count
                },
                'queued_tasks': [
                    {
                        'id': task.id,
                        'project_id': task.project_id,
                        'priority': task.priority,
                        'created_at': task.created_at.isoformat(),
                        'retry_count': task.retry_count
                    }
                    for task in queued_tasks
                ],
                'running_tasks': [
                    {
                        'id': task.id,
                        'project_id': task.project_id,
                        'started_at': task.started_at.isoformat() if task.started_at else None,
                        'external_task_id': task.external_task_id
                    }
                    for task in running_tasks
                ]
            }

        finally:
            if should_close:
                db.close()

    def cancel_queued_task(self, queue_task_id: int, db: Session = None) -> bool:
        """取消排队中的任务"""
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False

        try:
            task = db.query(TaskQueue).filter(
                and_(
                    TaskQueue.id == queue_task_id,
                    TaskQueue.status == 'queued'
                )
            ).first()

            if task:
                task.status = 'cancelled'
                task.completed_at = datetime.utcnow()
                db.commit()
                logger.info(f"Cancelled queued task: {queue_task_id}")
                return True
            else:
                logger.warning(f"Task {queue_task_id} not found or not in queued status")
                return False

        except Exception as e:
            logger.error(f"Error cancelling task {queue_task_id}: {e}")
            db.rollback()
            return False
        finally:
            if should_close:
                db.close()


# 全局任务调度器实例
task_scheduler = TaskScheduler()