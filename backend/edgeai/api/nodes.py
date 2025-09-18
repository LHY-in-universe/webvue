from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Optional
from ..schemas.edgeai import (
    NodeResponse,
    NodeOperationRequest,
    NodeStatus,
    NodeType
)
from common.schemas.common import BaseResponse
import asyncio
import json

router = APIRouter()

# Mock nodes database with expanded geographic diversity
import random
from datetime import datetime, timedelta

def generate_dynamic_nodes():
    """生成动态节点数据"""
    node_templates = [
        # 控制节点
        {"name": "Control Center Alpha", "type": "control", "location": "US East - Virginia", "projects": ["System"], "tier": "primary"},
        {"name": "Control Center Beta", "type": "control", "location": "US West - Oregon", "projects": ["System"], "tier": "secondary"},
        {"name": "Control Center Gamma", "type": "control", "location": "EU Central - Frankfurt", "projects": ["System"], "tier": "backup"},

        # 边缘节点 - 制造业
        {"name": "Smart Factory Detroit", "type": "edge", "location": "US Midwest - Detroit", "projects": ["Smart Manufacturing Monitor"], "industry": "Manufacturing"},
        {"name": "Industrial Plant Houston", "type": "edge", "location": "US South - Houston", "projects": ["Smart Manufacturing Monitor"], "industry": "Manufacturing"},
        {"name": "Factory Complex Shanghai", "type": "edge", "location": "Asia Pacific - Shanghai", "projects": ["Smart Manufacturing Monitor"], "industry": "Manufacturing"},

        # 边缘节点 - 交通
        {"name": "Traffic Hub Los Angeles", "type": "edge", "location": "US West - Los Angeles", "projects": ["Urban Traffic Optimization"], "industry": "Transportation"},
        {"name": "Metro Control London", "type": "edge", "location": "EU West - London", "projects": ["Urban Traffic Optimization"], "industry": "Transportation"},
        {"name": "Smart City Singapore", "type": "edge", "location": "Asia Pacific - Singapore", "projects": ["Urban Traffic Optimization"], "industry": "Transportation"},

        # 边缘节点 - 医疗
        {"name": "Medical Center Boston", "type": "edge", "location": "US East - Boston", "projects": ["Medical Image Diagnosis"], "industry": "Healthcare"},
        {"name": "Hospital Network Berlin", "type": "edge", "location": "EU Central - Berlin", "projects": ["Medical Image Diagnosis"], "industry": "Healthcare"},
        {"name": "Healthcare Tokyo", "type": "edge", "location": "Asia Pacific - Tokyo", "projects": ["Medical Image Diagnosis"], "industry": "Healthcare"},

        # 边缘节点 - 金融
        {"name": "Financial District NYC", "type": "edge", "location": "US East - New York", "projects": ["Financial Fraud Detection"], "industry": "Finance"},
        {"name": "Banking Hub Zurich", "type": "edge", "location": "EU West - Zurich", "projects": ["Financial Fraud Detection"], "industry": "Finance"},
        {"name": "FinTech Center Hong Kong", "type": "edge", "location": "Asia Pacific - Hong Kong", "projects": ["Financial Fraud Detection"], "industry": "Finance"},

        # 边缘节点 - 零售
        {"name": "Retail Analytics Seattle", "type": "edge", "location": "US West - Seattle", "projects": ["Retail Customer Analytics"], "industry": "Retail"},
        {"name": "Shopping District Milan", "type": "edge", "location": "EU South - Milan", "projects": ["Retail Customer Analytics"], "industry": "Retail"},
        {"name": "E-commerce Hub Seoul", "type": "edge", "location": "Asia Pacific - Seoul", "projects": ["Retail Customer Analytics"], "industry": "Retail"},

        # 边缘节点 - 农业
        {"name": "AgriTech Farm Iowa", "type": "edge", "location": "US Midwest - Iowa", "projects": ["Smart Agriculture Monitor"], "industry": "Agriculture"},
        {"name": "Smart Farm Netherlands", "type": "edge", "location": "EU West - Amsterdam", "projects": ["Smart Agriculture Monitor"], "industry": "Agriculture"},
        {"name": "Precision Farm Australia", "type": "edge", "location": "Asia Pacific - Sydney", "projects": ["Smart Agriculture Monitor"], "industry": "Agriculture"}
    ]

    statuses = ["online", "offline", "training", "idle", "error"]
    nodes = []

    for i, template in enumerate(node_templates):
        # 动态状态分配
        status = random.choice(statuses)

        # 根据状态设置资源使用率
        if status == "training":
            cpu_usage = random.uniform(60, 95)
            memory_usage = random.uniform(50, 90)
            gpu_usage = random.uniform(70, 95) if template["type"] == "edge" else 0
            progress = random.uniform(1, 99)
            current_epoch = int(progress) if progress > 0 else None
            total_epochs = random.randint(100, 300) if current_epoch else None
        elif status == "online":
            cpu_usage = random.uniform(15, 50)
            memory_usage = random.uniform(20, 60)
            gpu_usage = random.uniform(0, 30) if template["type"] == "edge" else 0
            progress = 0.0
            current_epoch = None
            total_epochs = None
        elif status == "idle":
            cpu_usage = random.uniform(5, 25)
            memory_usage = random.uniform(10, 40)
            gpu_usage = 0.0
            progress = 0.0
            current_epoch = None
            total_epochs = None
        elif status == "error":
            cpu_usage = 0.0
            memory_usage = random.uniform(5, 20)
            gpu_usage = 0.0
            progress = random.uniform(0, 50)  # 中断的进度
            current_epoch = int(progress) if progress > 0 else None
            total_epochs = random.randint(100, 300) if current_epoch else None
        else:  # offline
            cpu_usage = 0.0
            memory_usage = 0.0
            gpu_usage = 0.0
            progress = 0.0
            current_epoch = None
            total_epochs = None

        # 最后在线时间
        if status == "offline" or status == "error":
            last_seen_minutes = random.randint(30, 1440)  # 30分钟到24小时前
            if last_seen_minutes < 60:
                last_seen = f"{last_seen_minutes} minutes ago"
            else:
                hours = last_seen_minutes // 60
                last_seen = f"{hours} hours ago"
        else:
            last_seen_seconds = random.randint(1, 300)  # 1秒到5分钟前
            if last_seen_seconds < 60:
                last_seen = f"{last_seen_seconds} seconds ago"
            else:
                minutes = last_seen_seconds // 60
                last_seen = f"{minutes} minutes ago"

        # 连接信息
        if template["type"] == "control":
            # 控制节点连接到其他边缘节点
            connections = [f"edge-{j+1}" for j in range(random.randint(3, 8))]
        else:
            # 边缘节点连接到控制节点
            connections = ["control-1"] if status != "offline" and status != "error" else []

        node = {
            "id": f"{template['type']}-{i+1}",
            "name": template["name"],
            "type": template["type"],
            "status": status,
            "project": random.choice(template["projects"]) if template["projects"] else None,
            "location": template["location"],
            "industry": template.get("industry", "System"),
            "tier": template.get("tier", "standard"),
            "cpu_usage": round(cpu_usage, 1),
            "memory_usage": round(memory_usage, 1),
            "gpu_usage": round(gpu_usage, 1),
            "progress": round(progress, 1),
            "current_epoch": current_epoch,
            "total_epochs": total_epochs,
            "last_seen": last_seen,
            "connections": connections,
            "uptime": random.uniform(85.5, 99.9) if status != "offline" else 0.0,
            "network_latency": random.randint(5, 150) if status == "online" or status == "training" else None,
            "hardware_info": {
                "cpu_cores": random.choice([4, 8, 16, 32]),
                "memory_gb": random.choice([8, 16, 32, 64, 128]),
                "gpu_model": random.choice(["RTX 4090", "A100", "V100", "RTX 3080", "GTX 1080"]) if template["type"] == "edge" else None,
                "storage_gb": random.choice([256, 512, 1024, 2048])
            }
        }
        nodes.append(node)

    return nodes

