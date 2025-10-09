from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from ..schemas.edgeai import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectImportRequest,
    ProjectExportRequest,
    SystemStats,
    ProjectStatus,
    ProjectType,
    TrainingStrategy,
    Protocol
)
from common.schemas.common import BaseResponse, PaginatedResponse
from database.edgeai import get_db, User, Project, Model, Node
import uuid
from datetime import datetime, timedelta

router = APIRouter()

# Mock data generation removed - now using database

def generate_dynamic_projects_OLD():
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

    statuses = [ProjectStatus.CREATED, ProjectStatus.TRAINING, ProjectStatus.ACTIVE, ProjectStatus.PAUSED, ProjectStatus.COMPLETED, ProjectStatus.IDLE]
    projects = []

    for i, template in enumerate(project_templates):
        # 动态计算时间
        created_days_ago = random.randint(1, 30)
        created_date = datetime.now() - timedelta(days=created_days_ago)

        # 动态状态和进度
        status = random.choice(statuses)
        if status == ProjectStatus.COMPLETED:
            progress = 100.0
            current_epoch = random.randint(80, 150)
        elif status == ProjectStatus.TRAINING:
            progress = random.uniform(10, 95)
            current_epoch = int(progress)
        elif status == ProjectStatus.ACTIVE:
            progress = 100.0
            current_epoch = random.randint(100, 200)
        elif status == ProjectStatus.PAUSED:
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
            "model": random.choice(["Gemma", "OpenVLA", "LLaMA", "Qwen"]),
            "status": status,
            "progress": round(progress, 1),
            "connected_nodes": random.randint(3, 25),
            "current_epoch": current_epoch,
            "total_epochs": random.randint(100, 300),
            "training_strategy": random.choice([TrainingStrategy.SFT, TrainingStrategy.DPO, TrainingStrategy.GRPO, TrainingStrategy.IPO, TrainingStrategy.KTO]),
            "protocol": random.choice([Protocol.FEDAVG, Protocol.FEDYGI, Protocol.FEDADAM, Protocol.FEDAVGM]),
            "epochs": random.randint(100, 300),
            "batch_size": random.choice([16, 32, 64, 128]),
            "learning_rate": random.choice([0.0001, 0.0005, 0.001, 0.005, 0.01]),
            "node_ip": f"192.168.1.{random.randint(100, 254)}",
            "created_time": created_date.strftime("%Y-%m-%d %H:%M:%S"),
            "last_update": last_update,
            "metrics": {
                "accuracy": round(current_accuracy, 1),
                "loss": round(random.uniform(0.05, 0.8), 3),
                "f1_score": round(current_accuracy * random.uniform(0.85, 0.98), 1),
                "precision": round(current_accuracy * random.uniform(0.85, 0.95), 1),
                "recall": round(current_accuracy * random.uniform(0.80, 0.95), 1)
            }
        }
        projects.append(project)

    return projects

# Mock data removed - now using database

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    status: Optional[ProjectStatus] = None,
    project_type: Optional[ProjectType] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取项目列表
    支持按状态、类型和搜索关键词过滤
    """
    query = db.query(Project)

    if status:
        query = query.filter(Project.status == status.value)

    if project_type:
        query = query.filter(Project.strategy == project_type.value)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Project.name.ilike(search_term)) |
            (Project.description.ilike(search_term))
        )

    projects = query.all()

    # Convert database projects to response format
    result = []
    for project in projects:
        project_response = ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            model="",  # Will be filled from related models
            status=ProjectStatus.CREATED if not project.status or project.status not in [e.value for e in ProjectStatus] else ProjectStatus(project.status),
            progress=project.progress,
            connected_nodes=db.query(Node).filter(Node.project_id == project.id).count(),
            current_epoch=0,  # Could be calculated from training status
            total_epochs=project.epoches,
            training_strategy=TrainingStrategy.SFT if not project.strategy or project.strategy not in [e.value for e in TrainingStrategy] else TrainingStrategy(project.strategy),
            protocol=Protocol.FEDAVG if not project.protocol or project.protocol not in [e.value for e in Protocol] else Protocol(project.protocol),
            epochs=project.epoches,
            batch_size=project.batch_size,
            learning_rate=project.learning_rate,
            node_ip="",  # Could be from related nodes
            created_time=project.created_time.isoformat() if project.created_time else "",
            last_update=project.updated_time.isoformat() if project.updated_time else "",
            metrics={}
        )
        result.append(project_response)

    return result

@router.get("/{project_id}/", response_model=ProjectResponse)
async def get_project(project_id: str, db: Session = Depends(get_db)):
    """
    获取特定项目详情
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    project = db.query(Project).filter(Project.id == project_id_int).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get related data
    connected_nodes = db.query(Node).filter(Node.project_id == project.id).count()

    return ProjectResponse(
        id=str(project.id),
        name=project.name,
        description=project.description,
        model="",  # Will be filled from related models
        status=ProjectStatus.CREATED if not project.status or project.status not in [e.value for e in ProjectStatus] else ProjectStatus(project.status),
        progress=project.progress,
        connected_nodes=connected_nodes,
        current_epoch=0,  # Could be calculated from training status
        total_epochs=project.epoches,
        training_strategy=TrainingStrategy.SFT if not project.strategy or project.strategy not in [e.value for e in TrainingStrategy] else TrainingStrategy(project.strategy),
        protocol=Protocol.FEDAVG if not project.protocol or project.protocol not in [e.value for e in Protocol] else Protocol(project.protocol),
        epochs=project.epoches,
        batch_size=project.batch_size,
        learning_rate=project.learning_rate,
        node_ip="",  # Could be from related nodes
        created_time=project.created_time.isoformat() if project.created_time else "",
        last_update=project.updated_time.isoformat() if project.updated_time else "",
        metrics={}
    )

