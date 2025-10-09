"""
任务监控和指标收集模块
提供任务执行统计、性能监控和告警功能
"""

import asyncio
import logging
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict, deque
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from database.edgeai import TaskQueue
from database.edgeai.database import SessionLocal


# 配置日志
logger = logging.getLogger(__name__)


@dataclass
class TaskMetrics:
    """任务指标数据类"""
    total_tasks: int = 0
    queued_tasks: int = 0
    running_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    cancelled_tasks: int = 0

    # 时间相关指标
    avg_queue_time: float = 0.0  # 平均排队时间 (秒)
    avg_execution_time: float = 0.0  # 平均执行时间 (秒)
    total_execution_time: float = 0.0  # 总执行时间 (秒)

    # 性能指标
    tasks_per_hour: float = 0.0
    success_rate: float = 0.0
    failure_rate: float = 0.0

    # 最近任务状态
    recent_completions: List[Dict[str, Any]] = field(default_factory=list)
    recent_failures: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'total_tasks': self.total_tasks,
            'queued_tasks': self.queued_tasks,
            'running_tasks': self.running_tasks,
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'cancelled_tasks': self.cancelled_tasks,
            'avg_queue_time': round(self.avg_queue_time, 2),
            'avg_execution_time': round(self.avg_execution_time, 2),
            'total_execution_time': round(self.total_execution_time, 2),
            'tasks_per_hour': round(self.tasks_per_hour, 2),
            'success_rate': round(self.success_rate, 2),
            'failure_rate': round(self.failure_rate, 2),
            'recent_completions': self.recent_completions[-10:],  # 最近10个
            'recent_failures': self.recent_failures[-10:]  # 最近10个
        }


@dataclass
class SystemHealth:
    """系统健康状态"""
    scheduler_running: bool = False
    database_connected: bool = False
    last_health_check: Optional[datetime] = None
    uptime_seconds: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0

    # 告警状态
    high_queue_length: bool = False
    long_running_tasks: bool = False
    high_failure_rate: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'scheduler_running': self.scheduler_running,
            'database_connected': self.database_connected,
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None,
            'uptime_seconds': round(self.uptime_seconds, 2),
            'memory_usage_mb': round(self.memory_usage_mb, 2),
            'cpu_usage_percent': round(self.cpu_usage_percent, 2),
            'high_queue_length': self.high_queue_length,
            'long_running_tasks': self.long_running_tasks,
            'high_failure_rate': self.high_failure_rate
        }


