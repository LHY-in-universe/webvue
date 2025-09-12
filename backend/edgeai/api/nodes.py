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

# Mock nodes database
mock_nodes = [
    {
        "id": "control-1",
        "name": "Control Center",
        "type": "control",
        "status": "online",
        "project": "System",
        "location": "US East",
        "cpu_usage": 35.0,
        "memory_usage": 45.0,
        "gpu_usage": 0.0,
        "progress": 0.0,
        "current_epoch": None,
        "total_epochs": None,
        "last_seen": "1 second ago",
        "connections": ["edge-1", "edge-2", "edge-3"]
    },
    {
        "id": "edge-1",
        "name": "Factory Node A",
        "type": "edge",
        "status": "training",
        "project": "Smart Manufacturing Monitor",
        "location": "US East",
        "cpu_usage": 75.0,
        "memory_usage": 68.0,
        "gpu_usage": 85.0,
        "progress": 65.0,
        "current_epoch": 65,
        "total_epochs": 100,
        "last_seen": "2 seconds ago",
        "connections": ["control-1"]
    },
    {
        "id": "edge-2",
        "name": "Traffic Hub Central",
        "type": "edge",
        "status": "training",
        "project": "Urban Traffic Optimization",
        "location": "US West",
        "cpu_usage": 82.0,
        "memory_usage": 71.0,
        "gpu_usage": 88.0,
        "progress": 78.0,
        "current_epoch": 78,
        "total_epochs": 100,
        "last_seen": "1 minute ago",
        "connections": ["control-1"]
    },
    {
        "id": "edge-3",
        "name": "Medical Center Node",
        "type": "edge",
        "status": "idle",
        "project": "Medical Image Diagnosis",
        "location": "EU Central",
        "cpu_usage": 15.0,
        "memory_usage": 25.0,
        "gpu_usage": 0.0,
        "progress": 0.0,
        "current_epoch": None,
        "total_epochs": None,
        "last_seen": "30 seconds ago",
        "connections": ["control-1"]
    },
    {
        "id": "edge-4",
        "name": "Retail Analytics Hub",
        "type": "edge",
        "status": "error",
        "project": "Retail Traffic Analysis",
        "location": "Asia Pacific",
        "cpu_usage": 0.0,
        "memory_usage": 0.0,
        "gpu_usage": 0.0,
        "progress": 23.0,
        "current_epoch": 23,
        "total_epochs": 100,
        "last_seen": "2 hours ago",
        "connections": []
    }
]

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
