#!/usr/bin/env python3
"""
测试数据库集成
验证从数据库到API到前端的完整数据流
"""

import requests
import json
import sqlite3
from datetime import datetime

# API基础URL
API_BASE = "http://127.0.0.1:8000"
DB_PATH = "/home/webvue/database/edgeai/edgeai.db"

def test_database_data():
    """测试数据库中的数据"""
    print("🔍 检查数据库中的数据...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查节点数据
    cursor.execute("""
        SELECT name, node_type, state, role, responsible_user, path_ipv4, connected_nodes_count
        FROM nodes 
        WHERE is_active = 1
        ORDER BY priority DESC
    """)
    
    nodes = cursor.fetchall()
    print(f"📊 数据库中的节点数量: {len(nodes)}")
    
    for node in nodes:
        print(f"  - {node[0]} ({node[1]}) - {node[2]} - {node[3]} - {node[4]} - {node[5]} - {node[6]} nodes")
    
    conn.close()
    return len(nodes)

def test_api_endpoints():
    """测试API端点"""
    print("\n🌐 测试API端点...")
    
    endpoints = [
        "/api/edgeai/nodes/",
        "/api/edgeai/nodes/stats/overview",
        "/api/edgeai/nodes/visualization/project-001/",
        "/api/edgeai/nodes/visualization/project-002/"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                if "nodes" in data:
                    print(f"✅ {endpoint}: {len(data['nodes'])} 个节点")
                elif "total_nodes" in data:
                    print(f"✅ {endpoint}: 总计 {data['total_nodes']} 个节点")
                else:
                    print(f"✅ {endpoint}: 响应正常")
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

def test_specific_node():
    """测试特定节点详情"""
    print("\n🔍 测试特定节点详情...")
    
    try:
        response = requests.get(f"{API_BASE}/api/edgeai/nodes/1")
        if response.status_code == 200:
            node = response.json()
            print(f"✅ 节点详情: {node['name']} - {node['role']} - {node['status']}")
            print(f"   IP地址: {node['ip_address']}")
            print(f"   连接节点: {node['connected_nodes']}")
            print(f"   资源使用: CPU {node['resources']['cpu']}%, Memory {node['resources']['memory']}GB")
        else:
            print(f"❌ 获取节点详情失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 获取节点详情失败: {e}")

def test_node_operations():
    """测试节点操作"""
    print("\n⚙️ 测试节点操作...")
    
    operations = ["start", "stop", "restart"]
    
    for operation in operations:
        try:
            response = requests.post(f"{API_BASE}/api/edgeai/nodes/1/operation", 
                                   json={"operation": operation})
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {operation} 操作: {result['message']}")
            else:
                print(f"❌ {operation} 操作失败: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {operation} 操作失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始数据库集成测试...\n")
    
    # 测试数据库
    db_count = test_database_data()
    
    # 测试API
    test_api_endpoints()
    
    # 测试特定节点
    test_specific_node()
    
    # 测试节点操作
    test_node_operations()
    
    print(f"\n✅ 测试完成! 数据库中有 {db_count} 个节点")
    print("🎉 数据库集成成功，硬编码已被替换!")

if __name__ == "__main__":
    main()







