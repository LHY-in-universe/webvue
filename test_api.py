#!/usr/bin/env python3
"""
测试 API 端点
"""
import requests
import json

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 测试 API 端点...")
    
    # 测试项目 API
    try:
        print("\n1. 测试项目 API...")
        response = requests.get(f"{base_url}/api/edgeai/projects/", 
                              headers={"accept": "application/json"})
        print(f"   状态码: {response.status_code}")
        print(f"   响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   数据类型: {type(data)}")
            print(f"   数据长度: {len(data) if isinstance(data, list) else 'N/A'}")
            print(f"   数据内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   错误响应: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 项目 API 测试失败: {e}")
    
    # 测试节点 API
    try:
        print("\n2. 测试节点 API...")
        response = requests.get(f"{base_url}/api/edgeai/nodes/", 
                              headers={"accept": "application/json"})
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   数据类型: {type(data)}")
            print(f"   数据长度: {len(data) if isinstance(data, list) else 'N/A'}")
            print(f"   数据内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   错误响应: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 节点 API 测试失败: {e}")
    
    # 测试日志 API
    try:
        print("\n3. 测试日志 API...")
        response = requests.get(f"{base_url}/api/edgeai/logs/", 
                              headers={"accept": "application/json"})
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   数据类型: {type(data)}")
            print(f"   数据长度: {len(data) if isinstance(data, list) else 'N/A'}")
            print(f"   数据内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   错误响应: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 日志 API 测试失败: {e}")

if __name__ == "__main__":
    test_api()


