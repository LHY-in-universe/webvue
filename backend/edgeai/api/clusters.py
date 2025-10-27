from database.edgeai.models import Node
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..schemas.edgeai import (
    ClusterCreateRequest,
    ClusterResponse,
    ClusterUpdateRequest
)
from common.schemas.common import BaseResponse, PaginatedResponse
from database.edgeai import get_db, User, Project, Cluster
from datetime import datetime
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


# ============ 远程API调用工具函数 ============

async def call_remote_cluster_api(
    endpoint_key: str,
    method: str = "POST",
    json_data: Optional[Dict[str, Any]] = None,
    **path_params
) -> Dict[str, Any]:
    """
    调用远程集群API的通用函数

    Args:
        endpoint_key: REMOTE_API_CONFIG中的端点键名
        method: HTTP方法（GET, POST, DELETE等）
        json_data: 请求体JSON数据
        **path_params: 路径参数（如 task_id="abc123"）

    Returns:
        远程API的响应数据

    Raises:
        HTTPException: 当远程API调用失败时
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
                response = await client.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            result = response.json()

            logger.info(f"Remote API response: {response.status_code}")
            logger.debug(f"Response data: {result}")

            return result

    except httpx.TimeoutException as e:
        logger.error(f"Remote API timeout: {e}")
        raise HTTPException(
            status_code=504,
            detail=f"Remote cluster API timeout after {timeout}s"
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"Remote API error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Remote cluster API error: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Remote API request error: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Cannot connect to remote cluster API: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error calling remote API: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to call remote cluster API: {str(e)}"
        )


def classify_nodes_by_type(nodes: List[Node]) -> tuple[Optional[str], List[str], List[str]]:
    """
    根据节点类型分类节点IP

    Args:
        nodes: 节点列表

    Returns:
        (head_node_ip, train_node_ips, mpc_node_ips)
        - head_node_ip: center类型节点的IP（head节点）
        - train_node_ips: training类型节点的IP列表
        - mpc_node_ips: mpc类型节点的IP列表
    """
    head_node = None
    train_nodes = []
    mpc_nodes = []

    for node in nodes:
        node_ip = node.path_ipv4
        if not node_ip:
            logger.warning(f"Node {node.id} ({node.name}) has no IP address, skipping")
            continue

        node_type = node.type.lower() if node.type else ""

        if node_type == 'center':
            if head_node is None:
                head_node = node_ip
                logger.debug(f"Classified node {node.id} as head node: {node_ip}")
            else:
                logger.warning(f"Multiple center nodes found, using first one. Skipping {node_ip}")
        elif node_type == 'training':
            train_nodes.append(node_ip)
            logger.debug(f"Classified node {node.id} as training node: {node_ip}")
        elif node_type == 'mpc':
            mpc_nodes.append(node_ip)
            logger.debug(f"Classified node {node.id} as MPC node: {node_ip}")
        else:
            logger.warning(f"Unknown node type '{node_type}' for node {node.id}, skipping")

    logger.info(f"Node classification: head={head_node}, train={len(train_nodes)}, mpc={len(mpc_nodes)}")

    return head_node, train_nodes, mpc_nodes

@router.get("/", response_model=List[ClusterResponse])
async def get_clusters(
    user_id: Optional[int] = None,
    project_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取集群列表
    支持按用户ID、项目ID和搜索关键词过滤
    """
    query = db.query(Cluster)

    if user_id:
        query = query.filter(Cluster.user_id == user_id)

    if project_id:
        query = query.filter(Cluster.project_id == project_id)

    if search:
        search_term = f"%{search}%"
        query = query.filter(Cluster.name.ilike(search_term))

    clusters = query.all()

    # Convert database clusters to response format
    result = []
    for cluster in clusters:
        cluster_response = ClusterResponse(
            id=str(cluster.id),
            name=cluster.name,
            user_id=cluster.user_id,
            project_id=cluster.project_id,
            created_time=cluster.created_time.isoformat() if cluster.created_time else "",
            last_updated_time=cluster.last_updated_time.isoformat() if cluster.last_updated_time else ""
        )
        result.append(cluster_response)

    return result

