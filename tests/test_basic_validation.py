#!/usr/bin/env python3
"""
基础验证测试脚本
验证代码文件的语法和基本结构
"""

import os
import sys
import ast
import importlib.util
from pathlib import Path

def test_python_syntax(file_path: str) -> bool:
    """测试Python文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        ast.parse(source)
        print(f"✅ {file_path} - Syntax OK")
        return True
    except SyntaxError as e:
        print(f"❌ {file_path} - Syntax Error: {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path} - Error: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    base_path = Path(__file__).parent.parent

    # 要验证的文件列表
    files_to_check = [
        "database/edgeai/models.py",
        "backend/edgeai/scheduler/task_scheduler.py",
        "backend/edgeai/config/scheduler_config.py",
        "backend/edgeai/monitoring/task_monitor.py",
        "backend/edgeai/api/training.py",
        "database/migrations/002_task_queue_migration.sql",
        "database/migrations/run_task_queue_migration.py"
    ]

    print("🧪 Testing File Structure and Syntax")
    print("=" * 60)

    passed = 0
    total = len(files_to_check)

    for file_path in files_to_check:
        full_path = base_path / file_path

        if not full_path.exists():
            print(f"❌ {file_path} - File not found")
            continue

        if file_path.endswith('.py'):
            if test_python_syntax(str(full_path)):
                passed += 1
        else:
            print(f"✅ {file_path} - File exists")
            passed += 1

    print("\n" + "=" * 60)
    print("📊 RESULTS")
    print("=" * 60)
    print(f"Files checked: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")

    if passed == total:
        print("🎉 All files are valid!")
        return True
    else:
        print("⚠️ Some files have issues.")
        return False

def test_key_components():
    """测试关键组件是否包含预期内容"""
    base_path = Path(__file__).parent.parent

    print("\n🔍 Testing Key Components")
    print("=" * 60)

    tests_passed = 0
    total_tests = 0

    # 测试 TaskQueue 模型
    total_tests += 1
    models_file = base_path / "database/edgeai/models.py"
    if models_file.exists():
        with open(models_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'class TaskQueue' in content and 'task_queue' in content:
                print("✅ TaskQueue model found in models.py")
                tests_passed += 1
            else:
                print("❌ TaskQueue model not found in models.py")
    else:
        print("❌ models.py not found")

    # 测试任务调度器
    total_tests += 1
    scheduler_file = base_path / "backend/edgeai/scheduler/task_scheduler.py"
    if scheduler_file.exists():
        with open(scheduler_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'class TaskScheduler' in content and 'MAX_CONCURRENT_TASKS' in content:
                print("✅ TaskScheduler class found")
                tests_passed += 1
            else:
                print("❌ TaskScheduler class incomplete")
    else:
        print("❌ task_scheduler.py not found")

    # 测试API接口
    total_tests += 1
    training_file = base_path / "backend/edgeai/api/training.py"
    if training_file.exists():
        with open(training_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'get_queue_status' in content and 'cancel_queued_task' in content:
                print("✅ Queue management API endpoints found")
                tests_passed += 1
            else:
                print("❌ Queue management API endpoints not found")
    else:
        print("❌ training.py not found")

    # 测试配置管理
    total_tests += 1
    config_file = base_path / "backend/edgeai/config/scheduler_config.py"
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'class SchedulerConfig' in content and 'MAX_CONCURRENT_TASKS' in content:
                print("✅ SchedulerConfig class found")
                tests_passed += 1
            else:
                print("❌ SchedulerConfig class incomplete")
    else:
        print("❌ scheduler_config.py not found")

    # 测试监控模块
    total_tests += 1
    monitor_file = base_path / "backend/edgeai/monitoring/task_monitor.py"
    if monitor_file.exists():
        with open(monitor_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'class TaskMonitor' in content and 'TaskMetrics' in content:
                print("✅ TaskMonitor class found")
                tests_passed += 1
            else:
                print("❌ TaskMonitor class incomplete")
    else:
        print("❌ task_monitor.py not found")

    print(f"\nComponent tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests

def test_sql_migration():
    """测试SQL迁移文件"""
    base_path = Path(__file__).parent.parent

    print("\n🗄️ Testing SQL Migration")
    print("=" * 60)

    sql_file = base_path / "database/migrations/002_task_queue_migration.sql"
    if not sql_file.exists():
        print("❌ SQL migration file not found")
        return False

    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()

    expected_elements = [
        'CREATE TABLE',
        'task_queue',
        'CREATE INDEX',
        'idx_queue_order',
        'priority',
        'status',
        'created_at'
    ]

    missing_elements = []
    for element in expected_elements:
        if element not in content:
            missing_elements.append(element)

    if not missing_elements:
        print("✅ SQL migration contains all expected elements")
        return True
    else:
        print(f"❌ SQL migration missing elements: {missing_elements}")
        return False

def main():
    """主函数"""
    print("🚀 Task Scheduling System - Basic Validation")
    print("=" * 60)

    results = []

    # 运行各项测试
    results.append(test_file_structure())
    results.append(test_key_components())
    results.append(test_sql_migration())

    # 总结
    passed_tests = sum(results)
    total_tests = len(results)

    print("\n" + "🎯 FINAL SUMMARY")
    print("=" * 60)
    print(f"Test categories passed: {passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        print("🎉 All validation tests passed!")
        print("✨ Task scheduling system appears to be correctly implemented.")
        return 0
    else:
        print("⚠️ Some validation tests failed.")
        print("Please review the issues above before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())