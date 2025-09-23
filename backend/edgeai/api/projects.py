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
    ProjectType
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
        query = query.filter(Project.training_alg == project_type.value)

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
            progress=project.progress or 0.0,
            connected_nodes=db.query(Node).filter(Node.project_id == project.id).count(),
            current_epoch=0,  # Could be calculated from training status

            # 统一的训练参数
            training_alg=project.training_alg or "sft",
            fed_alg=project.fed_alg or "fedavg",
            secure_aggregation=project.secure_aggregation or "shamir_threshold",

            # 训练配置
            total_epochs=project.total_epochs or 100,
            num_rounds=project.num_rounds or 10,
            batch_size=project.batch_size or 32,
            lr=project.lr or "1e-4",

            # 高级训练参数
            num_computers=project.num_computers or 3,
            threshold=project.threshold or 2,
            num_clients=project.num_clients or 2,
            sample_clients=project.sample_clients or 2,
            max_steps=project.max_steps or 100,

            # 模型和数据集配置
            model_name_or_path=project.model_name_or_path or "sshleifer/tiny-gpt2",
            dataset_name=project.dataset_name or "vicgalle/alpaca-gpt4",
            dataset_sample=project.dataset_sample or 50,

            # 其他信息
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
        progress=project.progress or 0.0,
        connected_nodes=connected_nodes,
        current_epoch=0,  # Could be calculated from training status

        # 统一的训练参数
        training_alg=project.training_alg or "sft",
        fed_alg=project.fed_alg or "fedavg",
        secure_aggregation=project.secure_aggregation or "shamir_threshold",

        # 训练配置
        total_epochs=project.total_epochs or 100,
        num_rounds=project.num_rounds or 10,
        batch_size=project.batch_size or 32,
        lr=project.lr or "1e-4",

        # 高级训练参数
        num_computers=project.num_computers or 3,
        threshold=project.threshold or 2,
        num_clients=project.num_clients or 2,
        sample_clients=project.sample_clients or 2,
        max_steps=project.max_steps or 100,

        # 模型和数据集配置
        model_name_or_path=project.model_name_or_path or "sshleifer/tiny-gpt2",
        dataset_name=project.dataset_name or "vicgalle/alpaca-gpt4",
        dataset_sample=project.dataset_sample or 50,

        # 其他信息
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
    # Create new project in database (使用合并后的字段)
    new_project = Project(
        user_id=1,  # TODO: Get from authenticated user
        name=request.name,
        description=request.description,

        # 统一的训练参数
        training_alg=request.training_alg,
        fed_alg=request.fed_alg,
        secure_aggregation=request.secure_aggregation,

        # 训练配置
        total_epochs=request.total_epochs,
        num_rounds=request.num_rounds,
        batch_size=request.batch_size,
        lr=request.lr,

        # 高级训练参数
        num_computers=request.num_computers,
        threshold=request.threshold,
        num_clients=request.num_clients,
        sample_clients=request.sample_clients,
        max_steps=request.max_steps,

        # 模型和数据集配置
        model_name_or_path=request.model_name_or_path,
        dataset_name=request.dataset_name,
        dataset_sample=request.dataset_sample,

        # 项目状态
        status="created",
        progress=0.0,
        task_id=f"task-{uuid.uuid4().hex[:8]}"
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # Create nodes for the project
    created_nodes = []
    for node_data in request.nodes:
        new_node = Node(
            user_id=1,  # 默认用户ID，实际应用中应该从认证中获取
            project_id=new_project.id,
            name=node_data.name or f"Node {node_data.ip}",
            path_ipv4=node_data.ip,
            state="idle",  # 使用idle而不是offline
            role="worker",  # 使用worker而不是edge
            progress=0.0,
            cpu="",  # 使用字符串而不是数字
            gpu="",  # 使用字符串而不是数字
            memory=""  # 使用字符串而不是数字
        )
        db.add(new_node)
        created_nodes.append(new_node)

    db.commit()

    return ProjectResponse(
        id=str(new_project.id),
        name=new_project.name,
        description=new_project.description,
        model=request.model,
        status=ProjectStatus.CREATED,
        progress=0.0,
        connected_nodes=len(created_nodes),
        current_epoch=0,

        # 统一的训练参数
        training_alg=new_project.training_alg,
        fed_alg=new_project.fed_alg,
        secure_aggregation=new_project.secure_aggregation,

        # 训练配置
        total_epochs=new_project.total_epochs,
        num_rounds=new_project.num_rounds,
        batch_size=new_project.batch_size,
        lr=new_project.lr,

        # 高级训练参数
        num_computers=new_project.num_computers,
        threshold=new_project.threshold,
        num_clients=new_project.num_clients,
        sample_clients=new_project.sample_clients,
        max_steps=new_project.max_steps,

        # 模型和数据集配置
        model_name_or_path=new_project.model_name_or_path,
        dataset_name=new_project.dataset_name,
        dataset_sample=new_project.dataset_sample,

        # 其他信息
        node_ip="",  # Multiple nodes now, so this field is empty
        created_time=new_project.created_time.isoformat() if new_project.created_time else "",
        last_update=new_project.updated_time.isoformat() if new_project.updated_time else "",
        metrics={}
    )

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, request: ProjectCreateRequest, db: Session = Depends(get_db)):
    """
    更新项目信息
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    project = db.query(Project).filter(Project.id == project_id_int).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Update project fields
    project.name = request.name
    project.description = request.description
    project.strategy = request.type.value
    project.updated_time = datetime.now()

    db.commit()
    db.refresh(project)

    return ProjectResponse(
        id=str(project.id),
        name=project.name,
        description=project.description,
        model="",
        status=ProjectStatus.CREATED if not project.status or project.status not in [e.value for e in ProjectStatus] else ProjectStatus(project.status),
        type=ProjectType.COMPUTER_VISION,
        model_type=request.model_type,
        progress=project.progress or 0.0,
        total_epochs=project.epoches,
        training_strategy=TrainingStrategy(project.strategy),
        protocol=Protocol(project.protocol),
        epochs=project.epoches,
        batch_size=project.batch_size,
        learning_rate=project.learning_rate,
        node_ip="",
        created_time=project.created_time.isoformat() if project.created_time else "",
        last_update=project.updated_time.isoformat() if project.updated_time else "",
        metrics={}
    )

@router.delete("/{project_id}", response_model=BaseResponse)
async def delete_project(project_id: str, db: Session = Depends(get_db)):
    """
    删除项目及其相关数据
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    project = db.query(Project).filter(Project.id == project_id_int).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 删除项目关联的节点
    project_nodes = db.query(Node).filter(Node.project_id == project_id_int).all()
    for node in project_nodes:
        db.delete(node)
    
    # 删除项目关联的模型
    project_models = db.query(Model).filter(Model.project_id == project_id_int).all()
    for model in project_models:
        db.delete(model)
    
    # 删除项目本身
    db.delete(project)
    db.commit()

    return BaseResponse(
        success=True,
        message=f"Project '{project.name}' and all related data deleted successfully"
    )

