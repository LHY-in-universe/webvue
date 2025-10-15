from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from ..schemas.edgeai import (
    NodeResponse,
    NodeOperationRequest,
    NodeStatus,
    NodeType,
    NodeCreateRequest
)
from common.schemas.common import BaseResponse
from database.edgeai import get_db, User, Project, Model, Node
import asyncio
import json
import random
from datetime import datetime, timedelta

router = APIRouter()

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
    project: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取节点列表
    支持按状态、类型和项目过滤
    """
    query = db.query(Node)

    if status:
        query = query.filter(Node.state == status.value)

    if project:
        try:
            project_id = int(project)
            query = query.filter(Node.project_id == project_id)
        except ValueError:
            # If project is not a valid ID, ignore the filter
            pass

    nodes = query.all()

    # Convert database nodes to response format
    result = []
    for node in nodes:
        node_response = NodeResponse(
            id=str(node.id),
            name=node.name,
            type=NodeType.EDGE,  # Default type
            status=NodeStatus(node.state) if node.state in [s.value for s in NodeStatus] else NodeStatus.OFFLINE,
            project=str(node.project_id) if node.project_id else None,
            location=node.path_ipv4 or "Unknown",
            cpu_usage=random.uniform(10, 80),  # Mock data for now
            memory_usage=random.uniform(20, 90),
            gpu_usage=random.uniform(0, 100) if node.gpu else 0,
            progress=node.progress,
            current_epoch=None,
            total_epochs=None,
            last_seen=node.last_updated_time.isoformat() if node.last_updated_time else "",
            connections=[]
        )
        result.append(node_response)

    return result

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
                    "payload": {
                        "message": "Node not found"
                    }
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
            
            # 发送更新数据，检查连接状态
            try:
                await websocket.send_text(json.dumps({
                    "type": "node_update",
                    "payload": {
                        "id": node_id,
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
            except Exception:
                # WebSocket已关闭，退出循环
                break
            
            await asyncio.sleep(2)  # 每2秒发送一次更新
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for node {node_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except Exception:
            pass  # 连接可能已经关闭

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

@router.delete("/batch", response_model=BaseResponse)
async def batch_delete_nodes(node_ids: List[str], db: Session = Depends(get_db)):
    """
    批量删除节点
    """
    deleted_count = 0
    failed_count = 0
    errors = []

    for node_id in node_ids:
        try:
            node_id_int = int(node_id)
            node = db.query(Node).filter(Node.id == node_id_int).first()
            
            if node:
                db.delete(node)
                deleted_count += 1
            else:
                failed_count += 1
                errors.append(f"Node {node_id} not found")
        except ValueError:
            failed_count += 1
            errors.append(f"Invalid node ID format: {node_id}")
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

@router.get("/visualization/{project_id}/")
async def get_visualization_nodes(project_id: str, db: Session = Depends(get_db)):
    """
    获取特定项目的可视化节点数据（从数据库获取真实数据）
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    # 获取项目信息
    project = db.query(Project).filter(Project.id == project_id_int).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 获取项目关联的真实节点数据
    project_nodes = db.query(Node).filter(Node.project_id == project_id_int).all()

    # 获取项目关联的模型数据
    project_models = db.query(Model).filter(Model.project_id == project_id_int).all()

    # 构建可视化节点数据
    visualization_nodes = []

    # 添加真实的数据库节点
    for node in project_nodes:
        visualization_nodes.append({
            "id": f"node-{node.id}",
            "name": node.name,  # 这将包含 "(db)" 标识
            "type": "training",
            "status": node.state,  # 应该是 "training"
            "role": node.role,
            "user": "EdgeAI System",
            "ip_address": node.path_ipv4,
            "connected_nodes": f"{len(project_nodes)} nodes",
            "last_heartbeat": "1 second ago",
            "resources": {
                "cpu": int(node.progress) if node.progress else 0,
                "memory": node.memory or "Unknown",
                "gpu": node.gpu or "None"
            },
            "priority": 7,
            "progress": node.progress or 0,
            "hardware": {
                "cpu_model": node.cpu,
                "gpu_model": node.gpu,
                "memory_size": node.memory
            }
        })

    # 基于真实模型数据添加模型服务器节点
    control_nodes = []
    for i, model in enumerate(project_models):
        control_nodes.append({
            "id": f"model-{model.id}",
            "name": f"{model.name} Server",  # 包含 "(db)" 标识
            "type": "model",
            "status": model.status,
            "role": "Model Aggregator",
            "user": "EdgeAI System",
            "ip_address": f"192.168.1.{100 + i}",
            "connected_nodes": f"{len(project_nodes)} nodes",
            "last_heartbeat": "1 second ago",
            "resources": {
                "cpu": int(model.progress) if model.progress else 0,
                "memory": f"{model.size}MB" if model.size else "Unknown",
                "gpu": 0
            },
            "priority": 10 - i,
            "accuracy": model.accuracy,
            "version": model.version
        })

    # 合并所有节点
    all_nodes = control_nodes + visualization_nodes

    return {
        "nodes": all_nodes,
        "project_id": project_id,
        "project_name": project.name,  # 包含 "(db)" 标识
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

@router.post("/", response_model=NodeResponse)
async def create_node(
    node_data: NodeCreateRequest,
    project_id: Optional[int] = None,
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
        
        # 创建新节点
        new_node = Node(
            user_id=1,  # 默认用户ID，实际应用中应该从认证中获取
            project_id=project_id,  # 关联到指定项目
            path_ipv4=node_data.ip,
            name=node_data.name or f"Node {node_data.ip}",
            state="idle",  # 默认为空闲状态
            role="worker",  # 默认为工作节点
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
            type="edge",  # 默认为边缘节点类型
            status=new_node.state,
            project=None,  # 新创建的节点暂时不关联项目
            location="Unknown",
            cpu_usage=0.0,
            memory_usage=0.0,
            gpu_usage=0.0,
            progress=new_node.progress,
            current_epoch=None,
            total_epochs=None,
            last_seen=datetime.now().isoformat(),
            connections=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create node: {str(e)}"
        )