@router.get("/{cluster_id}/", response_model=ClusterResponse)
async def get_cluster(cluster_id: str, db: Session = Depends(get_db)):
    """
    获取特定集群详情
    """
    try:
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cluster ID format")

    cluster = db.query(Cluster).filter(Cluster.id == cluster_id_int).first()

    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")

    return ClusterResponse(
        id=str(cluster.id),
        name=cluster.name,
        user_id=cluster.user_id,
        project_id=cluster.project_id,
        created_time=cluster.created_time.isoformat() if cluster.created_time else "",
        last_updated_time=cluster.last_updated_time.isoformat() if cluster.last_updated_time else ""
    )

@router.post("/", response_model=ClusterResponse)
async def create_cluster(request: ClusterCreateRequest, db: Session = Depends(get_db)):
    """
    创建新集群
    """
    # Create new cluster in database
    new_cluster = Cluster(
        name=request.name,
        user_id=1,  # TODO: Get from authenticated user
        project_id=request.project_id
    )

    db.add(new_cluster)
    db.commit()
    db.refresh(new_cluster)

    return ClusterResponse(
        id=str(new_cluster.id),
        name=new_cluster.name,
        user_id=new_cluster.user_id,
        project_id=new_cluster.project_id,
        created_time=new_cluster.created_time.isoformat() if new_cluster.created_time else "",
        last_updated_time=new_cluster.last_updated_time.isoformat() if new_cluster.last_updated_time else ""
    )

@router.put("/{cluster_id}", response_model=ClusterResponse)
async def update_cluster(cluster_id: str, request: ClusterUpdateRequest, db: Session = Depends(get_db)):
    """
    更新集群信息
    """
    try:
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cluster ID format")

    cluster = db.query(Cluster).filter(Cluster.id == cluster_id_int).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")

    # Update cluster fields
    if request.name is not None:
        cluster.name = request.name
    if request.project_id is not None:
        cluster.project_id = request.project_id
    
    cluster.last_updated_time = datetime.now()

    db.commit()
    db.refresh(cluster)

    return ClusterResponse(
        id=str(cluster.id),
        name=cluster.name,
        user_id=cluster.user_id,
        project_id=cluster.project_id,
        created_time=cluster.created_time.isoformat() if cluster.created_time else "",
        last_updated_time=cluster.last_updated_time.isoformat() if cluster.last_updated_time else ""
    )

@router.delete("/{cluster_id}", response_model=BaseResponse)
async def delete_cluster(cluster_id: str, db: Session = Depends(get_db)):
    """
    删除集群
    """
    try:
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cluster ID format")

    cluster = db.query(Cluster).filter(Cluster.id == cluster_id_int).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")

    nodes = db.query(Node).filter(Node.cluster_id == cluster_id_int).all()
    if nodes:
        raise HTTPException(status_code=400, detail="Cluster has nodes, cannot be deleted")

    cluster_name = cluster.name
    db.delete(cluster)
    db.commit()

    return BaseResponse(
        success=True,
        message=f"Cluster '{cluster_name}' deleted successfully"
    )

@router.get("/user/{user_id}/clusters", response_model=List[ClusterResponse])
async def get_user_clusters(user_id: int, db: Session = Depends(get_db)):
    """
    获取特定用户的所有集群
    """
    clusters = db.query(Cluster).filter(Cluster.user_id == user_id).all()

    result = []
    for cluster in clusters:
        cluster_response = ClusterResponse(
            id=str(cluster.id),
            name=cluster.name,
            user_id=cluster.user_id,
            project_id=cluster.project_id,
            created_time=cluster.created_time.isoformat() if cluster.created_time else "",
            last_updated_time=cluster.last_updated_time.isoformat() if cluster.last_updated_time else ""
        )
        result.append(cluster_response)

    return result