# 生成初始节点数据
mock_nodes = generate_dynamic_nodes()

@router.get("/", response_model=List[NodeResponse])
async def get_nodes(
    status: Optional[NodeStatus] = None,
    node_type: Optional[NodeType] = None,
    project: Optional[str] = None
):
    """
    获取节点列表
    支持按状态、类型和项目过滤
    """
    filtered_nodes = mock_nodes
    
    if status:
        filtered_nodes = [n for n in filtered_nodes if n["status"] == status.value]
    
    if node_type:
        filtered_nodes = [n for n in filtered_nodes if n["type"] == node_type.value]
    
    if project:
        filtered_nodes = [n for n in filtered_nodes if n["project"] == project]
    
    return [NodeResponse(**node) for node in filtered_nodes]

@router.get("/{node_id}", response_model=NodeResponse)
async def get_node(node_id: str):
    """
    获取特定节点详情
    """
    for node in mock_nodes:
        if node["id"] == node_id:
            return NodeResponse(**node)
    
    raise HTTPException(status_code=404, detail="Node not found")

@router.post("/{node_id}/operation", response_model=BaseResponse)
async def perform_node_operation(node_id: str, request: NodeOperationRequest):
    """
    执行节点操作
    """
    for node in mock_nodes:
        if node["id"] == node_id:
            if request.operation == "start":
                node["status"] = "online"
                node["cpu_usage"] = 25.0
                node["memory_usage"] = 30.0
                node["last_seen"] = "just now"
            elif request.operation == "stop":
                node["status"] = "offline"
                node["cpu_usage"] = 0.0
                node["memory_usage"] = 0.0
                node["gpu_usage"] = 0.0
            elif request.operation == "restart":
                node["status"] = "online"
                node["cpu_usage"] = 20.0
                node["memory_usage"] = 25.0
                node["gpu_usage"] = 0.0
                node["last_seen"] = "just now"
            elif request.operation == "assign" and request.project_id:
                node["project"] = request.project_id
            
            return BaseResponse(
                success=True,
                message=f"Node {node_id} {request.operation} operation completed"
            )
    
    raise HTTPException(status_code=404, detail="Node not found")

