from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from ..schemas.edgeai import TaskRequest, TaskResponse
from common.schemas.common import BaseResponse
from common.api.auth import get_current_user_id
from database.edgeai import get_db, User, Project, Model, Node
from datetime import datetime, timedelta
import uuid
import random

router = APIRouter()

def generate_dynamic_tasks():
    """生成动态任务数据"""
    task_templates = [
        # 训练任务
        {
            "task_type": "training",
            "description": "Model training with federated learning",
            "config_template": {
                "epochs": [50, 100, 200, 300],
                "batch_size": [16, 32, 64, 128],
                "learning_rate": [0.0001, 0.0005, 0.001, 0.005]
            }
        },
        {
            "task_type": "fine_tuning",
            "description": "Fine-tune pre-trained model",
            "config_template": {
                "base_model": ["resnet50", "vgg16", "inception_v3", "transformer_base"],
                "epochs": [20, 50, 100],
                "learning_rate": [0.00001, 0.0001, 0.001]
            }
        },
        {
            "task_type": "inference",
            "description": "Run model inference on new data",
            "config_template": {
                "model_path": ["/models/cnn_model.pth", "/models/rnn_model.h5", "/models/transformer.pkl"],
                "input_size": [[224, 224, 3], [128, 128, 1], [512, 512, 3]],
                "batch_size": [1, 8, 16, 32]
            }
        },
        {
            "task_type": "data_processing",
            "description": "Process and clean training data",
            "config_template": {
                "data_path": ["/data/images", "/data/text", "/data/sensor_data"],
                "output_format": ["hdf5", "parquet", "csv", "json"],
                "preprocessing": ["normalize", "augment", "clean", "tokenize"]
            }
        },
        {
            "task_type": "model_validation",
            "description": "Validate model performance",
            "config_template": {
                "validation_set": ["/data/val_set_1", "/data/val_set_2", "/data/test_set"],
                "metrics": ["accuracy", "f1_score", "precision", "recall"],
                "cross_validation": [3, 5, 10]
            }
        },
        {
            "task_type": "hyperparameter_tuning",
            "description": "Optimize model hyperparameters",
            "config_template": {
                "search_method": ["grid_search", "random_search", "bayesian"],
                "parameter_space": ["learning_rate", "batch_size", "hidden_units"],
                "max_trials": [10, 20, 50, 100]
            }
        },
        {
            "task_type": "model_deployment",
            "description": "Deploy model to production",
            "config_template": {
                "deployment_target": ["edge_devices", "cloud", "hybrid"],
                "scaling_policy": ["auto", "manual", "scheduled"],
                "health_checks": ["endpoint", "metrics", "logs"]
            }
        },
        {
            "task_type": "data_collection",
            "description": "Collect training data from sensors",
            "config_template": {
                "data_sources": ["camera", "lidar", "accelerometer", "temperature"],
                "collection_duration": ["1h", "6h", "24h", "7d"],
                "sampling_rate": [1, 10, 100, 1000]
            }
        },
        {
            "task_type": "anomaly_detection",
            "description": "Detect anomalies in system behavior",
            "config_template": {
                "detection_method": ["isolation_forest", "autoencoder", "statistical"],
                "threshold": [0.1, 0.05, 0.01],
                "window_size": [100, 500, 1000]
            }
        },
        {
            "task_type": "model_compression",
            "description": "Compress model for edge deployment",
            "config_template": {
                "compression_method": ["quantization", "pruning", "distillation"],
                "compression_ratio": [0.1, 0.25, 0.5, 0.75],
                "target_accuracy": [0.9, 0.95, 0.98]
            }
        },
        {
            "task_type": "federated_aggregation",
            "description": "Aggregate federated learning updates",
            "config_template": {
                "aggregation_method": ["fedavg", "fedprox", "scaffold"],
                "min_clients": [2, 5, 10],
                "rounds": [10, 50, 100]
            }
        },
        {
            "task_type": "model_monitoring",
            "description": "Monitor model performance in production",
            "config_template": {
                "monitoring_interval": ["5m", "1h", "6h", "24h"],
                "alert_threshold": [0.05, 0.1, 0.2],
                "metrics_tracked": ["accuracy", "latency", "throughput"]
            }
        },
        {
            "task_type": "data_synchronization",
            "description": "Synchronize data across nodes",
            "config_template": {
                "sync_method": ["rsync", "delta_sync", "full_sync"],
                "frequency": ["realtime", "hourly", "daily"],
                "compression": [True, False]
            }
        },
        {
            "task_type": "security_scan",
            "description": "Scan for security vulnerabilities",
            "config_template": {
                "scan_type": ["network", "application", "data"],
                "severity_filter": ["critical", "high", "medium", "all"],
                "scan_depth": ["surface", "deep", "comprehensive"]
            }
        },
        {
            "task_type": "backup_creation",
            "description": "Create system backups",
            "config_template": {
                "backup_type": ["full", "incremental", "differential"],
                "compression": ["gzip", "lz4", "zstd"],
                "retention_days": [7, 30, 90, 365]
            }
        }
    ]

    project_ids = [f"proj-{str(i+1).zfill(3)}" for i in range(10)]
    statuses = ["pending", "running", "completed", "failed", "paused"]
    priorities = [1, 2, 3, 4, 5]
    node_pools = [
        ["control-1", "control-2"],
        ["edge-1", "edge-2", "edge-3"],
        ["edge-4", "edge-5"],
        ["edge-1", "edge-3", "edge-5"],
        ["control-1"],
        []
    ]

    tasks = []

    for i in range(15):
        template = random.choice(task_templates)
        status = random.choice(statuses)
        priority = random.choice(priorities)

        # 时间计算
        created_hours_ago = random.randint(1, 168)  # 1小时到1周前
        created_at = datetime.now() - timedelta(hours=created_hours_ago)

        if status == "pending":
            started_at = None
            completed_at = None
            progress = 0.0
        elif status == "running":
            start_delay = random.randint(10, 60)  # 创建后10-60分钟开始
            started_at = created_at + timedelta(minutes=start_delay)
            completed_at = None
            progress = random.uniform(1, 95)
        elif status == "completed":
            start_delay = random.randint(5, 30)
            duration = random.randint(30, 480)  # 30分钟到8小时
            started_at = created_at + timedelta(minutes=start_delay)
            completed_at = started_at + timedelta(minutes=duration)
            progress = 100.0
        elif status == "failed":
            start_delay = random.randint(5, 30)
            failure_time = random.randint(10, 240)  # 10分钟到4小时后失败
            started_at = created_at + timedelta(minutes=start_delay)
            completed_at = started_at + timedelta(minutes=failure_time)
            progress = random.uniform(5, 80)
        else:  # paused
            start_delay = random.randint(5, 30)
            started_at = created_at + timedelta(minutes=start_delay)
            completed_at = None
            progress = random.uniform(10, 70)

        # 配置生成
        config = {}
        for key, options in template["config_template"].items():
            if isinstance(options, list):
                config[key] = random.choice(options)
            else:
                config[key] = options

        # 节点分配
        assigned_nodes = random.choice(node_pools) if status != "pending" else []

        task = {
            "id": f"task-{str(i+1).zfill(3)}",
            "project_id": random.choice(project_ids),
            "task_type": template["task_type"],
            "description": template["description"],
            "status": status,
            "priority": priority,
            "created_at": created_at,
            "started_at": started_at,
            "completed_at": completed_at,
            "progress": round(progress, 1),
            "assigned_nodes": assigned_nodes,
            "config": config,
            "estimated_duration": f"{random.randint(30, 480)} minutes",
            "resource_requirements": {
                "cpu_cores": random.randint(1, 8),
                "memory_gb": random.randint(2, 32),
                "gpu_required": random.choice([True, False]),
                "storage_gb": random.randint(1, 100)
            },
            "retry_count": random.randint(0, 3) if status == "failed" else 0,
            "last_error": "Connection timeout" if status == "failed" else None
        }
        tasks.append(task)

    return tasks

