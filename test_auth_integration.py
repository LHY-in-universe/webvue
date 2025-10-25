#!/usr/bin/env python3
"""
测试用户认证集成功能
"""
import requests
import json
import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# 导入认证辅助工具
from test_auth_helper import TestAuthHelper

def test_auth_flow():
    """测试完整的认证流程"""
    base_url = "http://localhost:8000"
    
    print("🧪 开始测试用户认证集成功能...")
    
    # 1. 测试用户注册
    print("\n1. 测试用户注册...")
    import time
    unique_email = f"test{int(time.time())}@example.com"  # 使用时间戳确保邮箱唯一
    register_data = {
        "name": "测试用户",
        "email": unique_email,
        "password": "test123456",
        "confirm_password": "test123456",
        "module": "edgeai"
    }
    
    try:
        response = requests.post(f"{base_url}/api/common/auth/register", json=register_data)
        if response.status_code == 200:
            auth_data = response.json()
            if auth_data.get("success"):
                print("✅ 用户注册成功")
                token = auth_data.get("token")
                user_id = auth_data.get("user", {}).get("id")
                print(f"   Token: {token}")
                print(f"   User ID: {user_id}")
            else:
                print(f"❌ 用户注册失败: {auth_data.get('error')}")
                return False
        else:
            print(f"❌ 注册请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 注册请求异常: {e}")
        return False
    
    # 2. 测试用户登录
    print("\n2. 测试用户登录...")
    login_data = {
        "username": unique_email,  # 使用注册时使用的邮箱
        "password": "test123456",
        "module": "edgeai"
    }
    
    try:
        response = requests.post(f"{base_url}/api/common/auth/login", json=login_data)
        if response.status_code == 200:
            auth_data = response.json()
            if auth_data.get("success"):
                print("✅ 用户登录成功")
                token = auth_data.get("token")
                user_id = auth_data.get("user", {}).get("id")
                print(f"   Token: {token}")
                print(f"   User ID: {user_id}")
            else:
                print(f"❌ 用户登录失败: {auth_data.get('error')}")
                return False
        else:
            print(f"❌ 登录请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 登录请求异常: {e}")
        return False
    
    # 3. 测试创建项目（需要认证）
    print("\n3. 测试创建项目（需要认证）...")
    project_data = {
        "name": "测试项目",
        "description": "这是一个测试项目",
        "model": "test-model",
        "nodes": [{"ip": "192.168.1.100", "name": "测试节点"}],  # 添加必需的nodes字段
        "training_alg": "sft",
        "fed_alg": "fedavg",
        "secure_aggregation": "shamir_threshold",
        "total_epochs": 100,
        "num_rounds": 10,
        "batch_size": 32,
        "lr": "1e-4",
        "num_computers": 3,
        "threshold": 2,
        "num_clients": 2,
        "sample_clients": 2,
        "max_steps": 100,
        "model_name_or_path": "sshleifer/tiny-gpt2",
        "dataset_name": "vicgalle/alpaca-gpt4",
        "dataset_sample": 50
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{base_url}/api/edgeai/projects/", json=project_data, headers=headers)
        if response.status_code == 200:
            project_response = response.json()
            print("✅ 项目创建成功")
            print(f"   项目ID: {project_response.get('id')}")
            print(f"   项目名称: {project_response.get('name')}")
        else:
            print(f"❌ 项目创建失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 项目创建请求异常: {e}")
        return False
    
    # 4. 测试创建集群（需要认证）
    print("\n4. 测试创建集群（需要认证）...")
    cluster_data = {
        "name": "测试集群",
        "project_id": 1  # 假设项目ID为1
    }
    
    try:
        response = requests.post(f"{base_url}/api/edgeai/clusters/", json=cluster_data, headers=headers)
        if response.status_code == 200:
            cluster_response = response.json()
            print("✅ 集群创建成功")
            print(f"   集群ID: {cluster_response.get('id')}")
            print(f"   集群名称: {cluster_response.get('name')}")
            print(f"   用户ID: {cluster_response.get('user_id')}")
        else:
            print(f"❌ 集群创建失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 集群创建请求异常: {e}")
        return False
    
    # 5. 测试无认证访问（应该失败）
    print("\n5. 测试无认证访问（应该失败）...")
    try:
        # 使用简化的项目数据测试无认证访问
        simple_project_data = {
            "name": "无认证测试项目",
            "description": "测试无认证访问",
            "model": "test-model",
            "nodes": [{"ip": "192.168.1.200", "name": "无认证节点"}]
        }
        response = requests.post(f"{base_url}/api/edgeai/projects/", json=simple_project_data)
        if response.status_code == 401:
            print("✅ 无认证访问正确被拒绝")
        else:
            print(f"❌ 无认证访问应该被拒绝，但返回了: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无认证访问测试异常: {e}")
        return False
    
    print("\n🎉 所有认证集成测试通过！")
    return True

def test_mock_user():
    """测试mock用户认证"""
    base_url = "http://localhost:8000"
    
    print("\n🧪 测试新注册用户认证...")
    
    # 注册新用户
    import time
    email = f"mockuser{int(time.time())}@example.com"
    register_data = {
        "name": "Mock测试用户",
        "email": email,
        "password": "test123456",
        "confirm_password": "test123456",
        "module": "edgeai"
    }
    
    try:
        response = requests.post(f"{base_url}/api/common/auth/register", json=register_data)
        if response.status_code == 200:
            auth_data = response.json()
            if auth_data.get("success"):
                print("✅ Mock用户注册成功")
                token = auth_data.get("token")
                user_id = auth_data.get("user", {}).get("id")
                print(f"   Token: {token}")
                print(f"   User ID: {user_id}")
                
                # 测试创建项目
                project_data = {
                    "name": "Mock用户项目",
                    "description": "Mock用户创建的项目",
                    "model": "mock-model",
                    "nodes": [{"ip": "192.168.1.101", "name": "Mock节点"}],  # 添加必需的nodes字段
                    "training_alg": "sft",
                    "fed_alg": "fedavg",
                    "secure_aggregation": "shamir_threshold",
                    "total_epochs": 50,
                    "num_rounds": 5,
                    "batch_size": 16,
                    "lr": "1e-3",
                    "num_computers": 2,
                    "threshold": 1,
                    "num_clients": 1,
                    "sample_clients": 1,
                    "max_steps": 50,
                    "model_name_or_path": "mock-model",
                    "dataset_name": "mock-dataset",
                    "dataset_sample": 25
                }
                
                headers = {"Authorization": f"Bearer {token}"}
                response = requests.post(f"{base_url}/api/edgeai/projects/", json=project_data, headers=headers)
                if response.status_code == 200:
                    project_response = response.json()
                    print("✅ Mock用户项目创建成功")
                    print(f"   项目ID: {project_response.get('id')}")
                    print(f"   用户ID: {project_response.get('user_id', 'N/A')}")
                else:
                    print(f"❌ Mock用户项目创建失败: {response.status_code}")
                    print(f"   响应内容: {response.text}")
                    return False
            else:
                print(f"❌ Mock用户注册失败: {auth_data.get('error')}")
                return False
        else:
            print(f"❌ Mock用户注册请求失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Mock用户测试异常: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 启动认证集成测试...")
    
    # 检查服务器是否运行
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ 服务器未正常运行")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        print("请确保服务器正在运行: python backend/main.py")
        sys.exit(1)
    
    # 运行测试
    success = True
    
    # 测试真实用户认证流程
    if not test_auth_flow():
        success = False
    
    # 测试mock用户认证
    if not test_mock_user():
        success = False
    
    if success:
        print("\n🎉 所有测试通过！用户认证集成功能正常工作。")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败，请检查实现。")
        sys.exit(1)