@router.post("/{node_id}/start-training", response_model=BaseResponse)
async def start_node_training(node_id: str):
    """
    启动节点训练
    """
    for node in mock_nodes:
        if node["id"] == node_id:
            if node["status"] != "online":
                raise HTTPException(status_code=400, detail="Node must be online to start training")
            
            node["status"] = "training"
            node["cpu_usage"] = 75.0
            node["memory_usage"] = 68.0
            node["gpu_usage"] = 85.0
            node["progress"] = 0.0
            node["current_epoch"] = 0
            node["total_epochs"] = 100
            node["last_seen"] = "just now"
            
            return BaseResponse(
                success=True,
                message=f"Training started on node {node_id}"
            )
    
    raise HTTPException(status_code=404, detail="Node not found")

@router.post("/{node_id}/stop-training", response_model=BaseResponse)
async def stop_node_training(node_id: str):
    """
    停止节点训练
    """
    for node in mock_nodes:
        if node["id"] == node_id:
            if node["status"] != "training":
                raise HTTPException(status_code=400, detail="Node is not currently training")
            
            node["status"] = "idle"
            node["cpu_usage"] = 15.0
            node["memory_usage"] = 25.0
            node["gpu_usage"] = 0.0
            node["last_seen"] = "just now"
            
            return BaseResponse(
                success=True,
                message=f"Training stopped on node {node_id}"
            )
    
    raise HTTPException(status_code=404, detail="Node not found")

@router.post("/{node_id}/restart", response_model=BaseResponse)
async def restart_node(node_id: str):
    """
    重启节点
    """
    for node in mock_nodes:
        if node["id"] == node_id:
            node["status"] = "online"
            node["cpu_usage"] = 20.0
            node["memory_usage"] = 25.0
            node["gpu_usage"] = 0.0
            node["last_seen"] = "just now"
            
            return BaseResponse(
                success=True,
                message=f"Node {node_id} restarted successfully"
            )
    
    raise HTTPException(status_code=404, detail="Node not found")

@router.get("/stats/overview")
async def get_node_stats():
    """
    获取节点统计信息
    """
    total_nodes = len(mock_nodes)
    online_nodes = len([n for n in mock_nodes if n["status"] == "online"])
    training_nodes = len([n for n in mock_nodes if n["status"] == "training"])
    idle_nodes = len([n for n in mock_nodes if n["status"] == "idle"])
    error_nodes = len([n for n in mock_nodes if n["status"] == "error"])
    
    return {
        "total_nodes": total_nodes,
        "online_nodes": online_nodes,
        "training_nodes": training_nodes,
        "idle_nodes": idle_nodes,
        "error_nodes": error_nodes,
        "avg_cpu_usage": sum(n["cpu_usage"] for n in mock_nodes) / total_nodes if total_nodes > 0 else 0,
        "avg_memory_usage": sum(n["memory_usage"] for n in mock_nodes) / total_nodes if total_nodes > 0 else 0,
        "avg_gpu_usage": sum(n["gpu_usage"] for n in mock_nodes) / total_nodes if total_nodes > 0 else 0
    }