@router.post("/import", response_model=BaseResponse)
async def import_project(request: ProjectImportRequest, db: Session = Depends(get_db)):
    """
    导入项目
    """
    try:
        new_project = Project(
            name=request.project_data.get("name", "Imported Project (db)"),
            description=request.project_data.get("description", "Imported from external source"),
            strategy=request.project_data.get("type", "Computer Vision"),
            protocol="HTTP",
            epoches=100,
            learning_rate=0.001,
            batch_size=32,
            status="created",
            progress=0.0,
            task_id=f"task_{uuid.uuid4().hex[:8]}",
            user_id=1  # Default to admin user
        )

        db.add(new_project)
        db.commit()
        db.refresh(new_project)

        return BaseResponse(
            success=True,
            message=f"Project imported successfully: {new_project.id}"
        )
    except Exception as e:
        db.rollback()
        return BaseResponse(
            success=False,
            error=str(e)
        )

@router.post("/{project_id}/export", response_model=BaseResponse)
async def export_project(project_id: str, request: ProjectExportRequest, db: Session = Depends(get_db)):
    """
    导出项目
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    project = db.query(Project).filter(Project.id == project_id_int).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    export_data = {
        "id": str(project.id),
        "name": project.name,
        "description": project.description,
        "strategy": project.strategy,
        "protocol": project.protocol,
        "status": project.status,
        "progress": project.progress,
        "exported_at": datetime.now().isoformat(),
        "export_format": request.format,
        "include_models": request.include_models,
        "include_data": request.include_data
    }

    return BaseResponse(
        success=True,
        message="Project exported successfully",
        data=export_data
    )

@router.get("/{project_id}/visualization")
async def get_project_visualization(project_id: str, db: Session = Depends(get_db)):
    """
    获取项目的完整可视化数据，包括项目详情、关联的模型和节点
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    project = db.query(Project).filter(Project.id == project_id_int).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 获取关联的模型
    models = db.query(Model).filter(Model.project_id == project.id).all()

    # 获取关联的节点
    nodes = db.query(Node).filter(Node.project_id == project.id).all()

    # 构建可视化数据
    visualization_data = {
        "project": {
            "id": str(project.id),
            "name": project.name,
            "description": project.description,
            "status": project.status,
            "progress": project.progress,
            "strategy": project.strategy,
            "protocol": project.protocol,
            "epochs": project.epoches,
            "batch_size": project.batch_size,
            "learning_rate": project.learning_rate,
            "created_time": project.created_time.isoformat() if project.created_time else None,
            "updated_time": project.updated_time.isoformat() if project.updated_time else None
        },
        "models": [
            {
                "id": str(model.id),
                "name": model.name,
                "description": model.description,
                "status": model.status,
                "progress": model.progress,
                "accuracy": model.accuracy,
                "loss": model.loss,
                "version": model.version,
                "size": model.size,
                "file_path": model.file_path,
                "class_config": model.class_config,
                "created_time": model.created_time.isoformat() if model.created_time else None,
                "updated_time": model.updated_time.isoformat() if model.updated_time else None
            }
            for model in models
        ],
        "nodes": [
            {
                "id": str(node.id),
                "name": node.name,
                "path_ipv4": node.path_ipv4,
                "state": node.state,
                "role": node.role,
                "progress": node.progress,
                "cpu": node.cpu,
                "gpu": node.gpu,
                "memory": node.memory,
                "created_time": node.created_time.isoformat() if node.created_time else None,
                "last_updated_time": node.last_updated_time.isoformat() if node.last_updated_time else None
            }
            for node in nodes
        ],
        "summary": {
            "total_models": len(models),
            "total_nodes": len(nodes),
            "training_nodes": len([n for n in nodes if n.state == "training"]),
            "active_models": len([m for m in models if m.status in ["training", "trained"]])
        }
    }

    return visualization_data

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
async def duplicate_project(project_id: str, db: Session = Depends(get_db)):
    """
    复制项目
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    original_project = db.query(Project).filter(Project.id == project_id_int).first()
    if not original_project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_project = Project(
        name=f"{original_project.name} (Copy) (db)",
        description=original_project.description,
        strategy=original_project.strategy,
        protocol=original_project.protocol,
        epoches=original_project.epoches,
        learning_rate=original_project.learning_rate,
        batch_size=original_project.batch_size,
        status="created",
        progress=0.0,
        task_id=f"task_{uuid.uuid4().hex[:8]}",
        user_id=original_project.user_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return BaseResponse(
        success=True,
        message=f"Project duplicated successfully: {new_project.id}"
    )

@router.post("/{project_id}/start", response_model=BaseResponse)
async def start_project(project_id: str, db: Session = Depends(get_db)):
    """
    启动项目
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    project = db.query(Project).filter(Project.id == project_id_int).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.status = "training"
    project.updated_time = datetime.now()
    db.commit()

    return BaseResponse(
        success=True,
        message=f"Project {project_id} started successfully"
    )

@router.post("/{project_id}/pause", response_model=BaseResponse)
async def pause_project(project_id: str, db: Session = Depends(get_db)):
    """
    暂停项目
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    project = db.query(Project).filter(Project.id == project_id_int).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.status = "paused"
    project.updated_time = datetime.now()
    db.commit()

    return BaseResponse(
        success=True,
        message=f"Project {project_id} paused successfully"
    )

@router.post("/{project_id}/stop", response_model=BaseResponse)
async def stop_project(project_id: str, db: Session = Depends(get_db)):
    """
    停止项目
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    project = db.query(Project).filter(Project.id == project_id_int).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.status = "idle"
    project.updated_time = datetime.now()
    db.commit()

    return BaseResponse(
        success=True,
        message=f"Project {project_id} stopped successfully"
    )

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