@router.get("/project/{project_id}/clusters", response_model=List[ClusterResponse])
async def get_project_clusters(project_id: int, db: Session = Depends(get_db)):
    """
    获取特定项目的所有集群
    """
    clusters = db.query(Cluster).filter(Cluster.project_id == project_id).all()

    result = []
    for cluster in clusters:
        cluster_response = ClusterResponse(
            id=str(cluster.id),
            name=cluster.name,
            user_id=cluster.user_id,
            project_id=cluster.project_id,
            created_time=cluster.created_time.isoformat() if cluster.created_time else "",
            last_updated_time=cluster.last_updated_time.isoformat() if cluster.last_updated_time else ""
        )
        result.append(cluster_response)

    return result

@router.post("/{cluster_id}/start", response_model=BaseResponse)
async def start_cluster(cluster_id: str, db: Session = Depends(get_db)):
    """
    启动指定集群
    通过调用远程API创建Ray集群，并更新本地数据库状态
    """
    try:
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cluster ID format")

    # 查询集群信息
    cluster = db.query(Cluster).filter(Cluster.id == cluster_id_int).first()
    if not cluster:
        raise HTTPException(status_code=404, detail=f"Cluster {cluster_id} not found")

    # 获取集群中的所有节点
    nodes = db.query(Node).filter(Node.cluster_id == cluster_id_int).all()
    if not nodes:
        return BaseResponse(
            success=False,
            message="No nodes in this cluster"
        )

    logger.info(f"Starting cluster {cluster_id} ({cluster.name}) with {len(nodes)} nodes")

    # 分类节点：head节点、训练节点、MPC节点
    head_node, train_nodes, mpc_nodes = classify_nodes_by_type(nodes)

    # 验证必须有head节点
    if not head_node:
        return BaseResponse(
            success=False,
            message="Cannot start cluster: No center (head) node found. Please add a center node first."
        )

    # 构造远程API请求体
    request_body = {
        "node_head": head_node,
        "node_train": train_nodes,
        "node_mpc": mpc_nodes
    }

    logger.info(f"Calling remote API to create Ray cluster with config: {request_body}")

    try:
        # 调用远程API创建集群
        remote_response = await call_remote_cluster_api(
            endpoint_key="CLUSTER_CREATE",
            method="POST",
            json_data=request_body
        )

        # 检查远程API响应
        if remote_response.get("success"):
            # 更新本地数据库状态
            for node in nodes:
                node.state = "online"
                node.last_updated_time = datetime.now()

            db.commit()

            remote_cluster_id = remote_response.get("cluster_id", "")
            node_count = len(train_nodes) + len(mpc_nodes) + 1  # +1 for head node

            logger.info(f"Cluster {cluster_id} started successfully. Remote cluster ID: {remote_cluster_id}")

            return BaseResponse(
                success=True,
                message=f"Cluster '{cluster.name}' started successfully with {node_count} nodes. Remote cluster ID: {remote_cluster_id}"
            )
        else:
            # 远程API返回失败
            error_msg = remote_response.get("message", "Unknown error from remote API")
            errors = remote_response.get("errors", [])

            logger.error(f"Remote API failed to start cluster: {error_msg}")

            return BaseResponse(
                success=False,
                message=f"Failed to start cluster: {error_msg}",
                errors=errors
            )

    except HTTPException as e:
        # 远程API调用异常
        logger.error(f"Failed to call remote API: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error starting cluster: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start cluster: {str(e)}"
        )

