#!/usr/bin/env python3
"""
EdgeAI Nodes API 测试脚本
测试 backend/edgeai/api/nodes.py 中的所有API端点
Updated with proper authentication flow
"""

import requests
import json
import time
import asyncio
import websockets
from typing import Dict, Any, List
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__)))

from test_auth_helper import TestAuthHelper

class NodesAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api/edgeai/nodes"
        self.test_results = []
        self.created_node_ids = []
        self.auth_helper = TestAuthHelper()
    
    def get_headers(self):
        """获取带认证的请求头"""
        return self.auth_helper.get_headers()
        
    def log_test(self, test_name: str, success: bool, message: str = "", response_data: Any = None):
        """记录测试结果"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if response_data and not success:
            print(f"   Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> tuple:
        """发送HTTP请求并返回响应"""
        url = f"{self.api_base}{endpoint}"
        headers = self.get_headers()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, json=data, headers=headers, timeout=10)
            else:
                return False, {"error": f"Unsupported method: {method}"}
            
            return response.status_code == 200, response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}
        except json.JSONDecodeError as e:
            return False, {"error": f"JSON decode error: {str(e)}"}
    
    def test_get_nodes(self):
        """测试获取节点列表"""
        print("\n🔍 测试获取节点列表...")
        
        # 测试基本获取
        success1, data = self.make_request("GET", "/")
        self.log_test("GET /nodes/", success1, "获取所有节点", data)
        
        # 测试带参数过滤
        success2, data = self.make_request("GET", "/", params={"status": "training"})
        self.log_test("GET /nodes/?status=training", success2, "按状态过滤节点", data)
        
        return success1 and success2
    
    def test_get_node_by_id(self):
        """测试获取特定节点"""
        print("\n🔍 测试获取特定节点...")
        
        # 测试存在的节点
        success1, data = self.make_request("GET", "/1")
        self.log_test("GET /nodes/1", success1, "获取节点1详情", data)
        
        # 测试不存在的节点
        success2, data = self.make_request("GET", "/99999")
        self.log_test("GET /nodes/99999", not success2, "获取不存在的节点应返回404", data)
        
        return success1 and (not success2)  # success2 should be False for 404
    
    def test_get_node_stats(self):
        """测试获取节点统计信息"""
        print("\n📊 测试获取节点统计信息...")
        
        success, data = self.make_request("GET", "/stats/overview")
        self.log_test("GET /nodes/stats/overview", success, "获取节点统计信息", data)
        
        fields_valid = True
        if success and data:
            required_fields = ["total_nodes", "online_nodes", "training_nodes", "idle_nodes", "error_nodes"]
            has_required_fields = all(field in data for field in required_fields)
            self.log_test("Stats fields validation", has_required_fields, "统计信息包含必需字段", data)
            fields_valid = has_required_fields
        
        return success and fields_valid
    
    def test_get_node_metrics(self):
        """测试获取节点性能指标"""
        print("\n📈 测试获取节点性能指标...")
        
        success, data = self.make_request("GET", "/1/metrics")
        self.log_test("GET /nodes/1/metrics", success, "获取节点1性能指标", data)
        
        fields_valid = True
        if success and data:
            required_fields = ["node_id", "cpu_usage", "memory_usage", "gpu_usage", "progress", "status"]
            has_required_fields = all(field in data for field in required_fields)
            self.log_test("Metrics fields validation", has_required_fields, "性能指标包含必需字段", data)
            fields_valid = has_required_fields
        
        return success and fields_valid
    
    def test_node_operations(self):
        """测试节点操作"""
        print("\n⚙️ 测试节点操作...")
        
        # 测试启动操作
        success, data = self.make_request("POST", "/1/operation", {"operation": "start"})
        self.log_test("POST /nodes/1/operation (start)", success, "启动节点操作", data)
        
        # 测试停止操作
        success, data = self.make_request("POST", "/1/operation", {"operation": "stop"})
        self.log_test("POST /nodes/1/operation (stop)", success, "停止节点操作", data)
        
        # 测试重启操作
        success, data = self.make_request("POST", "/1/operation", {"operation": "restart"})
        self.log_test("POST /nodes/1/operation (restart)", success, "重启节点操作", data)
        
        # 测试分配项目操作
        success, data = self.make_request("POST", "/1/operation", {"operation": "assign", "project_id": "1"})
        self.log_test("POST /nodes/1/operation (assign)", success, "分配节点到项目", data)
        
        return success
    
    def test_training_operations(self):
        """测试训练操作"""
        print("\n🏋️ 测试训练操作...")
        
        # 先确保节点在线
        self.make_request("POST", "/1/operation", {"operation": "start"})
        time.sleep(1)
        
        # 测试启动训练
        success, data = self.make_request("POST", "/1/start-training")
        self.log_test("POST /nodes/1/start-training", success, "启动节点训练", data)
        
        # 测试停止训练
        success, data = self.make_request("POST", "/1/stop-training")
        self.log_test("POST /nodes/1/stop-training", success, "停止节点训练", data)
        
        return success
    
    def test_restart_node(self):
        """测试重启节点"""
        print("\n🔄 测试重启节点...")
        
        success, data = self.make_request("POST", "/1/restart")
        self.log_test("POST /nodes/1/restart", success, "重启节点", data)
        
        return success
    
    def test_create_node(self):
        """测试创建节点"""
        print("\n➕ 测试创建节点...")
        
        # 创建测试节点
        node_data = {
            "name": f"Test Node {int(time.time())}",
            "ip": f"192.168.1.{200 + int(time.time()) % 255}"
        }
        
        success, data = self.make_request("POST", "/", node_data)
        self.log_test("POST /nodes/ (create)", success, "创建新节点", data)
        
        if success and data and "id" in data:
            self.created_node_ids.append(data["id"])
            print(f"   创建了节点ID: {data['id']}")
        
        return success
    
    def test_assign_node_to_cluster(self):
        """测试分配节点到集群"""
        print("\n🔗 测试分配节点到集群...")
        
        # 先确保节点1处于idle状态
        self.make_request("POST", "/1/operation", {"operation": "stop"})
        time.sleep(1)
        
        # 如果节点已经在集群中，先退出
        self.make_request("POST", "/1/exit-cluster")
        time.sleep(1)
        
        success, data = self.make_request("POST", "/1/assign-cluster?cluster_id=1")
        self.log_test("POST /nodes/1/assign-cluster", success, "分配节点到集群", data)
        
        return success
    
    def test_exit_node_from_cluster(self):
        """测试节点退出集群"""
        print("\n🔓 测试节点退出集群...")
        
        # 先确保节点1处于idle状态
        self.make_request("POST", "/1/operation", {"operation": "stop"})
        time.sleep(1)
        
        # 如果节点不在集群中，先分配到集群
        self.make_request("POST", "/1/assign-cluster?cluster_id=1")
        time.sleep(1)
        
        # 测试退出集群
        success, data = self.make_request("POST", "/1/exit-cluster")
        self.log_test("POST /nodes/1/exit-cluster", success, "节点退出集群", data)
        
        return success
    
    def test_delete_node(self):
        """测试删除节点"""
        print("\n🗑️ 测试删除节点...")
        
        if self.created_node_ids:
            node_id = self.created_node_ids[-1]  # 删除最后创建的节点
            success, data = self.make_request("DELETE", f"/{node_id}")
            self.log_test(f"DELETE /nodes/{node_id}", success, "删除节点", data)
            
            if success:
                self.created_node_ids.remove(node_id)
        else:
            print("   没有可删除的测试节点")
            success = True
        
        return success
    
    def test_batch_delete_nodes(self):
        """测试批量删除节点"""
        print("\n🗑️ 测试批量删除节点...")
        
        # 先创建几个测试节点
        test_node_ids = []
        for i in range(3):
            node_data = {
                "name": f"Batch Test Node {i}",
                "ip": f"192.168.1.{250 + i + int(time.time()) % 100}"
            }
            success, data = self.make_request("POST", "/", node_data)
            if success and data and "id" in data:
                test_node_ids.append(data["id"])
        
        if test_node_ids:
            # 测试批量删除
            success, data = self.make_request("DELETE", "/batch", {"node_ids": test_node_ids})
            self.log_test("DELETE /nodes/batch", success, "批量删除节点", data)
        else:
            print("   无法创建测试节点进行批量删除测试")
            success = True
        
        return success
    
    def test_visualization_nodes(self):
        """测试获取可视化节点数据"""
        print("\n📊 测试获取可视化节点数据...")
        
        success, data = self.make_request("GET", "/visualization/1/")
        self.log_test("GET /nodes/visualization/1/", success, "获取项目1的可视化节点数据", data)
        
        fields_valid = True
        if success and data:
            required_fields = ["nodes", "project_id", "total_nodes", "network_topology"]
            has_required_fields = all(field in data for field in required_fields)
            self.log_test("Visualization fields validation", has_required_fields, "可视化数据包含必需字段", data)
            fields_valid = has_required_fields
        
        return success and fields_valid
    
    async def test_websocket(self):
        """测试WebSocket连接"""
        print("\n🔌 测试WebSocket连接...")
        
        try:
            uri = f"ws://localhost:8000/api/edgeai/nodes/ws/1"
            async with websockets.connect(uri) as websocket:
                # 等待接收消息
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(message)
                
                if data.get("type") == "node_update":
                    self.log_test("WebSocket /nodes/ws/1", True, "WebSocket连接成功，收到节点更新", data)
                    return True
                else:
                    self.log_test("WebSocket /nodes/ws/1", False, "WebSocket消息格式不正确", data)
                    return False
                    
        except asyncio.TimeoutError:
            self.log_test("WebSocket /nodes/ws/1", False, "WebSocket连接超时", {})
            return False
        except Exception as e:
            self.log_test("WebSocket /nodes/ws/1", False, f"WebSocket连接失败: {str(e)}", {})
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始EdgeAI Nodes API测试...")
        print("=" * 60)
        
        # 设置认证
        print("🔐 Setting up authentication...")
        if not self.auth_helper.setup_auth():
            print("❌ Failed to setup authentication. Cannot run tests.")
            return False
        
        try:
            # 检查服务器是否运行
            try:
                response = requests.get(f"{self.base_url}/docs", timeout=5)
                if response.status_code != 200:
                    print("❌ 服务器未运行或无法访问")
                    return False
            except:
                print("❌ 无法连接到服务器，请确保后端服务正在运行")
                return False
            
            print("✅ 服务器连接正常")
        
        # 运行所有测试
        tests = [
            self.test_get_nodes,
            self.test_get_node_by_id,
            self.test_get_node_stats,
            self.test_get_node_metrics,
            self.test_node_operations,
            self.test_training_operations,
            self.test_restart_node,
            self.test_create_node,
            self.test_assign_node_to_cluster,
            self.test_exit_node_from_cluster,
            self.test_visualization_nodes,
            self.test_delete_node,
            self.test_batch_delete_nodes,
        ]
        
        passed_tests = 0
        total_tests = len(tests) + 1  # +1 for WebSocket test
        
        for test in tests:
            try:
                if test():
                    passed_tests += 1
            except Exception as e:
                print(f"❌ 测试 {test.__name__} 出现异常: {str(e)}")
        
        # 测试WebSocket（异步）
        try:
            if asyncio.run(self.test_websocket()):
                passed_tests += 1
        except Exception as e:
            print(f"❌ WebSocket测试出现异常: {str(e)}")
        
        # 输出测试结果
        print("\n" + "=" * 60)
        print("📊 测试结果汇总:")
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {passed_tests}")
        print(f"失败测试: {total_tests - passed_tests}")
        print(f"成功率: {(passed_tests/total_tests)*100:.1f}%")
        
            # 保存详细测试结果
            self.save_test_results()
            
            return passed_tests == total_tests
            
        finally:
            # 清理认证
            print("\n🔐 Cleaning up authentication...")
            self.auth_helper.cleanup_auth()
    
    def save_test_results(self):
        """保存测试结果到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nodes_api_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 详细测试结果已保存到: {filename}")

def main():
    """主函数"""
    print("EdgeAI Nodes API 测试工具")
    print("=" * 60)
    
    # 检查命令行参数
    base_url = "http://localhost:8000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"测试目标: {base_url}")
    
    # 创建测试器并运行测试
    tester = NodesAPITester(base_url)
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 所有测试通过！")
        sys.exit(0)
    else:
        print("\n⚠️ 部分测试失败，请检查上述输出")
        sys.exit(1)

if __name__ == "__main__":
    main()