class TaskMonitor:
    """任务监控器"""

    def __init__(self):
        self.start_time = time.time()
        self.metrics_history = deque(maxlen=100)  # 保存最近100次指标
        self.event_log = deque(maxlen=1000)  # 保存最近1000个事件
        self.is_running = False
        self.monitor_task: Optional[asyncio.Task] = None

        # 性能计数器
        self.task_counters = defaultdict(int)
        self.timing_data = defaultdict(list)

        logger.info("TaskMonitor initialized")

    async def start(self, check_interval: int = 60):
        """启动监控"""
        if self.is_running:
            logger.warning("TaskMonitor is already running")
            return

        self.is_running = True
        self.monitor_task = asyncio.create_task(self._monitor_loop(check_interval))
        logger.info("TaskMonitor started")

    async def stop(self):
        """停止监控"""
        if not self.is_running:
            return

        self.is_running = False
        if self.monitor_task and not self.monitor_task.done():
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass

        logger.info("TaskMonitor stopped")

    async def _monitor_loop(self, check_interval: int):
        """监控主循环"""
        logger.info(f"Monitor loop started with {check_interval}s interval")

        while self.is_running:
            try:
                await self._collect_metrics()
                await asyncio.sleep(check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                logger.error(traceback.format_exc())
                await asyncio.sleep(check_interval)

    async def _collect_metrics(self):
        """收集指标数据"""
        db = SessionLocal()
        try:
            metrics = await self._calculate_metrics(db)
            health = await self._check_system_health(db)

            # 保存到历史记录
            self.metrics_history.append({
                'timestamp': datetime.utcnow(),
                'metrics': metrics,
                'health': health
            })

            # 记录事件
            self._log_event('metrics_collected', {
                'total_tasks': metrics.total_tasks,
                'success_rate': metrics.success_rate
            })

            # 检查告警条件
            await self._check_alerts(metrics, health)

        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            self._log_event('metrics_error', {'error': str(e)})
        finally:
            db.close()

    async def _calculate_metrics(self, db: Session) -> TaskMetrics:
        """计算任务指标"""
        metrics = TaskMetrics()

        # 基础统计
        status_counts = db.query(
            TaskQueue.status,
            func.count(TaskQueue.id)
        ).group_by(TaskQueue.status).all()

        status_dict = dict(status_counts)
        metrics.total_tasks = sum(status_dict.values())
        metrics.queued_tasks = status_dict.get('queued', 0)
        metrics.running_tasks = status_dict.get('running', 0)
        metrics.completed_tasks = status_dict.get('completed', 0)
        metrics.failed_tasks = status_dict.get('failed', 0)
        metrics.cancelled_tasks = status_dict.get('cancelled', 0)

        # 成功率和失败率
        if metrics.total_tasks > 0:
            metrics.success_rate = (metrics.completed_tasks / metrics.total_tasks) * 100
            metrics.failure_rate = (metrics.failed_tasks / metrics.total_tasks) * 100

        # 时间相关指标
        completed_tasks = db.query(TaskQueue).filter(
            and_(
                TaskQueue.status == 'completed',
                TaskQueue.started_at.isnot(None),
                TaskQueue.completed_at.isnot(None)
            )
        ).all()

        if completed_tasks:
            queue_times = []
            execution_times = []

            for task in completed_tasks:
                # 排队时间：从创建到开始
                if task.started_at:
                    queue_time = (task.started_at - task.created_at).total_seconds()
                    queue_times.append(queue_time)

                # 执行时间：从开始到完成
                if task.started_at and task.completed_at:
                    execution_time = (task.completed_at - task.started_at).total_seconds()
                    execution_times.append(execution_time)

            if queue_times:
                metrics.avg_queue_time = sum(queue_times) / len(queue_times)

            if execution_times:
                metrics.avg_execution_time = sum(execution_times) / len(execution_times)
                metrics.total_execution_time = sum(execution_times)

        # 每小时任务数 (基于最近24小时)
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        recent_completions = db.query(TaskQueue).filter(
            and_(
                TaskQueue.status == 'completed',
                TaskQueue.completed_at >= twenty_four_hours_ago
            )
        ).count()

        metrics.tasks_per_hour = recent_completions / 24.0

        # 最近的完成和失败任务
        recent_completed = db.query(TaskQueue).filter(
            TaskQueue.status == 'completed'
        ).order_by(TaskQueue.completed_at.desc()).limit(10).all()

        metrics.recent_completions = [
            {
                'id': task.id,
                'project_id': task.project_id,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'execution_time': (
                    (task.completed_at - task.started_at).total_seconds()
                    if task.completed_at and task.started_at
                    else None
                )
            }
            for task in recent_completed
        ]

        recent_failed = db.query(TaskQueue).filter(
            TaskQueue.status == 'failed'
        ).order_by(TaskQueue.completed_at.desc()).limit(10).all()

        metrics.recent_failures = [
            {
                'id': task.id,
                'project_id': task.project_id,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'error_message': task.error_message,
                'retry_count': task.retry_count
            }
            for task in recent_failed
        ]

        return metrics

    async def _check_system_health(self, db: Session) -> SystemHealth:
        """检查系统健康状态"""
        health = SystemHealth()
        health.last_health_check = datetime.utcnow()
        health.uptime_seconds = time.time() - self.start_time

        # 检查数据库连接
        try:
            db.execute("SELECT 1")
            health.database_connected = True
        except Exception as e:
            health.database_connected = False
            logger.error(f"Database health check failed: {e}")

        # 检查调度器状态 (需要从调度器获取)
        # 这里可以添加对调度器的健康检查

        # 获取系统资源使用情况
        try:
            import psutil
            process = psutil.Process()
            health.memory_usage_mb = process.memory_info().rss / 1024 / 1024
            health.cpu_usage_percent = process.cpu_percent()
        except ImportError:
            logger.warning("psutil not available, system resource monitoring disabled")

        return health

    async def _check_alerts(self, metrics: TaskMetrics, health: SystemHealth):
        """检查告警条件"""
        alerts = []

        # 高队列长度告警
        if metrics.queued_tasks > 10:
            health.high_queue_length = True
            alerts.append({
                'type': 'high_queue_length',
                'message': f'High queue length: {metrics.queued_tasks} tasks',
                'severity': 'warning'
            })

        # 高失败率告警
        if metrics.failure_rate > 20:
            health.high_failure_rate = True
            alerts.append({
                'type': 'high_failure_rate',
                'message': f'High failure rate: {metrics.failure_rate:.1f}%',
                'severity': 'error'
            })

        # 长时间运行任务告警
        db = SessionLocal()
        try:
            long_running_threshold = datetime.utcnow() - timedelta(hours=2)
            long_running_tasks = db.query(TaskQueue).filter(
                and_(
                    TaskQueue.status == 'running',
                    TaskQueue.started_at < long_running_threshold
                )
            ).count()

            if long_running_tasks > 0:
                health.long_running_tasks = True
                alerts.append({
                    'type': 'long_running_tasks',
                    'message': f'{long_running_tasks} tasks running longer than 2 hours',
                    'severity': 'warning'
                })
        finally:
            db.close()

        # 记录告警
        for alert in alerts:
            self._log_event('alert', alert)
            logger.warning(f"ALERT: {alert['message']}")

    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """记录事件"""
        event = {
            'timestamp': datetime.utcnow(),
            'type': event_type,
            'data': data
        }
        self.event_log.append(event)

    def get_current_metrics(self) -> Optional[Dict[str, Any]]:
        """获取当前指标"""
        if self.metrics_history:
            latest = self.metrics_history[-1]
            return {
                'timestamp': latest['timestamp'].isoformat(),
                'metrics': latest['metrics'].to_dict(),
                'health': latest['health'].to_dict()
            }
        return None

    def get_metrics_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取指标历史"""
        history = list(self.metrics_history)[-limit:]
        return [
            {
                'timestamp': item['timestamp'].isoformat(),
                'metrics': item['metrics'].to_dict(),
                'health': item['health'].to_dict()
            }
            for item in history
        ]

    def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取最近事件"""
        events = list(self.event_log)[-limit:]
        return [
            {
                'timestamp': event['timestamp'].isoformat(),
                'type': event['type'],
                'data': event['data']
            }
            for event in events
        ]

    def record_task_event(self, event_type: str, task_id: int, **kwargs):
        """记录任务事件"""
        self._log_event('task_event', {
            'event_type': event_type,
            'task_id': task_id,
            **kwargs
        })

    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要"""
        if not self.metrics_history:
            return {}

        latest = self.metrics_history[-1]
        metrics = latest['metrics']
        health = latest['health']

        return {
            'uptime_hours': round(health.uptime_seconds / 3600, 2),
            'total_tasks_processed': metrics.completed_tasks + metrics.failed_tasks,
            'current_queue_length': metrics.queued_tasks,
            'success_rate': metrics.success_rate,
            'avg_processing_time': metrics.avg_execution_time,
            'tasks_per_hour': metrics.tasks_per_hour,
            'system_health': {
                'database_ok': health.database_connected,
                'memory_usage_mb': health.memory_usage_mb,
                'cpu_usage': health.cpu_usage_percent
            },
            'alerts': {
                'high_queue': health.high_queue_length,
                'long_running': health.long_running_tasks,
                'high_failure_rate': health.high_failure_rate
            }
        }


# 全局监控器实例
task_monitor = TaskMonitor()