@router.post("/", response_model=ProjectResponse)
async def create_project(request: ProjectCreateRequest, db: Session = Depends(get_db)):
    """
    创建新项目
    """
    # Create new project in database
    new_project = Project(
        user_id=1,  # TODO: Get from authenticated user
        name=request.name,
        description=request.description,
        
        # Training configuration fields (from frontend form)
        training_alg=request.training_alg,
        fed_alg=request.fed_alg,
        num_rounds=request.num_rounds,
        num_clients=request.num_clients,
        sample_clients=request.sample_clients,
        max_steps=request.max_steps,
        lr=request.lr,
        dataset_sample=request.dataset_sample,
        model_name_or_path=request.model_name_or_path,
        dataset_name=request.dataset_name,
        
        # Legacy fields (for backward compatibility)
        strategy=request.training_strategy.value if request.training_strategy else "sft",
        protocol=request.protocol.value if request.protocol else "fedavg",
        epoches=request.epochs,
        learning_rate=request.learning_rate,
        batch_size=request.batch_size,
        
        status="created",
        progress=0.0,
        task_id=f"task-{uuid.uuid4().hex[:8]}"
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return ProjectResponse(
        id=str(new_project.id),
        name=new_project.name,
        description=new_project.description,
        model=request.model,
        status=ProjectStatus.CREATED,
        progress=0.0,
        connected_nodes=0,
        current_epoch=0,
        total_epochs=new_project.epoches,
        training_strategy=TrainingStrategy(new_project.strategy),
        protocol=Protocol(new_project.protocol),
        epochs=new_project.epoches,
        batch_size=new_project.batch_size,
        learning_rate=new_project.learning_rate,
        node_ip=request.node_ip,
        created_time=new_project.created_time.isoformat() if new_project.created_time else "",
        last_update=new_project.updated_time.isoformat() if new_project.updated_time else "",
        metrics={}
    )

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
async def delete_project(project_id: str, db: Session = Depends(get_db)):
    """
    删除项目
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    # Find the project in database
    project = db.query(Project).filter(Project.id == project_id_int).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Delete related nodes first (cascade delete)
    db.query(Node).filter(Node.project_id == project_id_int).delete()
    
    # Delete related models first (cascade delete)
    db.query(Model).filter(Model.project_id == project_id_int).delete()
    
    # Delete the project
    db.delete(project)
    db.commit()
    
    return BaseResponse(
        success=True,
        message=f"Project '{project.name}' deleted successfully"
    )

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
async def get_system_stats(db: Session = Depends(get_db)):
    """
    获取系统统计信息
    """
    total_projects = db.query(Project).count()
    active_projects = db.query(Project).filter(
        Project.status.in_(["active", "training"])
    ).count()

    total_nodes = db.query(Node).count()
    online_nodes = db.query(Node).filter(Node.state == "online").count()
    training_nodes = db.query(Node).filter(Node.state == "training").count()
    error_nodes = db.query(Node).filter(Node.state == "error").count()

    completion_rate = round((active_projects / total_projects * 100) if total_projects > 0 else 0, 2)

    return SystemStats(
        total_projects=total_projects,
        active_projects=active_projects,
        total_nodes=total_nodes,
        online_nodes=online_nodes,
        training_nodes=training_nodes,
        error_nodes=error_nodes,
        completion_rate=completion_rate
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
