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
from database.edgeai import get_db, User, Project, Model, Node, Cluster
import asyncio
import json
import random
from datetime import datetime, timedelta

router = APIRouter()

class BatchDeleteRequest(BaseModel):
    node_ids: List[str]


@router.get("/", response_model=List[NodeResponse])
async def get_nodes(
    status: Optional[NodeStatus] = None,
    node_type: Optional[NodeType] = None,
    db: Session = Depends(get_db)
):
    """
    获取节点列表
    支持按状态、类型和项目过滤
    """
    query = db.query(Node)

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
async def get_node(node_id: str, db: Session = Depends(get_db)):
    """
    获取特定节点详情
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(Node.id == node_id_int).first()
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
async def perform_node_operation(node_id: str, request: NodeOperationRequest, db: Session = Depends(get_db)):
    """
    执行节点操作
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(Node.id == node_id_int).first()
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
async def start_node_training(node_id: str, db: Session = Depends(get_db)):
    """
    启动节点训练
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(Node.id == node_id_int).first()
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
async def stop_node_training(node_id: str, db: Session = Depends(get_db)):
    """
    停止节点训练
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(Node.id == node_id_int).first()
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
async def restart_node(node_id: str, db: Session = Depends(get_db)):
    """
    重启节点
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(Node.id == node_id_int).first()
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
async def get_node_stats(db: Session = Depends(get_db)):
    """
    获取节点统计信息
    """
    # 获取所有节点
    all_nodes = db.query(Node).all()
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
async def get_node_metrics(node_id: str, db: Session = Depends(get_db)):
    """
    获取节点性能指标
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(Node.id == node_id_int).first()
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
async def assign_node_to_cluster(node_id: str, cluster_id: str, db: Session = Depends(get_db)):
    """
    将节点分配到集群
    """
    try:
        node_id_int = int(node_id)
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID or cluster ID format")
    
    node = db.query(Node).filter(Node.id == node_id_int).first()
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
async def exit_node_from_cluster(node_id: str, db: Session = Depends(get_db)):
    """
    将节点退出集群
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")
    
    node = db.query(Node).filter(Node.id == node_id_int).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    # 只有空闲或离线节点才可以进入或者退出集群
    if node.state not in ["idle", "offline"]:
        raise HTTPException(status_code=400, detail="Node must be idle or offline to exit from a cluster")

    # 节点必须加入一个集群才可以退出
    if node.cluster_id is None:
        raise HTTPException(status_code=400, detail="Node is not assigned to any cluster")
    
    # 检查cluster是否存在
    try:
        # 将节点退出集群
        node.cluster_id = None
        node.last_updated_time = datetime.now()
        
        db.commit()
        
        return BaseResponse(
            success=True,
            message=f"Node {node_id} exited from cluster successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to assign node to cluster: {str(e)}"
        )

@router.delete("/batch", response_model=BaseResponse)
async def batch_delete_nodes(request: Request, db: Session = Depends(get_db)):
    """
    批量删除节点
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
async def delete_node(node_id: str, db: Session = Depends(get_db)):
    """
    删除节点
    """
    try:
        node_id_int = int(node_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid node ID format")

    # 从数据库删除节点
    node = db.query(Node).filter(Node.id == node_id_int).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    db.delete(node)
    db.commit()

    return BaseResponse(
        success=True,
        message=f"Node {node_id} deleted successfully"
    )

@router.get("/visualization/{project_id}/")
async def get_visualization_nodes(project_id: str, db: Session = Depends(get_db)):
    """
    获取特定项目的可视化节点数据（从数据库获取真实数据）
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    try:
        # 获取项目信息
        project = db.query(Project).filter(Project.id == project_id_int).first()
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
    db: Session = Depends(get_db)
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
            user_id=1,  # 默认用户ID，实际应用中应该从认证中获取
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


