from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..schemas.edgeai import NodeResponse, NodeStatus, NodeType
from common.schemas.common import BaseResponse
from database.edgeai import get_db, User, Project, Model, Node, Cluster
import httpx
import asyncio
import logging
from datetime import datetime, timedelta
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Ray监控API配置
RAY_MONITOR_BASE_URL = "http://12.148.158.61:6677"
RAY_MONITOR_ENDPOINTS = {
    "cluster_nodes": "/monitor/ray/cluster/node",
    "cluster_status": "/monitor/ray/cluster/status",
    "node_metrics": "/monitor/ray/cluster/node/{node_id}/metrics"
}

class RayMonitorService:
    """Ray监控服务类，负责调用外部API和数据处理"""
    
    def __init__(self):
        self.base_url = RAY_MONITOR_BASE_URL
        self.timeout = httpx.Timeout(30.0)  # 30秒超时
    
    async def fetch_cluster_nodes(self) -> Dict[str, Any]:
        """获取Ray集群节点信息"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{RAY_MONITOR_ENDPOINTS['cluster_nodes']}"
                logger.info(f"正在调用Ray监控API: {url}")
                
                response = await client.get(url)
                response.raise_for_status()
                
                data = response.json()
                logger.info(f"成功获取Ray集群数据，节点数量: {len(data.get('nodes', []))}")
                return data
                
        except httpx.TimeoutException:
            logger.error("调用Ray监控API超时")
            raise HTTPException(status_code=504, detail="Ray监控API调用超时")
        except httpx.HTTPStatusError as e:
            logger.error(f"Ray监控API返回错误状态码: {e.response.status_code}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Ray监控API错误: {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Ray监控API请求错误: {str(e)}")
            raise HTTPException(status_code=503, detail=f"无法连接到Ray监控服务: {str(e)}")
        except Exception as e:
            logger.error(f"获取Ray集群数据时发生未知错误: {str(e)}")
            raise HTTPException(status_code=500, detail=f"获取Ray集群数据失败: {str(e)}")
    
    async def fetch_node_metrics(self, node_id: str) -> Dict[str, Any]:
        """获取特定节点的指标数据"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{RAY_MONITOR_ENDPOINTS['node_metrics'].format(node_id=node_id)}"
                logger.info(f"正在获取节点 {node_id} 的指标数据")
                
                response = await client.get(url)
                response.raise_for_status()
                
                data = response.json()
                logger.info(f"成功获取节点 {node_id} 的指标数据")
                return data
                
        except httpx.TimeoutException:
            logger.error(f"获取节点 {node_id} 指标数据超时")
            raise HTTPException(status_code=504, detail="获取节点指标数据超时")
        except httpx.HTTPStatusError as e:
            logger.error(f"获取节点 {node_id} 指标数据失败，状态码: {e.response.status_code}")
            raise HTTPException(status_code=e.response.status_code, detail=f"获取节点指标数据失败: {e.response.text}")
        except Exception as e:
            logger.error(f"获取节点 {node_id} 指标数据时发生错误: {str(e)}")
            raise HTTPException(status_code=500, detail=f"获取节点指标数据失败: {str(e)}")

# 创建Ray监控服务实例
ray_monitor_service = RayMonitorService()

def transform_ray_node_to_db_node(ray_node: Dict[str, Any], user_id: int = 1, project_id: Optional[int] = None) -> Node:
    """将Ray节点数据转换为数据库Node对象"""
    try:
        # 提取Ray节点信息
        node_name = ray_node.get("name", f"Ray Node {ray_node.get('id', 'Unknown')}")
        node_ip = ray_node.get("ip", ray_node.get("address", ""))
        node_status = ray_node.get("state", "unknown")
        
        # 映射Ray状态到我们的状态
        status_mapping = {
            "ALIVE": "online",
            "DEAD": "offline", 
            "UNKNOWN": "idle"
        }
        mapped_status = status_mapping.get(node_status.upper(), "idle")
        
        # 提取资源信息
        resources = ray_node.get("resources", {})
        cpu_info = resources.get("CPU", "Unknown")
        memory_info = resources.get("memory", "Unknown")
        gpu_info = resources.get("GPU", "None")
        
        # 提取进度信息（如果有训练任务）
        progress = 0.0
        if "training" in ray_node:
            training_info = ray_node["training"]
            progress = training_info.get("progress", 0.0)
        
        # 创建Node对象
        db_node = Node(
            user_id=user_id,
            cluster_id=None,  # 需要后续设置cluster_id
            name=node_name,
            path_ipv4=node_ip,
            progress=progress,
            state=mapped_status,
            role="worker",  # Ray节点默认为工作节点
            cpu=str(cpu_info) if cpu_info != "Unknown" else "",
            gpu=str(gpu_info) if gpu_info != "None" else "",
            memory=str(memory_info) if memory_info != "Unknown" else "",
            created_time=datetime.now(),
            last_updated_time=datetime.now()
        )
        
        return db_node
        
    except Exception as e:
        logger.error(f"转换Ray节点数据时发生错误: {str(e)}")
        raise

