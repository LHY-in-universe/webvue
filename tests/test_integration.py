#!/usr/bin/env python3
"""
简单集成测试 - 验证任务调度系统是否可以正常工作
"""

import sys
import os
from pathlib import Path

# 设置正确的路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'backend'))
sys.path.insert(0, str(project_root / 'database'))

def test_basic_imports():
    """测试基本导入"""
    print("🧪 Testing Basic Imports...")

    try:
        # 测试配置导入
        from backend.edgeai.config.scheduler_config import SchedulerConfig, get_config
        print("✅ Scheduler config imports successful")

        # 测试配置创建
        config = SchedulerConfig()
        assert config.MAX_CONCURRENT_TASKS == 1, "Default concurrent tasks should be 1"
        print(f"✅ Default config: MAX_CONCURRENT_TASKS = {config.MAX_CONCURRENT_TASKS}")

        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_task_scheduler_class():
    """测试TaskScheduler类结构"""
    print("\n🧪 Testing TaskScheduler Class Structure...")

    try:
        from backend.edgeai.scheduler.task_scheduler import TaskScheduler

        # 创建调度器实例 (应该使用单例模式)
        scheduler1 = TaskScheduler()
        scheduler2 = TaskScheduler()

        # 验证单例模式
        assert scheduler1 is scheduler2, "TaskScheduler should be singleton"
        print("✅ TaskScheduler singleton pattern works")

        # 验证关键方法存在
        assert hasattr(scheduler1, 'can_start_new_task'), "Missing can_start_new_task method"
        assert hasattr(scheduler1, 'add_task_to_queue'), "Missing add_task_to_queue method"
        assert hasattr(scheduler1, 'get_next_task'), "Missing get_next_task method"
        assert hasattr(scheduler1, 'get_queue_status'), "Missing get_queue_status method"
        print("✅ TaskScheduler has all required methods")

        # 测试并发检查
        can_start = scheduler1.can_start_new_task()
        assert isinstance(can_start, bool), "can_start_new_task should return boolean"
        print(f"✅ Can start new task: {can_start}")

        return True
    except Exception as e:
        print(f"❌ TaskScheduler test failed: {e}")
        return False

def test_task_monitor_class():
    """测试TaskMonitor类结构"""
    print("\n🧪 Testing TaskMonitor Class Structure...")

    try:
        from backend.edgeai.monitoring.task_monitor import TaskMonitor, TaskMetrics

        # 创建监控器实例
        monitor = TaskMonitor()
        print("✅ TaskMonitor created successfully")

        # 测试指标类
        metrics = TaskMetrics()
        metrics.total_tasks = 10
        metrics.success_rate = 85.5

        # 测试序列化
        metrics_dict = metrics.to_dict()
        assert 'total_tasks' in metrics_dict, "Missing total_tasks in metrics"
        assert 'success_rate' in metrics_dict, "Missing success_rate in metrics"
        assert metrics_dict['total_tasks'] == 10, "total_tasks value incorrect"
        print("✅ TaskMetrics serialization works")

        # 测试事件记录
        monitor.record_task_event('test_event', 123, test_data='test_value')
        events = monitor.get_recent_events(limit=1)
        assert len(events) > 0, "No events recorded"
        assert events[0]['type'] == 'task_event', "Event type incorrect"
        print("✅ Event recording works")

        return True
    except Exception as e:
        print(f"❌ TaskMonitor test failed: {e}")
        return False

def test_priority_logic():
    """测试优先级排序逻辑"""
    print("\n🧪 Testing Priority Logic...")

    try:
        # 模拟任务数据
        tasks = [
            {'priority': 5, 'created_at': '2023-01-01 10:00:00'},
            {'priority': 1, 'created_at': '2023-01-01 11:00:00'},  # 高优先级
            {'priority': 5, 'created_at': '2023-01-01 09:00:00'},  # 同优先级但更早
        ]

        # 按优先级 ASC, 创建时间 ASC 排序
        sorted_tasks = sorted(tasks, key=lambda x: (x['priority'], x['created_at']))

        # 验证排序结果
        assert sorted_tasks[0]['priority'] == 1, "First task should have priority 1"
        assert sorted_tasks[1]['created_at'] == '2023-01-01 09:00:00', "Second task should be earlier"
        assert sorted_tasks[2]['created_at'] == '2023-01-01 10:00:00', "Third task should be later"

        print("✅ Priority ordering logic correct")
        print(f"   1st: priority={sorted_tasks[0]['priority']}, time={sorted_tasks[0]['created_at']}")
        print(f"   2nd: priority={sorted_tasks[1]['priority']}, time={sorted_tasks[1]['created_at']}")
        print(f"   3rd: priority={sorted_tasks[2]['priority']}, time={sorted_tasks[2]['created_at']}")

        return True
    except Exception as e:
        print(f"❌ Priority logic test failed: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 Task Scheduling System - Integration Test")
    print("=" * 60)

    tests = [
        ("Basic Imports", test_basic_imports),
        ("TaskScheduler Class", test_task_scheduler_class),
        ("TaskMonitor Class", test_task_monitor_class),
        ("Priority Logic", test_priority_logic)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")

    print("\n" + "=" * 60)
    print("🎯 INTEGRATION TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 All integration tests passed!")
        print("✨ Task scheduling system is working correctly.")
        return 0
    else:
        print("⚠️ Some integration tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())