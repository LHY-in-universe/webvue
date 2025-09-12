from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..schemas.edgeai import TaskRequest, TaskResponse
from common.schemas.common import BaseResponse
from datetime import datetime, timedelta
import uuid

router = APIRouter()

# Mock tasks database
mock_tasks = [
    {
        "id": "task-001",
        "project_id": "proj-001",
        "task_type": "training",
        "status": "running",
        "priority": 1,
        "created_at": datetime.now() - timedelta(hours=2),
        "started_at": datetime.now() - timedelta(hours=1, minutes=30),
        "completed_at": None,
        "progress": 65.0,
        "assigned_nodes": ["edge-1", "edge-2"],
        "config": {
            "epochs": 100,
            "batch_size": 32,
            "learning_rate": 0.001
        }
    },
    {
        "id": "task-002",
        "project_id": "proj-002",
        "task_type": "inference",
        "status": "completed",
        "priority": 2,
        "created_at": datetime.now() - timedelta(hours=4),
        "started_at": datetime.now() - timedelta(hours=3, minutes=45),
        "completed_at": datetime.now() - timedelta(minutes=30),
        "progress": 100.0,
        "assigned_nodes": ["edge-3"],
        "config": {
            "model_path": "/models/traffic_model.pth",
            "input_size": [224, 224, 3]
        }
    },
    {
        "id": "task-003",
        "project_id": "proj-003",
        "task_type": "data_processing",
        "status": "pending",
        "priority": 3,
        "created_at": datetime.now() - timedelta(minutes=30),
        "started_at": None,
        "completed_at": None,
        "progress": 0.0,
        "assigned_nodes": [],
        "config": {
            "data_path": "/data/medical_images",
            "output_format": "hdf5"
        }
    }
]

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    task_type: Optional[str] = None
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