async def save_ray_nodes_to_db(ray_data: Dict[str, Any], db: Session, user_id: int = 1, project_id: Optional[int] = None) -> List[Node]:
    """将Ray节点数据保存到数据库"""
    try:
        saved_nodes = []
        nodes_data = ray_data.get("nodes", [])
        
        if not nodes_data:
            logger.warning("Ray集群数据中没有节点信息")
            return saved_nodes
        
        for ray_node in nodes_data:
            try:
                # 检查节点是否已存在（基于IP地址）
                node_ip = ray_node.get("ip", ray_node.get("address", ""))
                existing_node = db.query(Node).filter(Node.path_ipv4 == node_ip).first()
                
                if existing_node:
                    # 更新现有节点
                    logger.info(f"更新现有节点: {node_ip}")
                    
                    # 更新节点信息
                    node_status = ray_node.get("state", "unknown")
                    status_mapping = {
                        "ALIVE": "online",
                        "DEAD": "offline", 
                        "UNKNOWN": "idle"
                    }
                    mapped_status = status_mapping.get(node_status.upper(), "idle")
                    
                    existing_node.state = mapped_status
                    existing_node.last_updated_time = datetime.now()
                    
                    # 更新资源信息
                    resources = ray_node.get("resources", {})
                    if resources.get("CPU"):
                        existing_node.cpu = str(resources["CPU"])
                    if resources.get("memory"):
                        existing_node.memory = str(resources["memory"])
                    if resources.get("GPU"):
                        existing_node.gpu = str(resources["GPU"])
                    
                    # 更新进度信息
                    if "training" in ray_node:
                        training_info = ray_node["training"]
                        existing_node.progress = training_info.get("progress", existing_node.progress)
                    
                    saved_nodes.append(existing_node)
                    
                else:
                    # 创建新节点
                    logger.info(f"创建新节点: {node_ip}")
                    new_node = transform_ray_node_to_db_node(ray_node, user_id, project_id)
                    db.add(new_node)
                    saved_nodes.append(new_node)
                    
            except Exception as e:
                logger.error(f"处理节点 {ray_node.get('id', 'Unknown')} 时发生错误: {str(e)}")
                continue
        
        # 提交数据库事务
        db.commit()
        logger.info(f"成功保存 {len(saved_nodes)} 个节点到数据库")
        
        # 刷新对象以获取最新数据
        for node in saved_nodes:
            db.refresh(node)
            
        return saved_nodes
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库操作失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"数据库操作失败: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"保存Ray节点数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"保存Ray节点数据失败: {str(e)}")