# 生成初始任务数据
mock_tasks = generate_dynamic_tasks()

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    task_type: Optional[str] = None,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    获取任务列表
    支持按项目ID、状态和类型过滤
    """
    filtered_tasks = mock_tasks
    
    if project_id:
        filtered_tasks = [t for t in filtered_tasks if t["project_id"] == project_id]
    
    if status:
        filtered_tasks = [t for t in filtered_tasks if t["status"] == status]
    
    if task_type:
        filtered_tasks = [t for t in filtered_tasks if t["task_type"] == task_type]
    
    return [TaskResponse(**task) for task in filtered_tasks]

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """
    获取特定任务详情
    """
    for task in mock_tasks:
        if task["id"] == task_id:
            return TaskResponse(**task)
    
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """
    创建新任务
    """
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    
    new_task = {
        "id": task_id,
        "project_id": request.project_id,
        "task_type": request.task_type,
        "status": "pending",
        "priority": request.priority,
        "created_at": datetime.now(),
        "started_at": None,
        "completed_at": None,
        "progress": 0.0,
        "assigned_nodes": request.target_nodes or [],
        "config": request.config or {}
    }
    
    mock_tasks.append(new_task)
    return TaskResponse(**new_task)

@router.put("/{task_id}/start", response_model=BaseResponse)
async def start_task(task_id: str):
    """
    启动任务
    """
    for task in mock_tasks:
        if task["id"] == task_id:
            if task["status"] != "pending":
                raise HTTPException(status_code=400, detail="Task is not in pending status")
            
            task["status"] = "running"
            task["started_at"] = datetime.now()
            
            return BaseResponse(
                success=True,
                message=f"Task {task_id} started successfully"
            )
    
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/{task_id}/stop", response_model=BaseResponse)
async def stop_task(task_id: str):
    """
    停止任务
    """
    for task in mock_tasks:
        if task["id"] == task_id:
            if task["status"] != "running":
                raise HTTPException(status_code=400, detail="Task is not running")
            
            task["status"] = "stopped"
            task["completed_at"] = datetime.now()
            
            return BaseResponse(
                success=True,
                message=f"Task {task_id} stopped successfully"
            )
    
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/{task_id}/complete", response_model=BaseResponse)
async def complete_task(task_id: str):
    """
    完成任务
    """
    for task in mock_tasks:
        if task["id"] == task_id:
            if task["status"] not in ["running", "pending"]:
                raise HTTPException(status_code=400, detail="Task cannot be completed in current status")
            
            task["status"] = "completed"
            task["progress"] = 100.0
            task["completed_at"] = datetime.now()
            
            return BaseResponse(
                success=True,
                message=f"Task {task_id} completed successfully"
            )
    
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}", response_model=BaseResponse)
async def delete_task(task_id: str):
    """
    删除任务
    """
    global mock_tasks
    original_count = len(mock_tasks)
    mock_tasks = [t for t in mock_tasks if t["id"] != task_id]
    
    if len(mock_tasks) < original_count:
        return BaseResponse(
            success=True,
            message="Task deleted successfully"
        )
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@router.get("/stats/overview")
async def get_task_stats():
    """
    获取任务统计信息
    """
    total_tasks = len(mock_tasks)
    pending_tasks = len([t for t in mock_tasks if t["status"] == "pending"])
    running_tasks = len([t for t in mock_tasks if t["status"] == "running"])
    completed_tasks = len([t for t in mock_tasks if t["status"] == "completed"])
    stopped_tasks = len([t for t in mock_tasks if t["status"] == "stopped"])
    
    # 按类型统计
    task_types = {}
    for task in mock_tasks:
        task_types[task["task_type"]] = task_types.get(task["task_type"], 0) + 1
    
    # 按优先级统计
    priority_counts = {}
    for task in mock_tasks:
        priority_counts[task["priority"]] = priority_counts.get(task["priority"], 0) + 1
    
    return {
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "running_tasks": running_tasks,
        "completed_tasks": completed_tasks,
        "stopped_tasks": stopped_tasks,
        "task_types": task_types,
        "priority_distribution": priority_counts,
        "completion_rate": round(completed_tasks / total_tasks * 100, 2) if total_tasks > 0 else 0
    }

@router.post("/batch-create")
async def create_batch_tasks(requests: List[TaskRequest]):
    """
    批量创建任务
    """
    created_tasks = []
    
    for request in requests:
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        
        new_task = {
            "id": task_id,
            "project_id": request.project_id,
            "task_type": request.task_type,
            "status": "pending",
            "priority": request.priority,
            "created_at": datetime.now(),
            "started_at": None,
            "completed_at": None,
            "progress": 0.0,
            "assigned_nodes": request.target_nodes or [],
            "config": request.config or {}
        }
        
        mock_tasks.append(new_task)
        created_tasks.append(TaskResponse(**new_task))
    
    return {
        "created_tasks": created_tasks,
        "total_created": len(created_tasks)
    }

@router.post("/batch-start")
async def start_batch_tasks(task_ids: List[str]):
    """
    批量启动任务
    """
    results = []
    
    for task_id in task_ids:
        for task in mock_tasks:
            if task["id"] == task_id:
                if task["status"] == "pending":
                    task["status"] = "running"
                    task["started_at"] = datetime.now()
                    results.append({
                        "task_id": task_id,
                        "success": True,
                        "message": "Task started"
                    })
                else:
                    results.append({
                        "task_id": task_id,
                        "success": False,
                        "message": "Task is not in pending status"
                    })
                break
        else:
            results.append({
                "task_id": task_id,
                "success": False,
                "message": "Task not found"
            })
    
    return {
        "results": results,
        "total_started": len([r for r in results if r["success"]])
    }

@router.get("/queue")
async def get_task_queue():
    """
    获取任务队列
    """
    # 按优先级和创建时间排序
    queue_tasks = sorted(
        [t for t in mock_tasks if t["status"] == "pending"],
        key=lambda x: (x["priority"], x["created_at"])
    )
    
    return {
        "queue": [TaskResponse(**task) for task in queue_tasks],
        "total_queued": len(queue_tasks)
    }

@router.put("/{task_id}/priority")
async def update_task_priority(task_id: str, priority: int):
    """
    更新任务优先级
    """
    for task in mock_tasks:
        if task["id"] == task_id:
            task["priority"] = priority
            return BaseResponse(
                success=True,
                message=f"Task {task_id} priority updated to {priority}"
            )
    
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/{task_id}/assign")
async def assign_task_to_nodes(task_id: str, node_ids: List[str]):
    """
    将任务分配给节点
    """
    for task in mock_tasks:
        if task["id"] == task_id:
            task["assigned_nodes"] = node_ids
            return BaseResponse(
                success=True,
                message=f"Task {task_id} assigned to nodes: {', '.join(node_ids)}"
            )
    
    raise HTTPException(status_code=404, detail="Task not found")
