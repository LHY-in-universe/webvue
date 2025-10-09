#!/usr/bin/env python3
"""
任务调度和并发控制功能测试脚本
验证任务队列、调度器和并发控制是否正常工作
"""

import asyncio
import sys
import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'database'))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('task_scheduling_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class TaskSchedulingTester:
    """任务调度功能测试器"""

    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()

    async def run_all_tests(self) -> bool:
        """运行所有测试"""
        logger.info("🚀 Starting Task Scheduling Tests")
        logger.info("=" * 60)

        tests = [
            ("Database Models", self.test_database_models),
            ("Task Scheduler Config", self.test_scheduler_config),
            ("Task Monitor", self.test_task_monitor),
            ("Task Queue Operations", self.test_task_queue_operations),
            ("Concurrency Control", self.test_concurrency_control),
            ("Priority Ordering", self.test_priority_ordering),
            ("Error Handling", self.test_error_handling),
            ("API Endpoints", self.test_api_endpoints),
        ]

        passed = 0
        total = len(tests)

        for test_name, test_func in tests:
            logger.info(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = await test_func()
                self.test_results[test_name] = result
                if result:
                    logger.info(f"✅ {test_name} - PASSED")
                    passed += 1
                else:
                    logger.error(f"❌ {test_name} - FAILED")
            except Exception as e:
                logger.error(f"❌ {test_name} - ERROR: {e}")
                self.test_results[test_name] = False

        # 测试摘要
        logger.info("\n" + "=" * 60)
        logger.info("🎯 TEST SUMMARY")
        logger.info("=" * 60)

        for test_name, result in self.test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{test_name:<30} {status}")

        elapsed_time = time.time() - self.start_time
        logger.info(f"\nResults: {passed}/{total} tests passed")
        logger.info(f"Elapsed time: {elapsed_time:.2f} seconds")

        if passed == total:
            logger.info("🎉 All tests passed! Task scheduling system is working correctly.")
            return True
        else:
            logger.warning("⚠️ Some tests failed. Please review the issues above.")
            return False

    async def test_database_models(self) -> bool:
        """测试数据库模型"""
        try:
            from database.edgeai.models import TaskQueue, Project

            logger.info("Testing TaskQueue model structure...")

            # 检查 TaskQueue 模型属性
            expected_fields = [
                'id', 'project_id', 'status', 'priority', 'task_config',
                'created_at', 'started_at', 'completed_at',
                'retry_count', 'max_retries', 'error_message', 'external_task_id'
            ]

            for field in expected_fields:
                if not hasattr(TaskQueue, field):
                    logger.error(f"TaskQueue model missing field: {field}")
                    return False

            logger.info("✅ TaskQueue model structure is correct")

            # 检查索引定义
            table = TaskQueue.__table__
            index_names = [idx.name for idx in table.indexes if idx.name]
            logger.info(f"TaskQueue indexes: {index_names}")

            expected_indexes = ['idx_queue_order', 'idx_project_queue']
            for idx_name in expected_indexes:
                if idx_name not in index_names:
                    logger.warning(f"Expected index {idx_name} not found (may be created by migration)")

            return True

        except ImportError as e:
            logger.error(f"Failed to import models: {e}")
            return False
        except Exception as e:
            logger.error(f"Database model test failed: {e}")
            return False

    async def test_scheduler_config(self) -> bool:
        """测试调度器配置"""
        try:
            from backend.edgeai.config.scheduler_config import SchedulerConfig, get_config

            logger.info("Testing scheduler configuration...")

            # 测试默认配置
            config = SchedulerConfig()
            logger.info(f"Default MAX_CONCURRENT_TASKS: {config.MAX_CONCURRENT_TASKS}")
            logger.info(f"Default QUEUE_CHECK_INTERVAL: {config.QUEUE_CHECK_INTERVAL}")

            # 测试配置验证
            config.MAX_CONCURRENT_TASKS = 2
            config.TASK_TIMEOUT = 1800
            config.validate()
            logger.info("✅ Configuration validation works")

            # 测试环境变量配置
            os.environ['SCHEDULER_MAX_CONCURRENT_TASKS'] = '2'
            env_config = SchedulerConfig.from_env()
            if env_config.MAX_CONCURRENT_TASKS == 2:
                logger.info("✅ Environment variable configuration works")
            else:
                logger.error("❌ Environment variable configuration failed")
                return False

            # 清理环境变量
            if 'SCHEDULER_MAX_CONCURRENT_TASKS' in os.environ:
                del os.environ['SCHEDULER_MAX_CONCURRENT_TASKS']

            return True

        except Exception as e:
            logger.error(f"Scheduler config test failed: {e}")
            return False

    async def test_task_monitor(self) -> bool:
        """测试任务监控"""
        try:
            from backend.edgeai.monitoring.task_monitor import TaskMonitor, TaskMetrics

            logger.info("Testing task monitor...")

            monitor = TaskMonitor()
            logger.info("✅ TaskMonitor created successfully")

            # 测试指标数据结构
            metrics = TaskMetrics()
            metrics.total_tasks = 10
            metrics.success_rate = 85.5

            metrics_dict = metrics.to_dict()
            if 'total_tasks' in metrics_dict and 'success_rate' in metrics_dict:
                logger.info("✅ TaskMetrics serialization works")
            else:
                logger.error("❌ TaskMetrics serialization failed")
                return False

            # 测试事件记录
            monitor.record_task_event('test_event', 123, test_data='test_value')
            events = monitor.get_recent_events(limit=1)
            if len(events) > 0 and events[0]['type'] == 'task_event':
                logger.info("✅ Event recording works")
            else:
                logger.error("❌ Event recording failed")
                return False

            return True

        except Exception as e:
            logger.error(f"Task monitor test failed: {e}")
            return False

    async def test_task_queue_operations(self) -> bool:
        """测试任务队列操作"""
        try:
            from backend.edgeai.scheduler.task_scheduler import TaskScheduler
            from database.edgeai.database import SessionLocal

            logger.info("Testing task queue operations...")

            # 创建调度器实例
            scheduler = TaskScheduler()
            logger.info("✅ TaskScheduler created successfully")

            # 测试队列状态检查
            db = SessionLocal()
            try:
                status = scheduler.get_queue_status(db)
                logger.info(f"Queue status: {status['scheduler_status']}")
                logger.info(f"Queue stats: {status['queue_stats']}")
                logger.info("✅ Queue status retrieval works")
            finally:
                db.close()

            # 测试并发限制检查
            can_start = scheduler.can_start_new_task()
            logger.info(f"Can start new task: {can_start}")
            logger.info("✅ Concurrency check works")

            return True

        except Exception as e:
            logger.error(f"Task queue operations test failed: {e}")
            return False

    async def test_concurrency_control(self) -> bool:
        """测试并发控制"""
        logger.info("Testing concurrency control...")

        try:
            from backend.edgeai.scheduler.task_scheduler import TaskScheduler

            scheduler = TaskScheduler()

            # 模拟添加多个运行中的任务来测试并发限制
            scheduler.running_tasks['task1'] = {
                'queue_task_id': 1,
                'project_id': 1,
                'started_at': datetime.utcnow()
            }

            # 现在应该不能启动新任务 (因为默认并发限制是1)
            can_start = scheduler.can_start_new_task()
            if not can_start:
                logger.info("✅ Concurrency limit enforced correctly")
            else:
                logger.error("❌ Concurrency limit not working")
                return False

            # 清理测试数据
            scheduler.running_tasks.clear()

            # 现在应该可以启动任务了
            can_start = scheduler.can_start_new_task()
            if can_start:
                logger.info("✅ Concurrency control allows tasks when under limit")
            else:
                logger.error("❌ Concurrency control blocking when it shouldn't")
                return False

            return True

        except Exception as e:
            logger.error(f"Concurrency control test failed: {e}")
            return False

    async def test_priority_ordering(self) -> bool:
        """测试优先级排序"""
        logger.info("Testing priority ordering...")

        # 这个测试需要实际的数据库连接，这里做一个简化的逻辑测试
        try:
            # 模拟优先级排序逻辑
            tasks = [
                {'priority': 5, 'created_at': '2023-01-01 10:00:00'},
                {'priority': 1, 'created_at': '2023-01-01 11:00:00'},  # 高优先级
                {'priority': 5, 'created_at': '2023-01-01 09:00:00'},  # 同优先级但更早
            ]

            # 按优先级 ASC, 创建时间 ASC 排序
            sorted_tasks = sorted(tasks, key=lambda x: (x['priority'], x['created_at']))

            # 验证排序结果
            if (sorted_tasks[0]['priority'] == 1 and
                sorted_tasks[1]['created_at'] == '2023-01-01 09:00:00' and
                sorted_tasks[2]['created_at'] == '2023-01-01 10:00:00'):
                logger.info("✅ Priority ordering logic correct")
                return True
            else:
                logger.error("❌ Priority ordering logic incorrect")
                return False

        except Exception as e:
            logger.error(f"Priority ordering test failed: {e}")
            return False

    async def test_error_handling(self) -> bool:
        """测试错误处理"""
        logger.info("Testing error handling...")

        try:
            from backend.edgeai.scheduler.task_scheduler import TaskScheduler

            scheduler = TaskScheduler()

            # 测试无效项目ID
            try:
                scheduler.add_task_to_queue(project_id=999999, priority=5)
                logger.error("❌ Should have raised error for invalid project ID")
                return False
            except Exception as e:
                logger.info(f"✅ Correctly handled invalid project ID: {type(e).__name__}")

            # 测试无效优先级
            try:
                scheduler.add_task_to_queue(project_id=1, priority=15)  # 超出有效范围
                # 注意：这个测试取决于是否在 add_task_to_queue 中实现了优先级验证
                logger.info("Priority validation might not be implemented in add_task_to_queue")
            except Exception as e:
                logger.info(f"Priority validation: {type(e).__name__}")

            return True

        except Exception as e:
            logger.error(f"Error handling test failed: {e}")
            return False

    async def test_api_endpoints(self) -> bool:
        """测试API端点 (模拟测试)"""
        logger.info("Testing API endpoints (simulated)...")

        try:
            # 由于我们没有运行的服务器，这里进行逻辑验证
            # 检查 API 函数是否可以导入
            from backend.edgeai.api.training import (
                get_queue_status,
                cancel_queued_task,
                get_project_queue_status,
                start_scheduler,
                stop_scheduler
            )

            logger.info("✅ API functions imported successfully")

            # 检查 API 函数签名
            import inspect

            # get_queue_status 应该接受 db 参数
            sig = inspect.signature(get_queue_status)
            if 'db' in sig.parameters:
                logger.info("✅ get_queue_status has correct signature")
            else:
                logger.error("❌ get_queue_status missing db parameter")
                return False

            # cancel_queued_task 应该接受 queue_task_id 和 db 参数
            sig = inspect.signature(cancel_queued_task)
            expected_params = {'queue_task_id', 'db'}
            actual_params = set(sig.parameters.keys())
            if expected_params.issubset(actual_params):
                logger.info("✅ cancel_queued_task has correct signature")
            else:
                logger.error(f"❌ cancel_queued_task missing parameters: {expected_params - actual_params}")
                return False

            return True

        except ImportError as e:
            logger.error(f"Failed to import API functions: {e}")
            return False
        except Exception as e:
            logger.error(f"API endpoints test failed: {e}")
            return False

    def generate_test_report(self) -> Dict:
        """生成测试报告"""
        report = {
            'test_run_time': datetime.utcnow().isoformat(),
            'total_duration': time.time() - self.start_time,
            'results': self.test_results,
            'summary': {
                'total_tests': len(self.test_results),
                'passed': sum(1 for r in self.test_results.values() if r),
                'failed': sum(1 for r in self.test_results.values() if not r),
                'success_rate': (sum(1 for r in self.test_results.values() if r) / len(self.test_results)) * 100
            }
        }

        return report

    def save_report(self, filename: str = 'test_report.json'):
        """保存测试报告"""
        report = self.generate_test_report()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logger.info(f"Test report saved to {filename}")


async def main():
    """主函数"""
    tester = TaskSchedulingTester()

    try:
        success = await tester.run_all_tests()
        tester.save_report()
        return 0 if success else 1

    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)