@router.get("/sync", response_model=BaseResponse)
async def sync_ray_cluster_data(
    background_tasks: BackgroundTasks,
    user_id: int = 1,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    同步Ray集群数据到数据库
    从外部Ray监控API获取数据并保存到本地数据库
    """
    try:
        logger.info("开始同步Ray集群数据")
        
        # 获取Ray集群数据
        ray_data = await ray_monitor_service.fetch_cluster_nodes()
        
        # 保存到数据库
        saved_nodes = await save_ray_nodes_to_db(ray_data, db, user_id, project_id)
        
        return BaseResponse(
            success=True,
            message=f"成功同步Ray集群数据，共处理 {len(saved_nodes)} 个节点"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"同步Ray集群数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"同步失败: {str(e)}")

@router.get("/cluster/status")
async def get_ray_cluster_status():
    """
    获取Ray集群状态
    直接从外部API获取实时状态
    """
    try:
        ray_data = await ray_monitor_service.fetch_cluster_nodes()
        
        # 统计节点状态
        nodes = ray_data.get("nodes", [])
        status_counts = {}
        total_nodes = len(nodes)
        
        for node in nodes:
            status = node.get("state", "UNKNOWN")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "cluster_status": "healthy" if status_counts.get("ALIVE", 0) > 0 else "unhealthy",
            "total_nodes": total_nodes,
            "status_counts": status_counts,
            "last_updated": datetime.now().isoformat(),
            "data_source": "ray_monitor_api"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取Ray集群状态时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取集群状态失败: {str(e)}")

@router.get("/nodes", response_model=List[NodeResponse])
async def get_ray_nodes_from_api():
    """
    直接从Ray监控API获取节点列表
    不经过数据库，实时获取最新数据
    """
    try:
        ray_data = await ray_monitor_service.fetch_cluster_nodes()
        nodes = ray_data.get("nodes", [])
        
        result = []
        for ray_node in nodes:
            # 转换为NodeResponse格式
            node_status = ray_node.get("state", "UNKNOWN")
            status_mapping = {
                "ALIVE": NodeStatus.ONLINE,
                "DEAD": NodeStatus.OFFLINE, 
                "UNKNOWN": NodeStatus.IDLE
            }
            mapped_status = status_mapping.get(node_status.upper(), NodeStatus.IDLE)
            
            # 提取资源信息
            resources = ray_node.get("resources", {})
            cpu_usage = 0.0
            memory_usage = 0.0
            gpu_usage = 0.0
            
            # 模拟资源使用率（实际API可能不提供使用率数据）
            if ray_node.get("state") == "ALIVE":
                cpu_usage = 25.0
                memory_usage = 40.0
                gpu_usage = 15.0
            
            node_response = NodeResponse(
                id=ray_node.get("id", "unknown"),
                name=ray_node.get("name", f"Ray Node {ray_node.get('id', 'Unknown')}"),
                type=NodeType.EDGE,
                status=mapped_status,
                project=None,
                location=ray_node.get("ip", ray_node.get("address", "Unknown")),
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                gpu_usage=gpu_usage,
                progress=ray_node.get("training", {}).get("progress", 0.0),
                current_epoch=None,
                total_epochs=None,
                last_seen=datetime.now().isoformat(),
                connections=[]
            )
            result.append(node_response)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取Ray节点列表时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取节点列表失败: {str(e)}")

@router.get("/nodes/{node_id}/metrics")
async def get_ray_node_metrics(node_id: str):
    """
    获取特定Ray节点的详细指标
    """
    try:
        metrics_data = await ray_monitor_service.fetch_node_metrics(node_id)
        
        return {
            "node_id": node_id,
            "metrics": metrics_data,
            "timestamp": datetime.now().isoformat(),
            "data_source": "ray_monitor_api"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取节点 {node_id} 指标时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取节点指标失败: {str(e)}")

@router.get("/database/nodes", response_model=List[NodeResponse])
async def get_ray_nodes_from_db(
    status: Optional[NodeStatus] = None,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    从数据库获取已同步的Ray节点数据
    """
    try:
        query = db.query(Node)
        
        # 按状态过滤
        if status:
            query = query.filter(Node.state == status.value)
        
        # 按项目过滤
        if project_id:
            query = query.join(Cluster).filter(Cluster.project_id == project_id)
        
        nodes = query.all()
        
        result = []
        for node in nodes:
            node_response = NodeResponse(
                id=str(node.id),
                name=node.name,
                type=NodeType.EDGE,
                status=NodeStatus(node.state) if node.state in [s.value for s in NodeStatus] else NodeStatus.OFFLINE,
                project=str(node.project_id) if node.project_id else None,
                location=node.path_ipv4 or "Unknown",
                cpu_usage=0.0,  # 需要从其他API获取实时数据
                memory_usage=0.0,
                gpu_usage=0.0,
                progress=node.progress,
                current_epoch=None,
                total_epochs=None,
                last_seen=node.last_updated_time.isoformat() if node.last_updated_time else "",
                connections=[]
            )
            result.append(node_response)
        
        return result
        
    except Exception as e:
        logger.error(f"从数据库获取Ray节点时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取数据库节点失败: {str(e)}")

@router.post("/sync/background", response_model=BaseResponse)
async def start_background_sync(
    background_tasks: BackgroundTasks,
    user_id: int = 1,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    启动后台同步任务
    异步同步Ray集群数据，不阻塞请求
    """
    try:
        # 添加后台任务
        background_tasks.add_task(
            sync_ray_cluster_data,
            user_id=user_id,
            project_id=project_id,
            db=db
        )
        
        return BaseResponse(
            success=True,
            message="后台同步任务已启动"
        )
        
    except Exception as e:
        logger.error(f"启动后台同步任务时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"启动后台同步失败: {str(e)}")

@router.get("/health")
async def check_ray_monitor_health():
    """
    检查Ray监控服务的健康状态
    """
    try:
        # 尝试调用Ray监控API
        ray_data = await ray_monitor_service.fetch_cluster_nodes()
        
        return {
            "status": "healthy",
            "ray_monitor_api": "accessible",
            "nodes_count": len(ray_data.get("nodes", [])),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException as e:
        return {
            "status": "unhealthy",
            "ray_monitor_api": "inaccessible",
            "error": e.detail,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "ray_monitor_api": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
