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

# Mock projects database with expanded data
import random
from datetime import datetime, timedelta

def generate_dynamic_projects():
    """生成动态项目数据"""
    project_templates = [
        {
            "name": "Smart Manufacturing Monitor",
            "description": "EdgeAI-based real-time factory equipment monitoring and predictive maintenance system",
            "type": "manufacturing",
            "model_type": "cnn",
            "industry": "Industrial"
        },
        {
            "name": "Urban Traffic Optimization",
            "description": "Intelligent traffic signal control and flow prediction system",
            "type": "traffic",
            "model_type": "rnn",
            "industry": "Transportation"
        },
        {
            "name": "Medical Image Diagnosis",
            "description": "Distributed medical imaging AI diagnostic system for early disease detection",
            "type": "medical",
            "model_type": "transformer",
            "industry": "Healthcare"
        },
        {
            "name": "Retail Customer Analytics",
            "description": "AI-powered customer behavior analysis and inventory optimization system",
            "type": "retail",
            "model_type": "lstm",
            "industry": "Retail"
        },
        {
            "name": "Smart Agriculture Monitor",
            "description": "Precision farming with AI-driven crop monitoring and yield prediction",
            "type": "agriculture",
            "model_type": "cnn",
            "industry": "Agriculture"
        },
        {
            "name": "Financial Fraud Detection",
            "description": "Real-time financial transaction fraud detection using federated learning",
            "type": "finance",
            "model_type": "transformer",
            "industry": "Finance"
        },
        {
            "name": "Energy Grid Optimization",
            "description": "Smart grid energy distribution and consumption optimization system",
            "type": "energy",
            "model_type": "gru",
            "industry": "Energy"
        },
        {
            "name": "Autonomous Vehicle Navigation",
            "description": "Distributed AI system for autonomous vehicle coordination and safety",
            "type": "automotive",
            "model_type": "cnn",
            "industry": "Automotive"
        },
        {
            "name": "Cybersecurity Threat Detection",
            "description": "AI-powered network security monitoring and intrusion detection system",
            "type": "security",
            "model_type": "rnn",
            "industry": "Cybersecurity"
        },
        {
            "name": "Environmental Monitoring System",
            "description": "Large-scale environmental data analysis for climate change research",
            "type": "environment",
            "model_type": "transformer",
            "industry": "Environmental"
        }
    ]

    statuses = ["created", "training", "active", "paused", "completed", "idle"]
    projects = []

    for i, template in enumerate(project_templates):
        # 动态计算时间
        created_days_ago = random.randint(1, 30)
        created_date = datetime.now() - timedelta(days=created_days_ago)

        # 动态状态和进度
        status = random.choice(statuses)
        if status == "completed":
            progress = 100.0
            current_epoch = random.randint(80, 150)
        elif status == "training":
            progress = random.uniform(10, 95)
            current_epoch = int(progress)
        elif status == "active":
            progress = 100.0
            current_epoch = random.randint(100, 200)
        elif status == "paused":
            progress = random.uniform(20, 80)
            current_epoch = int(progress)
        else:  # created, idle
            progress = random.uniform(0, 20)
            current_epoch = int(progress)

        # 动态指标
        base_accuracy = random.uniform(75, 98)
        accuracy_variance = random.uniform(-5, 5)
        current_accuracy = max(0, min(100, base_accuracy + accuracy_variance))

        # 最后更新时间
        last_update_minutes = random.randint(1, 1440)  # 1分钟到24小时前
        if last_update_minutes < 60:
            last_update = f"{last_update_minutes} minutes ago"
        elif last_update_minutes < 1440:
            hours = last_update_minutes // 60
            last_update = f"{hours} hours ago"
        else:
            days = last_update_minutes // 1440
            last_update = f"{days} days ago"

        project = {
            "id": f"proj-{str(i+1).zfill(3)}",
            "name": template["name"],
            "description": template["description"],
            "type": template["type"],
            "industry": template["industry"],
            "status": status,
            "progress": round(progress, 1),
            "connected_nodes": random.randint(3, 25),
            "current_epoch": current_epoch,
            "total_epochs": random.randint(100, 300),
            "model_type": template["model_type"],
            "batch_size": random.choice([16, 32, 64, 128]),
            "learning_rate": random.choice([0.0001, 0.0005, 0.001, 0.005, 0.01]),
            "created": created_date.strftime("%Y-%m-%d"),
            "last_update": last_update,
            "metrics": {
                "accuracy": round(current_accuracy, 1),
                "loss": round(random.uniform(0.05, 0.8), 3),
                "f1_score": round(current_accuracy * random.uniform(0.85, 0.98), 1)
            },
            "estimated_completion": (datetime.now() + timedelta(hours=random.randint(1, 72))).strftime("%Y-%m-%d %H:%M"),
            "resource_usage": {
                "cpu_hours": random.randint(50, 500),
                "gpu_hours": random.randint(20, 200),
                "storage_gb": random.randint(10, 100)
            }
        }
        projects.append(project)

    return projects

# 生成初始项目数据
mock_projects = generate_dynamic_projects()

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

