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
from common.api.auth import get_current_user_id
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
async def create_cluster(
    request: ClusterCreateRequest, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    创建新集群
    """
    # Create new cluster in database
    new_cluster = Cluster(
        name=request.name,
        user_id=current_user_id,  # 使用认证用户的ID
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
