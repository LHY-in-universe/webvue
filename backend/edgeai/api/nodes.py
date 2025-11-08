from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends, Request
from typing import List, Optional
from sqlalchemy.orm import Session
from ..schemas.edgeai import (
    NodeResponse,
    NodeOperationRequest,
    NodeStatus,
    NodeType,
    NodeCreateRequest
)
from pydantic import BaseModel
from common.schemas.common import BaseResponse
from common.api.auth import get_current_user_id
from database.edgeai import get_db, User, Project, Model, Node, Cluster
import asyncio
import json
import random
from datetime import datetime, timedelta
import httpx
import logging
import sys
from pathlib import Path

# Add project root to path for config import
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))
from config.remote_api import REMOTE_API_CONFIG, get_remote_api_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class BatchDeleteRequest(BaseModel):
    node_ids: List[str]


# ============ 远程API调用辅助函数 ============

async def call_remote_api(
    endpoint_key: str,
    method: str = "POST",
    json_data: Optional[dict] = None,
    **path_params
) -> Optional[dict]:
    """
    调用远程API的通用函数

    Args:
        endpoint_key: REMOTE_API_CONFIG中的端点键名
        method: HTTP方法
        json_data: 请求体JSON数据
        **path_params: 路径参数

    Returns:
        远程API的响应数据，如果失败返回None
    """
    try:
        url = get_remote_api_url(endpoint_key, **path_params)
        timeout = REMOTE_API_CONFIG["TIMEOUT"]

        logger.info(f"Calling remote API: {method} {url}")
        if json_data:
            logger.debug(f"Request body: {json_data}")

        async with httpx.AsyncClient(timeout=timeout) as client:
            if method.upper() == "GET":
                response = await client.get(url)
            elif method.upper() == "POST":
                response = await client.post(url, json=json_data)
            elif method.upper() == "DELETE":
                response = await client.delete(url, json=json_data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            result = response.json()

            logger.info(f"Remote API response: {response.status_code}")
            logger.debug(f"Response data: {result}")

            return result

    except Exception as e:
        logger.error(f"Failed to call remote API: {e}")
        # 不抛出异常，返回None表示远程API调用失败
        return None


async def sync_nodes_to_remote(node_ips: List[str], cluster_id: int, operation: str) -> bool:
    """
    同步节点变更到远程API

    Args:
        node_ips: 节点IP列表
        cluster_id: 集群ID
        operation: 操作类型 ('add' 或 'remove')

    Returns:
        是否成功
    """
    if not node_ips:
        return True

    try:
        if operation == "add":
            endpoint_key = "CLUSTER_ADD_NODES"
            request_body = {"nodes": node_ips}
        elif operation == "remove":
            endpoint_key = "CLUSTER_REMOVE_NODES"
            request_body = {"nodes": node_ips}
        else:
            logger.error(f"Invalid operation: {operation}")
            return False

        logger.info(f"Syncing {len(node_ips)} nodes to remote API ({operation})")

        result = await call_remote_api(
            endpoint_key=endpoint_key,
            method="POST",
            json_data=request_body
        )

        if result and result.get("success"):
            logger.info(f"Successfully synced {len(node_ips)} nodes to remote ({operation})")
            return True
        else:
            error_msg = result.get("message", "Unknown error") if result else "No response"
            logger.warning(f"Failed to sync nodes to remote: {error_msg}")
            return False

    except Exception as e:
        logger.error(f"Error syncing nodes to remote: {e}")
        return False


@router.get("/", response_model=List[NodeResponse])
async def get_nodes(
    status: Optional[NodeStatus] = None,
    node_type: Optional[NodeType] = None,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    获取节点列表
    支持按状态、类型和项目过滤
    只返回当前用户的节点
    """
    query = db.query(Node).filter(Node.user_id == current_user_id)

    if status:
        query = query.filter(Node.state == status.value)

    if node_type:
        query = query.filter(Node.type == node_type.value)

    nodes = query.all()

    # Convert database nodes to response format
    result = []
    for node in nodes:
        # 计算最后在线时间
        if node.last_updated_time:
            time_diff = datetime.now() - node.last_updated_time
            if time_diff.total_seconds() < 60:
                last_seen = f"{int(time_diff.total_seconds())} seconds ago"
            elif time_diff.total_seconds() < 3600:
                minutes = int(time_diff.total_seconds() / 60)
                last_seen = f"{minutes} minutes ago"
            else:
                hours = int(time_diff.total_seconds() / 3600)
                last_seen = f"{hours} hours ago"
        else:
            last_seen = "never"
        
        # 确定节点类型
        node_type_enum = NodeType.EDGE  # 默认为边缘节点
        if hasattr(node, 'type') and node.type:
            if node.type in ["coordinator", "model"]:
                node_type_enum = NodeType.CONTROL
            elif node.type == "training":
                node_type_enum = NodeType.Training
            elif node.type == "mpc":
                node_type_enum = NodeType.MPC
        
        node_response = NodeResponse(
            id=str(node.id),
            name=node.name,
            type=node_type_enum,
            status=NodeStatus(node.state) if node.state in [s.value for s in NodeStatus] else NodeStatus.OFFLINE,
            location=node.path_ipv4 or "Unknown",
            cpu_usage=float(node.cpu_usage) if node.cpu_usage else 0.0,
            memory_usage=float(node.memory_usage) if node.memory_usage else 0.0,
            gpu_usage=0.0,  # 暂时设为0，后续可以从硬件信息中获取
            progress=float(node.progress) if node.progress else 0.0,
            current_epoch=None,
            total_epochs=None,
            last_seen=last_seen,
            connections=[],
            node_type=node.type,  # 添加节点类型信息
            cluster_id=node.cluster_id,  # 添加集群ID信息
            project="No Project",
            uptime="0h 0m",
            active_tasks=0
        )
        result.append(node_response)

    return result

@router.get("/{node_id}", response_model=NodeResponse)
async def get_node(
    node_id: str, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    获取特定节点详情
    只能访问当前用户的节点
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(
        Node.id == node_id_int,
        Node.user_id == current_user_id
    ).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # 计算最后在线时间
    if node.last_updated_time:
        time_diff = datetime.now() - node.last_updated_time
        if time_diff.total_seconds() < 60:
            last_seen = f"{int(time_diff.total_seconds())} seconds ago"
        elif time_diff.total_seconds() < 3600:
            minutes = int(time_diff.total_seconds() / 60)
            last_seen = f"{minutes} minutes ago"
        else:
            hours = int(time_diff.total_seconds() / 3600)
            last_seen = f"{hours} hours ago"
    else:
        last_seen = "never"
    
    # 确定节点类型
    node_type_enum = NodeType.EDGE  # 默认为边缘节点
    if hasattr(node, 'type') and node.type:
        if node.type in ["coordinator", "model"]:
            node_type_enum = NodeType.CONTROL
        elif node.type == "training":
            node_type_enum = NodeType.Training
        elif node.type == "mpc":
            node_type_enum = NodeType.MPC
    
    return NodeResponse(
        id=str(node.id),
        name=node.name,
        type=node_type_enum,
        status=NodeStatus(node.state) if node.state in [s.value for s in NodeStatus] else NodeStatus.OFFLINE,
        location=node.path_ipv4 or "Unknown",
        cpu_usage=float(node.cpu_usage) if node.cpu_usage else 0.0,
        memory_usage=float(node.memory_usage) if node.memory_usage else 0.0,
        gpu_usage=0.0,  # 暂时设为0，后续可以从硬件信息中获取
        progress=float(node.progress) if node.progress else 0.0,
        current_epoch=None,
        total_epochs=None,
        last_seen=last_seen,
        connections=[],
        node_type=node.type,  # 添加节点类型信息
        cluster_id=node.cluster_id,  # 添加集群ID信息
        project="No Project",
        uptime="0h 0m",
        active_tasks=0
    )

@router.post("/{node_id}/operation", response_model=BaseResponse)
async def perform_node_operation(
    node_id: str, 
    request: NodeOperationRequest, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    执行节点操作
    只能操作当前用户的节点
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(
        Node.id == node_id_int,
        Node.user_id == current_user_id
    ).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    try:
        if request.operation == "start":
            node.state = "online"
            node.cpu_usage = 25.0
            node.memory_usage = 30.0
        elif request.operation == "stop":
            node.state = "offline"
            node.cpu_usage = 0.0
            node.memory_usage = 0.0
        elif request.operation == "restart":
            node.state = "online"
            node.cpu_usage = 20.0
            node.memory_usage = 25.0
        
        # 更新最后更新时间
        node.last_updated_time = datetime.now()
        
        db.commit()
        
        return BaseResponse(
            success=True,
            message=f"Node {node_id} {request.operation} operation completed"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to perform operation: {str(e)}"
        )

@router.post("/{node_id}/start-training", response_model=BaseResponse)
async def start_node_training(
    node_id: str, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    启动节点训练
    只能启动当前用户的节点
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(
        Node.id == node_id_int,
        Node.user_id == current_user_id
    ).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    if node.state != "online":
        raise HTTPException(status_code=400, detail="Node must be online to start training")
    
    try:
        node.state = "training"
        node.cpu_usage = 75.0
        node.memory_usage = 68.0
        node.progress = 0.0
        node.last_updated_time = datetime.now()
        
        db.commit()
        
        return BaseResponse(
            success=True,
            message=f"Training started on node {node_id}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start training: {str(e)}"
        )

@router.post("/{node_id}/stop-training", response_model=BaseResponse)
async def stop_node_training(
    node_id: str, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    停止节点训练
    只能停止当前用户的节点
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(
        Node.id == node_id_int,
        Node.user_id == current_user_id
    ).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    if node.state != "training":
        raise HTTPException(status_code=400, detail="Node is not currently training")
    
    try:
        node.state = "idle"
        node.cpu_usage = 15.0
        node.memory_usage = 25.0
        node.last_updated_time = datetime.now()
        
        db.commit()
        
        return BaseResponse(
            success=True,
            message=f"Training stopped on node {node_id}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to stop training: {str(e)}"
        )

@router.post("/{node_id}/restart", response_model=BaseResponse)
async def restart_node(
    node_id: str, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    重启节点
    只能重启当前用户的节点
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(
        Node.id == node_id_int,
        Node.user_id == current_user_id
    ).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    try:
        node.state = "online"
        node.cpu_usage = 20.0
        node.memory_usage = 25.0
        node.last_updated_time = datetime.now()
        
        db.commit()
        
        return BaseResponse(
            success=True,
            message=f"Node {node_id} restarted successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to restart node: {str(e)}"
        )

@router.get("/stats/overview")
async def get_node_stats(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    获取节点统计信息
    只统计当前用户的节点
    """
    # 获取当前用户的所有节点
    all_nodes = db.query(Node).filter(Node.user_id == current_user_id).all()
    total_nodes = len(all_nodes)
    
    # 统计各状态节点数量
    online_nodes = len([n for n in all_nodes if n.state == "online"])
    training_nodes = len([n for n in all_nodes if n.state == "training"])
    idle_nodes = len([n for n in all_nodes if n.state == "idle"])
    error_nodes = len([n for n in all_nodes if n.state == "error"])
    
    # 计算平均使用率
    if total_nodes > 0:
        avg_cpu_usage = sum(float(n.cpu_usage) for n in all_nodes if n.cpu_usage) / total_nodes
        avg_memory_usage = sum(float(n.memory_usage) for n in all_nodes if n.memory_usage) / total_nodes
        avg_gpu_usage = 0.0  # 暂时设为0，后续可以从硬件信息中获取
    else:
        avg_cpu_usage = 0.0
        avg_memory_usage = 0.0
        avg_gpu_usage = 0.0
    
    return {
        "total_nodes": total_nodes,
        "online_nodes": online_nodes,
        "training_nodes": training_nodes,
        "idle_nodes": idle_nodes,
        "error_nodes": error_nodes,
        "avg_cpu_usage": round(avg_cpu_usage, 1),
        "avg_memory_usage": round(avg_memory_usage, 1),
        "avg_gpu_usage": round(avg_gpu_usage, 1)
    }

@router.get("/{node_id}/metrics")
async def get_node_metrics(
    node_id: str, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    获取节点性能指标
    只能访问当前用户的节点
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(
        Node.id == node_id_int,
        Node.user_id == current_user_id
    ).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # 计算最后在线时间
    if node.last_updated_time:
        time_diff = datetime.now() - node.last_updated_time
        if time_diff.total_seconds() < 60:
            last_seen = f"{int(time_diff.total_seconds())} seconds ago"
        elif time_diff.total_seconds() < 3600:
            minutes = int(time_diff.total_seconds() / 60)
            last_seen = f"{minutes} minutes ago"
        else:
            hours = int(time_diff.total_seconds() / 3600)
            last_seen = f"{hours} hours ago"
    else:
        last_seen = "never"
    
    return {
        "node_id": node_id,
        "cpu_usage": float(node.cpu_usage) if node.cpu_usage else 0.0,
        "memory_usage": float(node.memory_usage) if node.memory_usage else 0.0,
        "gpu_usage": 0.0,  # 暂时设为0，后续可以从硬件信息中获取
        "progress": float(node.progress) if node.progress else 0.0,
        "current_epoch": None,  # 暂时设为None，后续可以从训练信息中获取
        "total_epochs": None,    # 暂时设为None，后续可以从训练信息中获取
        "last_seen": last_seen,
        "status": node.state
    }

@router.websocket("/ws/{node_id}")
async def node_websocket(websocket: WebSocket, node_id: str):
    """
    节点实时监控WebSocket
    """
    await websocket.accept()
    
    try:
        node_id_int = int(node_id)
    except ValueError:
        await websocket.send_text(json.dumps({
            "type": "error",
            "payload": {
                "message": "Invalid node ID format"
            }
        }))
        await websocket.close()
        return
    
    try:
        while True:
            # 从数据库获取节点信息
            from database.edgeai import get_db
            db = next(get_db())
            
            try:
                node = db.query(Node).filter(Node.id == node_id_int).first()
                
                if not node:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "payload": {
                            "message": "Node not found"
                        }
                    }))
                    break
                
                # 计算最后在线时间
                if node.last_updated_time:
                    time_diff = datetime.now() - node.last_updated_time
                    if time_diff.total_seconds() < 60:
                        last_seen = f"{int(time_diff.total_seconds())} seconds ago"
                    elif time_diff.total_seconds() < 3600:
                        minutes = int(time_diff.total_seconds() / 60)
                        last_seen = f"{minutes} minutes ago"
                    else:
                        hours = int(time_diff.total_seconds() / 3600)
                        last_seen = f"{hours} hours ago"
                else:
                    last_seen = "never"
                
                # 发送更新数据，检查连接状态
                try:
                    await websocket.send_text(json.dumps({
                        "type": "node_update",
                        "payload": {
                            "id": node_id,
                            "status": node.state,
                            "cpu_usage": float(node.cpu_usage) if node.cpu_usage else 0.0,
                            "memory_usage": float(node.memory_usage) if node.memory_usage else 0.0,
                            "gpu_usage": 0.0,  # 暂时设为0，后续可以从硬件信息中获取
                            "progress": float(node.progress) if node.progress else 0.0,
                            "current_epoch": None,  # 暂时设为None，后续可以从训练信息中获取
                            "total_epochs": None,    # 暂时设为None，后续可以从训练信息中获取
                            "last_seen": last_seen
                        }
                    }))
                except Exception:
                    # WebSocket已关闭，退出循环
                    break
                
            finally:
                db.close()
            
            await asyncio.sleep(2)  # 每2秒发送一次更新
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for node {node_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except Exception:
            pass  # 连接可能已经关闭

@router.post("/{node_id}/assign-cluster")
async def assign_node_to_cluster(
    node_id: str, 
    cluster_id: str, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    将节点分配到集群并同步到远程API
    """
    try:
        node_id_int = int(node_id)
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID or cluster ID format")
    
    node = db.query(Node).filter(
        Node.id == node_id_int,
        Node.user_id == current_user_id
    ).first()

    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    # 只有空闲或离线节点才可以进入或者退出集群
    if node.state not in ["idle", "offline"]:
        raise HTTPException(status_code=400, detail="Node must be idle or offline to assign to a cluster")

    # 每一个节点只能加入一个集群
    if node.cluster_id is not None:
        raise HTTPException(status_code=400, detail="Node already assigned to a cluster")

    # 检查cluster是否存在
    cluster = db.query(Cluster).filter(Cluster.id == cluster_id_int).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")

    # 集群与主节点是一一对应的关系, 主节点只能属于一个集群
    if node.type == "control":
        cluster_center_node = db.query(Node).filter(Node.cluster_id == cluster_id_int, Node.type == "control").first()
        if cluster_center_node:
            raise HTTPException(status_code=400, detail="Cluster already has a center node")

    try:
        # 将节点分配到cluster
        node.cluster_id = cluster.id
        node.last_updated_time = datetime.now()

        db.commit()

        # 同步到远程API（如果节点有IP地址）
        if node.path_ipv4:
            logger.info(f"Syncing added node {node.path_ipv4} to remote API (cluster {cluster_id})")
            await sync_nodes_to_remote([node.path_ipv4], cluster_id_int, operation="add")

        return BaseResponse(
            success=True,
            message=f"Node {node_id} assigned to cluster {cluster_id}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to assign node to cluster: {str(e)}"
        )

@router.post("/{node_id}/exit-cluster")
async def exit_node_from_cluster(
    node_id: str, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    将节点退出集群并同步到远程API
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(
        Node.id == node_id_int,
        Node.user_id == current_user_id
    ).first()

    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    # 只有空闲或离线节点才可以进入或者退出集群
    if node.state not in ["idle", "offline"]:
        raise HTTPException(status_code=400, detail="Node must be idle or offline to exit from a cluster")

    # 节点必须加入一个集群才可以退出
    if node.cluster_id is None:
        raise HTTPException(status_code=400, detail="Node is not assigned to any cluster")

    # 保存节点信息用于远程同步
    node_ip = node.path_ipv4
    cluster_id = node.cluster_id

    try:
        # 将节点退出集群
        node.cluster_id = None
        node.last_updated_time = datetime.now()

        db.commit()

        # 同步到远程API
        if cluster_id and node_ip:
            logger.info(f"Syncing removed node {node_ip} from remote API (cluster {cluster_id})")
            await sync_nodes_to_remote([node_ip], cluster_id, operation="remove")

        return BaseResponse(
            success=True,
            message=f"Node {node_id} exited from cluster successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to exit node from cluster: {str(e)}"
        )

@router.delete("/batch", response_model=BaseResponse)
async def batch_delete_nodes(
    request: Request, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    批量删除节点并同步到远程API
    """
    try:
        body = await request.json()
        node_ids = body if isinstance(body, list) else body.get('node_ids', [])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request body: {str(e)}")

    if not node_ids:
        raise HTTPException(status_code=400, detail="No node IDs provided")

    deleted_count = 0
    failed_count = 0
    errors = []

    # 用于收集需要同步到远程的节点（按集群分组）
    cluster_nodes_to_sync = {}  # {cluster_id: [node_ips]}

    try:
        for node_id in node_ids:
            try:
                # 确保node_id是字符串且可以转换为整数
                if not isinstance(node_id, str):
                    node_id = str(node_id)

                # 验证node_id格式
                if not node_id.isdigit():
                    failed_count += 1
                    errors.append(f"Invalid node ID format: {node_id} (must be numeric)")
                    continue

                node_id_int = int(node_id)
                node = db.query(Node).filter(Node.id == node_id_int).first()

                if node:
                    # 保存节点信息用于远程同步
                    if node.cluster_id and node.path_ipv4:
                        if node.cluster_id not in cluster_nodes_to_sync:
                            cluster_nodes_to_sync[node.cluster_id] = []
                        cluster_nodes_to_sync[node.cluster_id].append(node.path_ipv4)

                    db.delete(node)
                    deleted_count += 1
                else:
                    failed_count += 1
                    errors.append(f"Node {node_id} not found")
            except ValueError as e:
                failed_count += 1
                errors.append(f"Invalid node ID format: {node_id} - {str(e)}")
            except Exception as e:
                failed_count += 1
                errors.append(f"Error deleting node {node_id}: {str(e)}")

        db.commit()

        # 同步删除的节点到远程API（按集群分组）
        for cluster_id, node_ips in cluster_nodes_to_sync.items():
            logger.info(f"Syncing {len(node_ips)} deleted nodes from cluster {cluster_id} to remote API")
            await sync_nodes_to_remote(node_ips, cluster_id, operation="remove")

        if failed_count > 0:
            return BaseResponse(
                success=False,
                message=f"Batch delete completed with errors. Deleted: {deleted_count}, Failed: {failed_count}",
                error="; ".join(errors)
            )
        else:
            return BaseResponse(
                success=True,
                message=f"Successfully deleted {deleted_count} node(s)"
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to perform batch delete: {str(e)}"
        )

@router.delete("/{node_id}", response_model=BaseResponse)
async def delete_node(
    node_id: str, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    删除节点并同步到远程API
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")

    # 从数据库删除节点
    node = db.query(Node).filter(
        Node.id == node_id_int,
        Node.user_id == current_user_id
    ).first()

    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    # 保存节点信息用于远程同步
    node_ip = node.path_ipv4
    cluster_id = node.cluster_id

    # 从数据库删除节点
    db.delete(node)
    db.commit()

    # 如果节点属于某个集群，同步到远程API
    if cluster_id and node_ip:
        logger.info(f"Syncing deleted node {node_ip} to remote API")
        await sync_nodes_to_remote([node_ip], cluster_id, operation="remove")

    return BaseResponse(
        success=True,
        message=f"Node {node_id} deleted successfully"
    )

@router.get("/visualization/{project_id}/")
async def get_visualization_nodes(
    project_id: str, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    获取特定项目的可视化节点数据（从数据库获取真实数据）
    只能访问当前用户的项目
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    try:
        # 获取项目信息
        project = db.query(Project).filter(
            Project.id == project_id_int,
            Project.user_id == current_user_id
        ).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # 获取项目关联的真实节点数据 - 修复JOIN查询
        project_nodes = []
        try:
            # 先尝试通过cluster关联查询
            project_nodes = db.query(Node).join(Cluster).filter(Cluster.project_id == project_id_int).all()
        except Exception:
            # 如果JOIN失败，直接查询所有节点作为fallback
            project_nodes = db.query(Node).all()

        # 获取项目关联的模型数据
        project_models = []
        try:
            project_models = db.query(Model).filter(Model.project_id == project_id_int).all()
        except Exception:
            # 如果模型查询失败，使用空列表
            project_models = []

        # 构建可视化节点数据
        visualization_nodes = []

        # 添加真实的数据库节点
        for node in project_nodes:
            try:
                visualization_nodes.append({
                    "id": f"node-{node.id}",
                    "name": node.name or f"Node {node.id}",
                    "type": "training",
                    "status": node.state or "idle",
                    "role": node.role or "worker",
                    "user": "EdgeAI System",
                    "ip_address": node.path_ipv4 or "Unknown",
                    "connected_nodes": f"{len(project_nodes)} nodes",
                    "last_heartbeat": "1 second ago",
                    "resources": {
                        "cpu": int(float(node.progress)) if node.progress else 0,
                        "memory": node.memory or "Unknown",
                        "gpu": node.gpu or "None"
                    },
                    "priority": 7,
                    "progress": float(node.progress) if node.progress else 0,
                    "hardware": {
                        "cpu_model": node.cpu or "Unknown",
                        "gpu_model": node.gpu or "None",
                        "memory_size": node.memory or "Unknown"
                    }
                })
            except Exception as e:
                # 如果单个节点处理失败，跳过该节点
                print(f"Error processing node {node.id}: {str(e)}")
                continue

        # 基于真实模型数据添加模型服务器节点
        control_nodes = []
        for i, model in enumerate(project_models):
            try:
                control_nodes.append({
                    "id": f"model-{model.id}",
                    "name": f"{model.name or 'Model'} Server",
                    "type": "model",
                    "status": model.status or "idle",
                    "role": "Model Aggregator",
                    "user": "EdgeAI System",
                    "ip_address": f"192.168.1.{100 + i}",
                    "connected_nodes": f"{len(project_nodes)} nodes",
                    "last_heartbeat": "1 second ago",
                    "resources": {
                        "cpu": int(float(model.progress)) if model.progress else 0,
                        "memory": f"{model.size}MB" if model.size else "Unknown",
                        "gpu": 0
                    },
                    "priority": 10 - i,
                    "accuracy": float(model.accuracy) if model.accuracy else 0.0,
                    "version": model.version or "1.0"
                })
            except Exception as e:
                # 如果单个模型处理失败，跳过该模型
                print(f"Error processing model {model.id}: {str(e)}")
                continue

        # 合并所有节点
        all_nodes = control_nodes + visualization_nodes

        return {
            "nodes": all_nodes,
            "project_id": project_id,
            "project_name": project.name or f"Project {project_id}",
            "total_nodes": len(all_nodes),
            "control_nodes": len(control_nodes),
            "training_nodes": len(visualization_nodes),
            "network_topology": {
                "architecture": "federated_learning",
                "coordination_type": "centralized",
                "communication_protocol": "secure_aggregation"
            },
            "last_updated": project.updated_time.isoformat() if project.updated_time else project.created_time.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get visualization nodes: {str(e)}"
        )

@router.post("/", response_model=NodeResponse)
async def create_node(
    node_data: NodeCreateRequest,
    cluster_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    创建新节点
    """
    try:
        # 检查IP地址是否已存在
        existing_node = db.query(Node).filter(Node.path_ipv4 == node_data.ip).first()
        if existing_node:
            raise HTTPException(
                status_code=400,
                detail=f"Node with IP address {node_data.ip} already exists"
            )

        # 验证节点类型
        valid_types = ["center", "mpc", "training"]
        if node_data.node_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid node type. Must be one of: {', '.join(valid_types)}"
            )

        new_node = Node(
            user_id=current_user_id,  # 使用认证用户的ID
            cluster_id=cluster_id,  # 关联到cluster
            path_ipv4=node_data.ip,
            name=node_data.name or f"{node_data.node_type.title()} Node {node_data.ip}",
            state="idle",  # 默认为空闲状态
            type=node_data.node_type,  # 使用指定的节点类型
            progress=0.0,
            cpu="",
            gpu="",
            memory=""
        )

        db.add(new_node)
        db.commit()
        db.refresh(new_node)

        # 返回节点响应
        return NodeResponse(
            id=str(new_node.id),
            name=new_node.name,
            type=NodeType.EDGE,  # 默认为边缘节点类型
            status=NodeStatus(new_node.state) if new_node.state in [s.value for s in NodeStatus] else NodeStatus.OFFLINE,
            location=new_node.path_ipv4 or "Unknown",
            cpu_usage=0.0,
            memory_usage=0.0,
            gpu_usage=0.0,
            progress=float(new_node.progress) if new_node.progress else 0.0,
            current_epoch=None,
            total_epochs=None,
            last_seen=datetime.now().isoformat(),
            connections=[],
            node_type=new_node.type,
            cluster_id=new_node.cluster_id,  # 添加集群ID信息
            project="No Project",
            uptime="0h 0m",
            active_tasks=0
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create node: {str(e)}"
        )


@router.post("/validate", response_model=BaseResponse)
async def validate_nodes(request: Request, db: Session = Depends(get_db)):
    """
    验证节点IP是否可用（通过远程API）

    请求体格式:
    {
        "node_ips": ["192.168.1.100", "192.168.1.101"]
    }

    返回格式:
    {
        "success": true,
        "message": "2 nodes validated",
        "data": {
            "valid_nodes": ["192.168.1.100"],
            "invalid_nodes": ["192.168.1.101"],
            "details": {
                "192.168.1.100": {"status": "available", "message": "Node is reachable"},
                "192.168.1.101": {"status": "unavailable", "message": "Node is not reachable"}
            }
        }
    }
    """
    try:
        body = await request.json()
        node_ips = body.get('node_ips', [])

        if not node_ips:
            raise HTTPException(status_code=400, detail="No node IPs provided")

        if not isinstance(node_ips, list):
            raise HTTPException(status_code=400, detail="node_ips must be a list")

        logger.info(f"Validating {len(node_ips)} nodes: {node_ips}")

        # 调用远程API验证节点
        request_body = {"nodes": node_ips}

        result = await call_remote_api(
            endpoint_key="CLUSTER_VALIDATE_NODES",
            method="POST",
            json_data=request_body
        )

        if not result:
            # 如果远程API调用失败，返回默认响应
            logger.warning("Remote API validation failed, returning default response")
            return BaseResponse(
                success=False,
                message="Failed to validate nodes via remote API",
                data={
                    "valid_nodes": [],
                    "invalid_nodes": node_ips,
                    "details": {ip: {"status": "unknown", "message": "Remote API unavailable"} for ip in node_ips}
                }
            )

        # 解析远程API响应
        valid_nodes = result.get("valid_nodes", [])
        invalid_nodes = result.get("invalid_nodes", [])
        details = result.get("details", {})

        logger.info(f"Validation result: {len(valid_nodes)} valid, {len(invalid_nodes)} invalid")

        return BaseResponse(
            success=True,
            message=f"Validated {len(node_ips)} nodes: {len(valid_nodes)} valid, {len(invalid_nodes)} invalid",
            data={
                "valid_nodes": valid_nodes,
                "invalid_nodes": invalid_nodes,
                "details": details
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating nodes: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to validate nodes: {str(e)}"
        )