@router.get("/{node_id}/metrics")
async def get_node_metrics(node_id: str):
    """
    获取节点性能指标
    """
    for node in mock_nodes:
        if node["id"] == node_id:
            return {
                "node_id": node_id,
                "cpu_usage": node["cpu_usage"],
                "memory_usage": node["memory_usage"],
                "gpu_usage": node["gpu_usage"],
                "progress": node["progress"],
                "current_epoch": node["current_epoch"],
                "total_epochs": node["total_epochs"],
                "last_seen": node["last_seen"],
                "status": node["status"]
            }
    
    raise HTTPException(status_code=404, detail="Node not found")

@router.websocket("/ws/{node_id}")
async def node_websocket(websocket: WebSocket, node_id: str):
    """
    节点实时监控WebSocket
    """
    await websocket.accept()
    
    try:
        while True:
            # 查找指定节点
            node = None
            for n in mock_nodes:
                if n["id"] == node_id:
                    node = n
                    break
            
            if not node:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Node not found"
                }))
                break
            
            # 模拟实时数据更新
            if node["status"] == "training":
                # 模拟训练进度更新
                if node["progress"] < 100:
                    node["progress"] += 1.0
                    if node["current_epoch"] is not None:
                        node["current_epoch"] = int(node["progress"])
                
                # 模拟资源使用率变化
                node["cpu_usage"] = max(50, min(95, node["cpu_usage"] + (0.5 - 0.1)))
                node["memory_usage"] = max(40, min(90, node["memory_usage"] + (0.3 - 0.1)))
                if node["gpu_usage"] > 0:
                    node["gpu_usage"] = max(60, min(95, node["gpu_usage"] + (0.4 - 0.1)))
            
            # 发送更新数据
            await websocket.send_text(json.dumps({
                "type": "node_update",
                "node_id": node_id,
                "data": {
                    "status": node["status"],
                    "cpu_usage": node["cpu_usage"],
                    "memory_usage": node["memory_usage"],
                    "gpu_usage": node["gpu_usage"],
                    "progress": node["progress"],
                    "current_epoch": node["current_epoch"],
                    "total_epochs": node["total_epochs"],
                    "last_seen": node["last_seen"]
                }
            }))
            
            await asyncio.sleep(2)  # 每2秒发送一次更新
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for node {node_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

@router.post("/{node_id}/assign-project")
async def assign_node_to_project(node_id: str, project_id: str):
    """
    将节点分配到项目
    """
    for node in mock_nodes:
        if node["id"] == node_id:
            node["project"] = project_id
            return BaseResponse(
                success=True,
                message=f"Node {node_id} assigned to project {project_id}"
            )

    raise HTTPException(status_code=404, detail="Node not found")

@router.get("/visualization/{project_id}/")
async def get_visualization_nodes(project_id: str):
    """
    获取特定项目的可视化节点数据
    """
    # 为可视化生成联邦学习节点网络
    visualization_nodes = []

    # 模型/控制节点
    control_nodes = [
        {
            "id": "model-1",
            "name": "Global Model Server",
            "type": "model",
            "status": "online",
            "role": "Model Aggregator",
            "user": "System Administrator",
            "ip_address": "192.168.1.100",
            "connected_nodes": "15 nodes",
            "last_heartbeat": "1 second ago",
            "resources": {
                "cpu": 45,
                "memory": "8.5",
                "gpu": 0
            },
            "priority": 10
        },
        {
            "id": "model-2",
            "name": "Backup Model Server",
            "type": "model",
            "status": "online",
            "role": "Backup Aggregator",
            "user": "System Administrator",
            "ip_address": "192.168.1.101",
            "connected_nodes": "8 nodes",
            "last_heartbeat": "2 seconds ago",
            "resources": {
                "cpu": 35,
                "memory": "6.2",
                "gpu": 0
            },
            "priority": 9
        },
        {
            "id": "backup-control",
            "name": "Coordination Center",
            "type": "control",
            "status": "online",
            "role": "Network Coordinator",
            "user": "Network Admin",
            "ip_address": "192.168.1.102",
            "connected_nodes": "23 nodes",
            "last_heartbeat": "1 second ago",
            "resources": {
                "cpu": 25,
                "memory": "4.1",
                "gpu": 0
            },
            "priority": 8
        }
    ]

    # 训练节点（根据项目动态生成）
    training_node_templates = [
        {"base_name": "Manufacturing Edge", "location": "Factory Floor", "specialty": "Quality Control"},
        {"base_name": "Logistics Hub", "location": "Distribution Center", "specialty": "Inventory Management"},
        {"base_name": "Retail Analytics", "location": "Store Network", "specialty": "Customer Behavior"},
        {"base_name": "Smart City Node", "location": "Urban Infrastructure", "specialty": "Traffic Management"},
        {"base_name": "Healthcare Terminal", "location": "Medical Center", "specialty": "Diagnostic Imaging"},
        {"base_name": "Financial Edge", "location": "Banking System", "specialty": "Fraud Detection"},
        {"base_name": "IoT Gateway", "location": "Sensor Network", "specialty": "Environmental Monitoring"},
        {"base_name": "Mobile Edge", "location": "Base Station", "specialty": "Network Optimization"},
        {"base_name": "Research Lab", "location": "University", "specialty": "Model Training"},
        {"base_name": "Cloud Edge", "location": "Data Center", "specialty": "Distributed Computing"},
        {"base_name": "Agricultural Node", "location": "Smart Farm", "specialty": "Crop Monitoring"},
        {"base_name": "Energy Grid", "location": "Power Station", "specialty": "Load Balancing"},
        {"base_name": "Transportation Hub", "location": "Port Authority", "specialty": "Logistics Tracking"},
        {"base_name": "Emergency Response", "location": "Public Safety", "specialty": "Incident Detection"},
        {"base_name": "Entertainment System", "location": "Media Center", "specialty": "Content Recommendation"},
        {"base_name": "Security Monitor", "location": "Surveillance Network", "specialty": "Threat Detection"},
        {"base_name": "Weather Station", "location": "Meteorological Center", "specialty": "Climate Prediction"},
        {"base_name": "Autonomous Vehicle", "location": "Transport Network", "specialty": "Route Optimization"},
        {"base_name": "Space Station", "location": "Orbital Platform", "specialty": "Satellite Communication"},
        {"base_name": "Deep Sea Monitor", "location": "Ocean Research", "specialty": "Marine Analytics"}
    ]

    # 生成20个训练节点
    import random
    for i in range(20):
        template = training_node_templates[i % len(training_node_templates)]
        node_id = f"training-{str(i+1).zfill(2)}"

        # 随机状态分配
        statuses = ["training", "idle", "completed"]
        weights = [0.6, 0.3, 0.1]  # 60% training, 30% idle, 10% completed
        status = random.choices(statuses, weights=weights)[0]

        # 根据状态设置资源使用率
        if status == "training":
            cpu_usage = random.randint(60, 95)
            memory_usage = round(random.uniform(3.0, 8.0), 1)
            gpu_usage = random.randint(70, 95)
            training_progress = random.randint(1, 99)
        elif status == "completed":
            cpu_usage = random.randint(15, 30)
            memory_usage = round(random.uniform(1.0, 3.0), 1)
            gpu_usage = random.randint(0, 10)
            training_progress = 100
        else:  # idle
            cpu_usage = random.randint(10, 25)
            memory_usage = round(random.uniform(0.5, 2.0), 1)
            gpu_usage = 0
            training_progress = random.randint(0, 30)

        training_node = {
            "id": node_id,
            "name": f"{template['base_name']} {str(i+1).zfill(2)}",
            "type": "training",
            "status": status,
            "role": "Training Participant",
            "user": f"Edge User {i+1}",
            "ip_address": f"192.168.{2 + i//100}.{i%100 + 1}",
            "connected_nodes": "3 nodes",
            "training_progress": training_progress,
            "last_heartbeat": f"{random.randint(1, 30)} seconds ago",
            "resources": {
                "cpu": cpu_usage,
                "memory": str(memory_usage),
                "gpu": gpu_usage
            },
            "priority": random.randint(1, 5),
            "specialty": template["specialty"],
            "location": template["location"]
        }
        visualization_nodes.append(training_node)

    # 合并控制节点和训练节点
    all_nodes = control_nodes + visualization_nodes

    return {
        "nodes": all_nodes,
        "project_id": project_id,
        "total_nodes": len(all_nodes),
        "control_nodes": len(control_nodes),
        "training_nodes": len(visualization_nodes),
        "network_topology": {
            "architecture": "federated_learning",
            "coordination_type": "centralized",
            "communication_protocol": "secure_aggregation"
        },
        "last_updated": "2024-01-15T10:30:00Z"
    }
