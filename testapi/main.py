from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import random
import time
from datetime import datetime, timedelta
import uuid

app = FastAPI(
    title="Training Monitor API Mock",
    description="模拟训练监控API，提供随机数据",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 数据模型定义
class NodeResource(BaseModel):
    CPU: float
    memory: float
    GPU: Optional[float] = None

class TrainingInfo(BaseModel):
    task_id: str
    progress: float
    epoch: int
    total_epochs: int
    loss: float
    accuracy: Optional[float] = None
    status: str

class RayNode(BaseModel):
    id: str
    name: str
    ip: str
    state: str
    resources: NodeResource
    training: Optional[TrainingInfo] = None

class ClusterStatus(BaseModel):
    status: str
    total_nodes: int
    active_nodes: int
    failed_nodes: int

class TrainingMonitorResponse(BaseModel):
    task_id: str
    status: str
    progress: float
    current_epoch: int
    total_epochs: int
    loss: float
    accuracy: Optional[float] = None
    estimated_time_remaining: Optional[int] = None
    nodes_involved: List[str]
    start_time: str
    last_update: str

class ClusterResponse(BaseModel):
    cluster_status: ClusterStatus
    nodes: List[RayNode]
    last_updated: str

# 生成随机节点数据
def generate_random_node(node_id: str = None) -> RayNode:
    """生成随机节点数据"""
    if not node_id:
        node_id = f"node_{random.randint(1000, 9999)}"
    
    states = ["ALIVE", "DEAD", "UNKNOWN"]
    state = random.choice(states)
    
    # 生成IP地址
    ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    # 生成资源信息
    cpu_count = random.randint(1, 16)
    memory_gb = random.randint(4, 128)
    gpu_count = random.randint(0, 4) if random.random() > 0.3 else 0
    
    resources = NodeResource(
        CPU=cpu_count,
        memory=memory_gb,
        GPU=gpu_count if gpu_count > 0 else None
    )
    
    # 如果有训练任务
    training = None
    if state == "ALIVE" and random.random() > 0.4:
        training = TrainingInfo(
            task_id=f"task_{uuid.uuid4().hex[:8]}",
            progress=random.uniform(0.1, 0.95),
            epoch=random.randint(1, 100),
            total_epochs=random.randint(50, 200),
            loss=random.uniform(0.01, 2.0),
            accuracy=random.uniform(0.7, 0.99) if random.random() > 0.3 else None,
            status=random.choice(["training", "completed", "failed"])
        )
    
    return RayNode(
        id=node_id,
        name=f"Ray Node {node_id}",
        ip=ip,
        state=state,
        resources=resources,
        training=training
    )

# 生成随机训练监控数据
def generate_training_monitor(task_id: str) -> TrainingMonitorResponse:
    """生成随机训练监控数据"""
    progress = random.uniform(0.1, 0.95)
    total_epochs = random.randint(50, 200)
    current_epoch = int(progress * total_epochs)
    
    # 生成参与节点
    node_count = random.randint(1, 5)
    nodes_involved = [f"node_{random.randint(1000, 9999)}" for _ in range(node_count)]
    
    # 估算剩余时间（秒）
    remaining_time = None
    if progress < 1.0:
        remaining_time = random.randint(300, 7200)  # 5分钟到2小时
    
    return TrainingMonitorResponse(
        task_id=task_id,
        status=random.choice(["running", "completed", "failed", "paused"]),
        progress=progress,
        current_epoch=current_epoch,
        total_epochs=total_epochs,
        loss=random.uniform(0.01, 2.0),
        accuracy=random.uniform(0.7, 0.99) if random.random() > 0.3 else None,
        estimated_time_remaining=remaining_time,
        nodes_involved=nodes_involved,
        start_time=(datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
        last_update=datetime.now().isoformat()
    )



# 添加缺失的API端点以匹配外部API
class TrainingParameters(BaseModel):
    training_alg: str
    fed_alg: str
    secure_aggregation: str
    num_computers: int
    threshold: int
    num_rounds: int
    num_clients: int
    sample_clients: int
    max_steps: int
    lr: str
    model_name_or_path: str
    dataset_name: str
    dataset_sample: int

class TrainRequest(BaseModel):
    parameters: TrainingParameters

class ValidationErrorDetail(BaseModel):
    loc: List[str]
    msg: str
    type: str

class ValidationErrorResponse(BaseModel):
    detail: List[ValidationErrorDetail]

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: float
    current_epoch: int
    total_epochs: int
    loss: float
    accuracy: Optional[float] = None
    start_time: str
    last_update: str

class TasksList(BaseModel):
    tasks: List[TaskStatus]
    total_count: int

@app.post("/train", responses={
    200: {"description": "Successful Response", "content": {"application/json": {"schema": {"type": "string"}}}},
    422: {"description": "Validation Error", "model": ValidationErrorResponse}
})
async def start_training(request: TrainRequest):
    """开始训练任务"""
    try:
        # 模拟参数验证
        params = request.parameters
        
        # 随机决定是否返回验证错误（10%概率）
        if random.random() < 0.1:
            # 返回验证错误
            error_details = [
                ValidationErrorDetail(
                    loc=["body", "parameters", random.choice(["training_alg", "fed_alg", "num_computers"])],
                    msg=random.choice(["field required", "ensure this value is greater than 0", "invalid choice"]),
                    type=random.choice(["value_error.missing", "value_error.number.not_gt", "type_error.enum"])
                )
            ]
            raise HTTPException(
                status_code=422,
                detail=[error.model_dump() for error in error_details]
            )
        
        # 成功情况：返回随机生成的任务ID字符串
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        return task_id
        
    except HTTPException:
        raise
    except Exception as e:
        # 其他错误情况
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{task_id}", responses={
    200: {"description": "Successful Response", "content": {"application/json": {"schema": {"type": "string"}}}},
    422: {"description": "Validation Error", "model": ValidationErrorResponse}
})
async def get_task_status(task_id: str):
    """获取任务状态"""
    try:
        # 模拟参数验证 - 如果task_id为空或无效格式，返回422错误
        if not task_id or task_id.strip() == "":
            error_details = [
                ValidationErrorDetail(
                    loc=["path", "task_id"],
                    msg="Required field is not provided.",
                    type="value_error.missing"
                )
            ]
            raise HTTPException(
                status_code=422,
                detail=[error.model_dump() for error in error_details]
            )
        
        # 随机决定是否返回验证错误（5%概率）
        if random.random() < 0.05:
            error_details = [
                ValidationErrorDetail(
                    loc=["path", "task_id"],
                    msg=random.choice(["Invalid task ID format", "Task ID must be alphanumeric"]),
                    type="value_error.str.regex"
                )
            ]
            raise HTTPException(
                status_code=422,
                detail=[error.model_dump() for error in error_details]
            )
        
        # 成功情况：返回随机状态字符串
        status_options = [
            "running",
            "completed", 
            "failed",
            "pending",
            "cancelled",
            "paused"
        ]
        
        return random.choice(status_options)
        
    except HTTPException:
        raise
    except Exception as e:
        # 其他错误情况
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks/{task_id}", responses={
    200: {"description": "Successful Response", "content": {"application/json": {"schema": {"type": "string"}}}},
    422: {"description": "Validation Error", "model": ValidationErrorResponse}
})
async def delete_task(task_id: str):
    """删除任务：终止对应训练进程（整组），并将状态标记为deleted"""
    try:
        # 模拟参数验证 - 如果task_id为空或无效格式，返回422错误
        if not task_id or task_id.strip() == "":
            error_details = [
                ValidationErrorDetail(
                    loc=["path", "task_id"],
                    msg="Required field is not provided.",
                    type="value_error.missing"
                )
            ]
            raise HTTPException(
                status_code=422,
                detail=[error.model_dump() for error in error_details]
            )
        
        # 随机决定是否返回验证错误（5%概率）
        if random.random() < 0.05:
            error_details = [
                ValidationErrorDetail(
                    loc=["path", "task_id"],
                    msg=random.choice(["Invalid task ID format", "Task ID must be alphanumeric", "Task not found"]),
                    type=random.choice(["value_error.str.regex", "value_error.not_found"])
                )
            ]
            raise HTTPException(
                status_code=422,
                detail=[error.model_dump() for error in error_details]
            )
        
        # 成功情况：返回删除确认消息字符串
        success_messages = [
            "Task deleted successfully",
            "Training process terminated and task marked as deleted",
            "Task removed from queue",
            f"Task {task_id} has been deleted",
            "Deletion completed",
            "Task terminated and cleaned up"
        ]
        
        return random.choice(success_messages)
        
    except HTTPException:
        raise
    except Exception as e:
        # 其他错误情况
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasksList", responses={
    200: {"description": "Successful Response", "content": {"application/json": {"schema": {"type": "string"}}}}
})
async def list_tasks():
    """获取任务列表"""
    try:
        # 成功情况：返回任务列表信息的字符串表示
        task_count = random.randint(1, 8)
        task_list_options = [
            f"Found {task_count} tasks in queue",
            f"Task list: {task_count} total tasks - {random.randint(0, task_count)} running, {random.randint(0, task_count)} completed",
            f"Active tasks: {random.randint(1, task_count)} | Pending: {random.randint(0, 3)} | Failed: {random.randint(0, 2)}",
            f"Training queue contains {task_count} tasks",
            f"Task summary: {task_count} tasks found, last updated {random.randint(1, 60)} minutes ago",
            f"Current task list: {task_count} entries - Status: {'healthy' if random.random() > 0.3 else 'warning'}"
        ]
        
        return random.choice(task_list_options)
        
    except Exception as e:
        # 其他错误情况
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hasRunningTask", responses={
    200: {"description": "Successful Response", "content": {"application/json": {"schema": {"type": "boolean"}}}}
})
async def has_running_task():
    """检查是否有运行中的任务"""
    try:
        # 随机返回true或false，模拟检查是否有运行中的任务
        # true表示至少有一个任务正在运行，false表示没有运行中的任务
        has_running = random.choice([True, False])
        
        return has_running
        
    except Exception as e:
        # 其他错误情况
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/monitor/{task_id}", responses={
    200: {"description": "Successful Response", "content": {"application/json": {"schema": {"type": "string"}}}},
    422: {"description": "Validation Error", "model": ValidationErrorResponse}
})
async def get_monitor(task_id: str):
    """获取训练进度指标"""
    try:
        # 模拟参数验证 - 如果task_id为空或无效格式，返回422错误
        if not task_id or task_id.strip() == "":
            error_details = [
                ValidationErrorDetail(
                    loc=["path", "task_id"],
                    msg="Required field is not provided.",
                    type="value_error.missing"
                )
            ]
            raise HTTPException(
                status_code=422,
                detail=[error.model_dump() for error in error_details]
            )
        
        # 随机决定是否返回验证错误（5%概率）
        if random.random() < 0.05:
            error_details = [
                ValidationErrorDetail(
                    loc=["path", "task_id"],
                    msg=random.choice(["Invalid task ID format", "Task not found", "Task ID must be numeric"]),
                    type=random.choice(["value_error.str.regex", "value_error.not_found"])
                )
            ]
            raise HTTPException(
                status_code=422,
                detail=[error.model_dump() for error in error_details]
            )
        
        # 成功情况：返回训练进度指标字符串
        progress_indicators = [
            f"Training progress: {random.randint(10, 95)}%",
            f"Epoch {random.randint(1, 100)}/{random.randint(100, 200)} - Loss: {random.uniform(0.01, 2.0):.4f}",
            f"Accuracy: {random.uniform(0.7, 0.99):.2%} - Time remaining: {random.randint(5, 120)}min",
            f"Current step: {random.randint(100, 5000)} - Learning rate: {random.uniform(0.0001, 0.01):.6f}",
            f"Validation loss: {random.uniform(0.05, 1.5):.4f} - Best accuracy: {random.uniform(0.8, 0.99):.2%}",
            f"Training status: {'Running' if random.random() > 0.3 else 'Paused'} - GPU utilization: {random.randint(60, 95)}%"
        ]
        
        return random.choice(progress_indicators)
        
    except HTTPException:
        raise
    except Exception as e:
        # 其他错误情况
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/monitorRayCluster/node", responses={
    200: {"description": "Successful Response", "content": {"application/json": {"schema": {"type": "array", "items": {"type": "object"}}}}}
})
async def get_monitor_ray_cluster():
    """获取集群节点信息"""
    try:
        # 生成随机节点数量
        node_count = random.randint(2, 6)
        nodes = []
        
        for i in range(node_count):
            # 生成随机IP地址
            ip = f"{random.randint(10, 192)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
            
            # 生成随机节点数据
            node = {
                "ip": ip,
                "cpu_usage": round(random.uniform(0.1, 99.9), 1),
                "memory_usage": round(random.uniform(1.0, 95.0), 1),
                "disk_usage": round(random.uniform(0.5, 90.0), 1),
                "role": random.choice(["computer node", "model node", "worker node", "coordinator node"]),
                "status": random.choice(["alive", "dead", "idle"]),
                "sent": round(random.uniform(1.0, 100.0), 12),
                "received": round(random.uniform(1.0, 100.0), 12),
                "heartbeat": random.randint(1750000000000, 1760000000000)
            }
            nodes.append(node)
        
        return nodes
        
    except Exception as e:
        # 其他错误情况
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6677)
