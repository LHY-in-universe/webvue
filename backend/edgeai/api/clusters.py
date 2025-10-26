from database.edgeai.models import Node
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from ..schemas.edgeai import (
    ClusterCreateRequest,
    ClusterResponse,
    ClusterUpdateRequest
)
from common.schemas.common import BaseResponse, PaginatedResponse
from database.edgeai import get_db, User, Project, Cluster
from datetime import datetime

router = APIRouter()

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
    启动集群中所有节点的训练任务
    """
    try:
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cluster ID format")
    
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
    
    started_count = 0
    failed_nodes = []
    
    for node in nodes:
        try:
            # 启动节点的训练任务
            node.status = "training"
            node.last_updated_time = datetime.now()
            started_count += 1
        except Exception as e:
            failed_nodes.append({"node_id": str(node.id), "error": str(e)})
    
    db.commit()
    
    if started_count > 0:
        return BaseResponse(
            success=True,
            message=f"Started {started_count} nodes in cluster {cluster.name}"
        )
    else:
        return BaseResponse(
            success=False,
            message="Failed to start any nodes",
            errors=failed_nodes
        )

@router.post("/{cluster_id}/stop", response_model=BaseResponse)
async def stop_cluster(cluster_id: str, db: Session = Depends(get_db)):
    """
    停止指定集群
    停止集群中所有节点的训练任务
    """
    try:
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cluster ID format")
    
    cluster = db.query(Cluster).filter(Cluster.id == cluster_id_int).first()
    if not cluster:
        raise HTTPException(status_code=404, detail=f"Cluster {cluster_id} not found")
    
    # 获取集群中的所有节点
    nodes = db.query(Node).filter(Node.cluster_id == cluster_id_int).all()
    
    stopped_count = 0
    failed_nodes = []
    
    for node in nodes:
        try:
            # 停止节点的训练任务
            if node.status == "training":
                node.status = "idle"
                node.last_updated_time = datetime.now()
                stopped_count += 1
        except Exception as e:
            failed_nodes.append({"node_id": str(node.id), "error": str(e)})
    
    db.commit()
    
    if stopped_count > 0:
        return BaseResponse(
            success=True,
            message=f"Stopped {stopped_count} nodes in cluster {cluster.name}"
        )
    else:
        return BaseResponse(
            success=True,
            message="No active training tasks to stop"
        )

@router.post("/{cluster_id}/restart", response_model=BaseResponse)
async def restart_cluster(cluster_id: str, db: Session = Depends(get_db)):
    """
    重启指定集群
    先停止所有节点，然后重新启动
    """
    import asyncio
    
    try:
        cluster_id_int = int(cluster_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cluster ID format")
    
    cluster = db.query(Cluster).filter(Cluster.id == cluster_id_int).first()
    if not cluster:
        raise HTTPException(status_code=404, detail=f"Cluster {cluster_id} not found")
    
    # 获取集群中的所有节点
    nodes = db.query(Node).filter(Node.cluster_id == cluster_id_int).all()
    
    # 先停止所有节点
    for node in nodes:
        if node.status == "training":
            node.status = "idle"
            node.last_updated_time = datetime.now()
    
    # 等待一下确保状态更新
    await asyncio.sleep(1)
    
    # 重新启动所有节点
    restarted_count = 0
    for node in nodes:
        try:
            node.status = "training"
            node.last_updated_time = datetime.now()
            restarted_count += 1
        except Exception:
            pass
    
    db.commit()
    
    return BaseResponse(
        success=True,
        message=f"Restarted {restarted_count} nodes in cluster {cluster.name}"
    )