@router.get("/templates")
async def get_project_templates():
    """
    获取项目模板
    """
    templates = [
        {
            "id": "template-001",
            "name": "Manufacturing AI Template",
            "description": "Pre-configured template for manufacturing quality control and predictive maintenance",
            "category": "manufacturing",
            "model_type": "cnn",
            "default_config": {
                "batch_size": 32,
                "learning_rate": 0.001,
                "total_epochs": 100,
                "optimizer": "adam"
            },
            "created_at": "2024-01-10T10:00:00Z",
            "popularity": 95
        },
        {
            "id": "template-002",
            "name": "Traffic Optimization Template",
            "description": "Template for intelligent traffic signal control and flow prediction",
            "category": "traffic",
            "model_type": "rnn",
            "default_config": {
                "batch_size": 64,
                "learning_rate": 0.0001,
                "total_epochs": 150,
                "optimizer": "rmsprop"
            },
            "created_at": "2024-01-08T14:30:00Z",
            "popularity": 87
        },
        {
            "id": "template-003",
            "name": "Medical Diagnosis Template",
            "description": "Template for distributed medical imaging AI diagnostic systems",
            "category": "medical",
            "model_type": "transformer",
            "default_config": {
                "batch_size": 16,
                "learning_rate": 0.0005,
                "total_epochs": 200,
                "optimizer": "adamw"
            },
            "created_at": "2024-01-05T09:15:00Z",
            "popularity": 92
        },
        {
            "id": "template-004",
            "name": "Retail Analytics Template",
            "description": "Customer behavior analysis and inventory optimization template",
            "category": "retail",
            "model_type": "neural_network",
            "default_config": {
                "batch_size": 128,
                "learning_rate": 0.01,
                "total_epochs": 80,
                "optimizer": "sgd"
            },
            "created_at": "2024-01-12T16:45:00Z",
            "popularity": 78
        }
    ]

    return {
        "templates": templates,
        "total": len(templates)
    }

@router.get("/import-history")
async def get_import_history(limit: int = Query(default=20, le=100)):
    """
    获取导入历史记录
    """
    import_history = [
        {
            "id": "import-001",
            "project_name": "Factory Quality Control",
            "source": "file_upload",
            "file_name": "factory_project.zip",
            "file_size": "2.5 MB",
            "status": "success",
            "imported_at": "2024-01-15T10:30:00Z",
            "import_duration": "45 seconds",
            "created_project_id": "proj-001"
        },
        {
            "id": "import-002",
            "project_name": "Traffic Analysis Model",
            "source": "url_config",
            "url": "https://models.example.com/traffic_config.json",
            "status": "success",
            "imported_at": "2024-01-14T15:20:00Z",
            "import_duration": "23 seconds",
            "created_project_id": "proj-002"
        },
        {
            "id": "import-003",
            "project_name": "Medical Imaging Pipeline",
            "source": "file_upload",
            "file_name": "medical_project.tar.gz",
            "file_size": "8.1 MB",
            "status": "failed",
            "imported_at": "2024-01-13T09:45:00Z",
            "import_duration": "12 seconds",
            "error_message": "Invalid model configuration format"
        },
        {
            "id": "import-004",
            "project_name": "Smart Retail System",
            "source": "template",
            "template_id": "template-004",
            "status": "success",
            "imported_at": "2024-01-12T14:10:00Z",
            "import_duration": "8 seconds",
            "created_project_id": "proj-004"
        },
        {
            "id": "import-005",
            "project_name": "IoT Sensor Network",
            "source": "file_upload",
            "file_name": "iot_config.json",
            "file_size": "512 KB",
            "status": "success",
            "imported_at": "2024-01-11T11:25:00Z",
            "import_duration": "15 seconds",
            "created_project_id": "proj-005"
        }
    ]

    # Apply limit
    limited_history = import_history[:limit]

    return {
        "import_history": limited_history,
        "total": len(import_history),
        "showing": len(limited_history)
    }

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

@router.post("/load-from-url")
async def load_project_from_url(request: dict):
    """
    从URL加载项目配置
    """
    url = request.get("url")

    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    # 模拟从URL加载配置
    try:
        # 模拟配置数据
        config_data = {
            "project_name": "Remote Configuration Project",
            "description": f"Project loaded from {url}",
            "model_type": "cnn",
            "training_config": {
                "batch_size": 64,
                "learning_rate": 0.001,
                "total_epochs": 100,
                "optimizer": "adam",
                "loss_function": "categorical_crossentropy"
            },
            "network_architecture": {
                "input_shape": [224, 224, 3],
                "layers": [
                    {"type": "conv2d", "filters": 32, "kernel_size": 3},
                    {"type": "maxpooling2d", "pool_size": 2},
                    {"type": "conv2d", "filters": 64, "kernel_size": 3},
                    {"type": "maxpooling2d", "pool_size": 2},
                    {"type": "flatten"},
                    {"type": "dense", "units": 128, "activation": "relu"},
                    {"type": "dense", "units": 10, "activation": "softmax"}
                ]
            },
            "data_config": {
                "dataset_path": "/data/remote_dataset",
                "validation_split": 0.2,
                "preprocessing": ["normalize", "augment"]
            },
            "loaded_at": "2024-01-15T10:30:00Z",
            "source_url": url
        }

        return BaseResponse(
            success=True,
            message="Configuration loaded successfully from URL",
            data=config_data
        )

    except Exception as e:
        return BaseResponse(
            success=False,
            error=f"Failed to load configuration from URL: {str(e)}"
        )
