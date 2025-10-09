from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..schemas.training import NodeInfo
from common.schemas.common import BaseResponse

router = APIRouter()

# Mock nodes database
mock_nodes = [
    {
        "id": "client-001",
        "name": "Client-001",
        "type": "client",
        "status": "online",
        "project": "federated-1",
        "location": "US East",
        "cpu_usage": 35.0,
        "memory_usage": 45.0,
        "gpu_usage": 0.0,
        "progress": 0.0,
        "last_seen": "2 mins ago",
        "connections": ["server-001"]
    },
    {
        "id": "client-002",
        "name": "Client-002",
        "type": "client",
        "status": "online",
        "project": "federated-1",
        "location": "US West",
        "cpu_usage": 42.0,
        "memory_usage": 38.0,
        "gpu_usage": 0.0,
        "progress": 0.0,
        "last_seen": "5 mins ago",
        "connections": ["server-001"]
    },
    {
        "id": "server-001",
        "name": "Server-001",
        "type": "server",
        "status": "online",
        "project": "federated-1",
        "location": "US Central",
        "cpu_usage": 75.0,
        "memory_usage": 68.0,
        "gpu_usage": 85.0,
        "progress": 65.0,
        "last_seen": "1 min ago",
        "connections": ["client-001", "client-002"]
    },
    {
        "id": "mpc-node-001",
        "name": "MPC Node 001",
        "type": "mpc",
        "status": "training",
        "project": "mpc-1",
        "location": "EU Central",
        "cpu_usage": 82.0,
        "memory_usage": 71.0,
        "gpu_usage": 0.0,
        "progress": 43.0,
        "last_seen": "30 seconds ago",
        "connections": ["mpc-node-002", "mpc-node-003"]
    }
]

@router.get("/", response_model=List[NodeInfo])
async def get_nodes(
    status: Optional[str] = None,
    node_type: Optional[str] = None,
    project: Optional[str] = None,
    type: Optional[str] = None  # 添加type参数支持
):
    """
    获取节点列表
    支持按状态、类型和项目过滤
    """
    filtered_nodes = mock_nodes
    
    if status:
        filtered_nodes = [n for n in filtered_nodes if n["status"] == status]
    
    if node_type:
        filtered_nodes = [n for n in filtered_nodes if n["type"] == node_type]
    
    if type:  # 支持type参数
        filtered_nodes = [n for n in filtered_nodes if n["type"] == type]
    
    if project:
        filtered_nodes = [n for n in filtered_nodes if n["project"] == project]
    
    return [NodeInfo(**node) for node in filtered_nodes]

@router.get("/{node_id}", response_model=NodeInfo)
async def get_node(node_id: str):
    """
    获取特定节点详情
    """
    for node in mock_nodes:
        if node["id"] == node_id:
            return NodeInfo(**node)
    
    raise HTTPException(status_code=404, detail="Node not found")

@router.post("/{node_id}/start", response_model=BaseResponse)
async def start_node(node_id: str):
    """
    启动节点
    """
    for node in mock_nodes:
        if node["id"] == node_id:
            node["status"] = "online"
            node["last_seen"] = "just now"
            return BaseResponse(
                success=True,
                message=f"Node {node_id} started successfully"
            )
    
    raise HTTPException(status_code=404, detail="Node not found")

@router.post("/{node_id}/stop", response_model=BaseResponse)
async def stop_node(node_id: str):
    """
    停止节点
    """
    for node in mock_nodes:
        if node["id"] == node_id:
            node["status"] = "offline"
            node["cpu_usage"] = 0.0
            node["memory_usage"] = 0.0
            node["gpu_usage"] = 0.0
            return BaseResponse(
                success=True,
                message=f"Node {node_id} stopped successfully"
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
            node["cpu_usage"] = 25.0
            node["memory_usage"] = 30.0
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
    offline_nodes = len([n for n in mock_nodes if n["status"] == "offline"])
    
    return {
        "total_nodes": total_nodes,
        "online_nodes": online_nodes,
        "training_nodes": training_nodes,
        "offline_nodes": offline_nodes,
        "avg_cpu_usage": sum(n["cpu_usage"] for n in mock_nodes) / total_nodes if total_nodes > 0 else 0,
        "avg_memory_usage": sum(n["memory_usage"] for n in mock_nodes) / total_nodes if total_nodes > 0 else 0
    }

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
                "last_seen": node["last_seen"],
                "status": node["status"]
            }
    
    raise HTTPException(status_code=404, detail="Node not found")
