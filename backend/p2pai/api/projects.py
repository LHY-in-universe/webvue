from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..schemas.training import (
    ProjectCreateRequest, 
    ProjectResponse, 
    SystemStats,
    TrainingType,
    TrainingStatus
)
from common.schemas.common import PaginatedResponse

router = APIRouter()

# Mock projects database
mock_projects = [
    {
        "id": "federated-1",
        "name": "Federated Learning Project A",
        "description": "Standard federated learning with 6 edge nodes for image classification",
        "training_type": "federated",
        "model_type": "cnn",
        "status": "training",
        "progress": 65.0,
        "connected_nodes": 6,
        "current_epoch": 65,
        "total_epochs": 100,
        "batch_size": 32,
        "learning_rate": 0.001,
        "created": "2024-01-15",
        "last_update": "2 hours ago",
        "metrics": {
            "accuracy": 87.5,
            "loss": 0.234,
            "f1_score": 85.2
        }
    },
    {
        "id": "mpc-1",
        "name": "MPC Privacy Training",
        "description": "Secure multi-party computation with cryptographic protection for sensitive data",
        "training_type": "mpc",
        "model_type": "transformer",
        "status": "training",
        "progress": 43.0,
        "connected_nodes": 3,
        "current_epoch": 43,
        "total_epochs": 100,
        "batch_size": 16,
        "learning_rate": 0.0005,
        "created": "2024-01-18",
        "last_update": "1 hour ago",
        "metrics": {
            "accuracy": 78.3,
            "loss": 0.412,
            "f1_score": 76.5
        }
    },
    {
        "id": "local-1",
        "name": "Local Model Training",
        "description": "Standalone training with local data for rapid prototyping",
        "training_type": "local",
        "model_type": "cnn",
        "status": "completed",
        "progress": 100.0,
        "connected_nodes": 1,
        "current_epoch": 100,
        "total_epochs": 100,
        "batch_size": 64,
        "learning_rate": 0.001,
        "created": "2024-01-10",
        "last_update": "3 days ago",
        "metrics": {
            "accuracy": 92.1,
            "loss": 0.156,
            "f1_score": 90.8
        }
    }
]

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    status: Optional[TrainingStatus] = None,
    training_type: Optional[TrainingType] = None,
    search: Optional[str] = None
):
    """
    获取项目列表
    支持按状态、训练类型和搜索关键词过滤
    """
    filtered_projects = mock_projects
    
    if status:
        filtered_projects = [p for p in filtered_projects if p["status"] == status.value]
    
    if training_type:
        filtered_projects = [p for p in filtered_projects if p["training_type"] == training_type.value]
    
    if search:
        search_lower = search.lower()
        filtered_projects = [
            p for p in filtered_projects 
            if search_lower in p["name"].lower() or search_lower in p["description"].lower()
        ]
    
    return [ProjectResponse(**project) for project in filtered_projects]

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """
    获取特定项目详情
    """
    for project in mock_projects:
        if project["id"] == project_id:
            return ProjectResponse(**project)
    
    raise HTTPException(status_code=404, detail="Project not found")

@router.post("/", response_model=ProjectResponse)
async def create_project(request: ProjectCreateRequest):
    """
    创建新项目
    """
    new_project = {
        "id": f"proj-{len(mock_projects) + 1}",
        "name": request.name,
        "description": request.description,
        "training_type": request.training_type.value,
        "model_type": request.model_type.value,
        "status": "created",
        "progress": 0.0,
        "connected_nodes": 0,
        "current_epoch": 0,
        "total_epochs": 100,
        "batch_size": 32,
        "learning_rate": 0.001,
        "created": "2024-01-15",
        "last_update": "just now",
        "metrics": {
            "accuracy": 0.0,
            "loss": 0.0,
            "f1_score": 0.0
        }
    }
    
    mock_projects.append(new_project)
    return ProjectResponse(**new_project)

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, request: ProjectCreateRequest):
    """
    更新项目信息
    """
    for i, project in enumerate(mock_projects):
        if project["id"] == project_id:
            updated_project = {
                **project,
                "name": request.name,
                "description": request.description,
                "training_type": request.training_type.value,
                "model_type": request.model_type.value,
                "last_update": "just now"
            }
            mock_projects[i] = updated_project
            return ProjectResponse(**updated_project)
    
    raise HTTPException(status_code=404, detail="Project not found")

@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """
    删除项目
    """
    global mock_projects
    mock_projects = [p for p in mock_projects if p["id"] != project_id]
    return {"success": True, "message": "Project deleted successfully"}

@router.get("/stats/overview", response_model=SystemStats)
async def get_system_stats():
    """
    获取系统统计信息
    """
    total_projects = len(mock_projects)
    active_projects = len([p for p in mock_projects if p["status"] in ["training", "created"]])
    
    return SystemStats(
        total_projects=total_projects,
        active_projects=active_projects,
        total_nodes=12,  # Mock data
        online_nodes=8,
        training_nodes=3,
        error_nodes=1,
        completion_rate=round((active_projects / total_projects * 100) if total_projects > 0 else 0, 2)
    )

@router.post("/{project_id}/duplicate")
async def duplicate_project(project_id: str):
    """
    复制项目
    """
    for project in mock_projects:
        if project["id"] == project_id:
            new_project = {
                **project,
                "id": f"proj-{len(mock_projects) + 1}",
                "name": f"{project['name']} (Copy)",
                "status": "created",
                "progress": 0.0,
                "current_epoch": 0,
                "connected_nodes": 0,
                "created": "2024-01-15",
                "last_update": "just now",
                "metrics": {
                    "accuracy": 0.0,
                    "loss": 0.0,
                    "f1_score": 0.0
                }
            }
            mock_projects.append(new_project)
            return {"success": True, "project": ProjectResponse(**new_project)}
    
    raise HTTPException(status_code=404, detail="Project not found")