@router.post("/{cluster_id}/stop", response_model=BaseResponse)
async def stop_cluster(cluster_id: str, db: Session = Depends(get_db)):
    """
    停止指定集群
    通过调用远程API停止Ray集群，并更新本地数据库状态
    """
    try:
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cluster ID format")

    # 查询集群信息
    cluster = db.query(Cluster).filter(Cluster.id == cluster_id_int).first()
    if not cluster:
        raise HTTPException(status_code=404, detail=f"Cluster {cluster_id} not found")

    # 获取集群中的所有节点
    nodes = db.query(Node).filter(Node.cluster_id == cluster_id_int).all()
    if not nodes:
        return BaseResponse(
            success=True,
            message="No nodes in this cluster to stop"
        )

    logger.info(f"Stopping cluster {cluster_id} ({cluster.name}) with {len(nodes)} nodes")

    # 收集所有节点的IP地址
    node_ips = [node.path_ipv4 for node in nodes if node.path_ipv4]

    if not node_ips:
        return BaseResponse(
            success=False,
            message="No valid node IP addresses found in this cluster"
        )

    # 构造远程API请求体
    request_body = {
        "nodes": node_ips
    }

    logger.info(f"Calling remote API to stop Ray cluster with nodes: {node_ips}")

    try:
        # 调用远程API停止集群
        remote_response = await call_remote_cluster_api(
            endpoint_key="CLUSTER_STOP",
            method="POST",
            json_data=request_body
        )

        # 检查远程API响应
        if remote_response.get("success"):
            # 更新本地数据库状态
            for node in nodes:
                node.state = "idle"
                node.last_updated_time = datetime.now()

            db.commit()

            stopped_count = len(node_ips)
            failed_nodes = remote_response.get("failed_nodes", [])

            logger.info(f"Cluster {cluster_id} stopped successfully. Stopped {stopped_count} nodes.")

            message = f"Cluster '{cluster.name}' stopped successfully. {stopped_count} nodes stopped."
            if failed_nodes:
                message += f" ({len(failed_nodes)} nodes failed to stop)"

            return BaseResponse(
                success=True,
                message=message,
                errors=failed_nodes if failed_nodes else None
            )
        else:
            # 远程API返回失败
            error_msg = remote_response.get("message", "Unknown error from remote API")
            errors = remote_response.get("errors", [])

            logger.error(f"Remote API failed to stop cluster: {error_msg}")

            return BaseResponse(
                success=False,
                message=f"Failed to stop cluster: {error_msg}",
                errors=errors
            )

    except HTTPException as e:
        # 远程API调用异常
        logger.error(f"Failed to call remote API: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error stopping cluster: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to stop cluster: {str(e)}"
        )

@router.post("/{cluster_id}/restart", response_model=BaseResponse)
async def restart_cluster(cluster_id: str, db: Session = Depends(get_db)):
    """
    重启指定集群
    先停止集群，然后重新启动
    通过依次调用stop和start实现
    """
    import asyncio

    try:
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cluster ID format")

    # 验证集群存在
    cluster = db.query(Cluster).filter(Cluster.id == cluster_id_int).first()
    if not cluster:
        raise HTTPException(status_code=404, detail=f"Cluster {cluster_id} not found")

    logger.info(f"Restarting cluster {cluster_id} ({cluster.name})")

    # 步骤1: 停止集群
    try:
        logger.info("Step 1: Stopping cluster")
        stop_result = await stop_cluster(cluster_id, db)

        if not stop_result.success:
            return BaseResponse(
                success=False,
                message=f"Failed to restart cluster: Stop operation failed - {stop_result.message}"
            )

        logger.info("Cluster stopped successfully, waiting 2 seconds before restart...")
        await asyncio.sleep(2)

    except Exception as e:
        logger.error(f"Error stopping cluster during restart: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to stop cluster during restart: {str(e)}"
        )

    # 步骤2: 启动集群
    try:
        logger.info("Step 2: Starting cluster")
        start_result = await start_cluster(cluster_id, db)

        if not start_result.success:
            return BaseResponse(
                success=False,
                message=f"Failed to restart cluster: Start operation failed - {start_result.message}"
            )

        logger.info(f"Cluster {cluster_id} restarted successfully")

        return BaseResponse(
            success=True,
            message=f"Cluster '{cluster.name}' restarted successfully"
        )

    except Exception as e:
        logger.error(f"Error starting cluster during restart: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start cluster during restart: {str(e)}"
        )
