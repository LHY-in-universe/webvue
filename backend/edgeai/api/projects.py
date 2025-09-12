from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..schemas.edgeai import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectImportRequest,
    ProjectExportRequest,
    SystemStats,
    ProjectStatus,
    ProjectType
)
from common.schemas.common import BaseResponse, PaginatedResponse
import uuid

router = APIRouter()

# Mock projects database
mock_projects = [
    {
        "id": "proj-001",
        "name": "Smart Manufacturing Monitor",
        "description": "EdgeAI-based real-time factory equipment monitoring and predictive maintenance system",
        "type": "manufacturing",
        "status": "training",
        "progress": 65.0,
        "connected_nodes": 8,
        "current_epoch": 65,
        "total_epochs": 100,
        "model_type": "cnn",
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
        "id": "proj-002",
        "name": "Urban Traffic Optimization",
        "description": "Intelligent traffic signal control and flow prediction system",
        "type": "traffic",
        "status": "active",
        "progress": 100.0,
        "connected_nodes": 15,
        "current_epoch": 100,
        "total_epochs": 100,
        "model_type": "rnn",
        "batch_size": 64,
        "learning_rate": 0.0001,
        "created": "2024-01-10",
        "last_update": "30 minutes ago",
        "metrics": {
            "accuracy": 92.1,
            "loss": 0.156,
            "f1_score": 90.8
        }
    },
    {
        "id": "proj-003",
        "name": "Medical Image Diagnosis",
        "description": "Distributed medical imaging AI diagnostic system",
        "type": "medical",
        "status": "paused",
        "progress": 45.0,
        "connected_nodes": 5,
        "current_epoch": 45,
        "total_epochs": 100,
        "model_type": "transformer",
        "batch_size": 16,
        "learning_rate": 0.0005,
        "created": "2024-01-08",
        "last_update": "1 day ago",
        "metrics": {
            "accuracy": 78.3,
            "loss": 0.412,
            "f1_score": 76.5
        }
    }
]

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    status: Optional[ProjectStatus] = None,
    project_type: Optional[ProjectType] = None,
    search: Optional[str] = None
):
    """
    获取项目列表
    支持按状态、类型和搜索关键词过滤
    """
    filtered_projects = mock_projects
    
    if status:
        filtered_projects = [p for p in filtered_projects if p["status"] == status.value]
    
    if project_type:
        filtered_projects = [p for p in filtered_projects if p["type"] == project_type.value]
    
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
        "id": f"proj-{uuid.uuid4().hex[:8]}",
        "name": request.name,
        "description": request.description,
        "type": request.type.value,
        "status": "created",
        "progress": 0.0,
        "connected_nodes": 0,
        "current_epoch": 0,
        "total_epochs": 100,
        "model_type": request.model_type.value,
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
                "type": request.type.value,
                "model_type": request.model_type.value,
                "last_update": "just now"
            }
            mock_projects[i] = updated_project
            return ProjectResponse(**updated_project)
    
    raise HTTPException(status_code=404, detail="Project not found")

@router.delete("/{project_id}", response_model=BaseResponse)
async def delete_project(project_id: str):
    """
    删除项目
    """
    global mock_projects
    original_count = len(mock_projects)
    mock_projects = [p for p in mock_projects if p["id"] != project_id]
    
    if len(mock_projects) < original_count:
        return BaseResponse(
            success=True,
            message="Project deleted successfully"
        )
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@router.post("/import", response_model=BaseResponse)
async def import_project(request: ProjectImportRequest):
    """
    导入项目
    """
    try:
        project_id = f"proj-{uuid.uuid4().hex[:8]}"
        
        imported_project = {
            "id": project_id,
            "name": request.project_data.get("name", "Imported Project"),
            "description": request.project_data.get("description", "Imported from external source"),
            "type": request.project_data.get("type", "manufacturing"),
            "status": "imported",
            "progress": 0.0,
            "connected_nodes": 0,
            "current_epoch": 0,
            "total_epochs": 100,
            "model_type": request.project_data.get("model_type", "cnn"),
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
        
        mock_projects.append(imported_project)
        
        return BaseResponse(
            success=True,
            message=f"Project imported successfully: {project_id}"
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            error=str(e)
        )

@router.post("/{project_id}/export", response_model=BaseResponse)
async def export_project(project_id: str, request: ProjectExportRequest):
    """
    导出项目
    """
    for project in mock_projects:
        if project["id"] == project_id:
            export_data = {
                **project,
                "exported_at": "2024-01-15T10:30:00Z",
                "export_format": request.format,
                "include_models": request.include_models,
                "include_data": request.include_data
            }
            
            return BaseResponse(
                success=True,
                message="Project exported successfully",
                data=export_data
            )
    
    raise HTTPException(status_code=404, detail="Project not found")

@router.get("/stats/overview", response_model=SystemStats)
async def get_system_stats():
    """
    获取系统统计信息
    """
    total_projects = len(mock_projects)
    active_projects = len([p for p in mock_projects if p["status"] in ["active", "training"]])
    
    return SystemStats(
        total_projects=total_projects,
        active_projects=active_projects,
        total_nodes=12,  # Mock data
        online_nodes=8,
        training_nodes=3,
        error_nodes=1,
        completion_rate=round((active_projects / total_projects * 100) if total_projects > 0 else 0, 2)
    )

@router.post("/{project_id}/duplicate", response_model=BaseResponse)
async def duplicate_project(project_id: str):
    """
    复制项目
    """
    for project in mock_projects:
        if project["id"] == project_id:
            new_project = {
                **project,
                "id": f"proj-{uuid.uuid4().hex[:8]}",
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
            return BaseResponse(
                success=True,
                message=f"Project duplicated successfully: {new_project['id']}"
            )
    
    raise HTTPException(status_code=404, detail="Project not found")

@router.post("/{project_id}/start", response_model=BaseResponse)
async def start_project(project_id: str):
    """
    启动项目
    """
    for project in mock_projects:
        if project["id"] == project_id:
            project["status"] = "training"
            project["last_update"] = "just now"
            return BaseResponse(
                success=True,
                message=f"Project {project_id} started successfully"
            )
    
    raise HTTPException(status_code=404, detail="Project not found")

@router.post("/{project_id}/pause", response_model=BaseResponse)
async def pause_project(project_id: str):
    """
    暂停项目
    """
    for project in mock_projects:
        if project["id"] == project_id:
            project["status"] = "paused"
            project["last_update"] = "just now"
            return BaseResponse(
                success=True,
                message=f"Project {project_id} paused successfully"
            )
    
    raise HTTPException(status_code=404, detail="Project not found")

@router.post("/{project_id}/stop", response_model=BaseResponse)
async def stop_project(project_id: str):
    """
    停止项目
    """
    for project in mock_projects:
        if project["id"] == project_id:
            project["status"] = "idle"
            project["last_update"] = "just now"
            return BaseResponse(
                success=True,
                message=f"Project {project_id} stopped successfully"
            )
    
    raise HTTPException(status_code=404, detail="Project not found")
