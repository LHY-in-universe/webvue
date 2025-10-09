from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
from ..schemas.training import (
    TrainingStartRequest,
    TrainingStopRequest,
    LocalTrainingRequest,
    FederatedRound,
    MPCTrainingRequest,
    TrainingMetrics
)
from common.schemas.common import BaseResponse
import asyncio
import json

router = APIRouter()

# Mock training sessions
active_training_sessions = {}

@router.post("/start", response_model=BaseResponse)
async def start_training(request: TrainingStartRequest):
    """
    开始训练
    """
    try:
        # 模拟训练开始
        session_id = f"session_{request.project_id}_{len(active_training_sessions)}"
        
        active_training_sessions[session_id] = {
            "project_id": request.project_id,
            "training_type": request.training_type.value,
            "status": "running",
            "progress": 0.0,
            "current_epoch": 0,
            "total_epochs": 100,
            "metrics": {
                "accuracy": 0.0,
                "loss": 1.0,
                "f1_score": 0.0
            },
            "config": request.config or {}
        }
        
        return BaseResponse(
            success=True,
            message=f"Training started for project {request.project_id}"
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            error=str(e)
        )

@router.post("/stop", response_model=BaseResponse)
async def stop_training(request: TrainingStopRequest):
    """
    停止训练
    """
    try:
        # 查找并停止相关训练会话
        sessions_to_stop = [
            session_id for session_id, session in active_training_sessions.items()
            if session["project_id"] == request.project_id
        ]
        
        for session_id in sessions_to_stop:
            active_training_sessions[session_id]["status"] = "stopped"
        
        return BaseResponse(
            success=True,
            message=f"Training stopped for project {request.project_id}"
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            error=str(e)
        )

@router.post("/local", response_model=BaseResponse)
async def start_local_training(request: LocalTrainingRequest):
    """
    开始本地训练
    """
    try:
        # 模拟本地训练
        session_id = f"local_{request.project_id}"
        
        active_training_sessions[session_id] = {
            "project_id": request.project_id,
            "training_type": "local",
            "status": "running",
            "progress": 0.0,
            "current_epoch": 0,
            "total_epochs": 100,
            "metrics": {
                "accuracy": 0.0,
                "loss": 1.0,
                "f1_score": 0.0
            },
            "config": request.training_config,
            "dataset_config": request.dataset_config
        }
        
        return BaseResponse(
            success=True,
            message="Local training started successfully"
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            error=str(e)
        )

@router.post("/federated/start", response_model=BaseResponse)
async def start_federated_training(request: TrainingStartRequest):
    """
    开始联邦学习训练
    """
    try:
        session_id = f"federated_{request.project_id}"
        
        active_training_sessions[session_id] = {
            "project_id": request.project_id,
            "training_type": "federated",
            "status": "running",
            "progress": 0.0,
            "current_round": 0,
            "total_rounds": 10,
            "participants": [],
            "metrics": {
                "global_accuracy": 0.0,
                "local_accuracies": {},
                "loss": 1.0
            },
            "config": request.config or {}
        }
        
        return BaseResponse(
            success=True,
            message="Federated training started successfully"
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            error=str(e)
        )

@router.post("/mpc/start", response_model=BaseResponse)
async def start_mpc_training(request: MPCTrainingRequest):
    """
    开始MPC训练
    """
    try:
        session_id = f"mpc_{request.project_id}"
        
        active_training_sessions[session_id] = {
            "project_id": request.project_id,
            "training_type": "mpc",
            "status": "running",
            "progress": 0.0,
            "participants": request.participants,
            "privacy_level": request.privacy_level,
            "encryption_method": request.encryption_method,
            "threshold": request.threshold,
            "metrics": {
                "accuracy": 0.0,
                "privacy_loss": 0.0,
                "communication_rounds": 0
            },
            "config": {}
        }
        
        return BaseResponse(
            success=True,
            message="MPC training started successfully"
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            error=str(e)
        )

@router.get("/sessions")
async def get_training_sessions():
    """
    获取所有训练会话
    """
    # 使用真正的训练服务获取会话
    tasks = await federated_trainer.get_tasks_list()
    sessions = []
    
    for task_id, status in tasks.items():
        task_status = await federated_trainer.get_training_status(task_id)
        if task_status:
            sessions.append({
                "task_id": task_id,
                "status": status,
                "current_round": task_status.get("current_round", 0),
                "total_rounds": task_status.get("total_rounds", 0),
                "progress": task_status.get("progress", 0.0),
                "metrics": task_status.get("metrics", {})
            })
    
    return {
        "sessions": sessions,
        "total": len(sessions)
    }

@router.get("/sessions/{project_id}")
async def get_project_training_sessions(project_id: str):
    """
    获取特定项目的训练会话
    """
    project_sessions = [
        session for session in active_training_sessions.values()
        if session["project_id"] == project_id
    ]
    
    return {
        "sessions": project_sessions,
        "total": len(project_sessions)
    }

@router.get("/metrics/{project_id}")
async def get_training_metrics(project_id: str):
    """
    获取训练指标
    """
    # 使用真正的训练服务获取指标
    tasks = await federated_trainer.get_tasks_list()
    running_tasks = [task_id for task_id, status in tasks.items() if status == "running"]
    
    if not running_tasks:
        raise HTTPException(status_code=404, detail="No active training session found")
    
    # 获取第一个运行中任务的指标
    task_id = running_tasks[0]
    task_status = await federated_trainer.get_training_status(task_id)
    
    if not task_status:
        raise HTTPException(status_code=404, detail="Training session not found")
    
    return {
        "project_id": project_id,
        "task_id": task_id,
        "metrics": task_status["metrics"],
        "progress": task_status["progress"],
        "current_round": task_status.get("current_round", 0),
        "total_rounds": task_status.get("total_rounds", 100)
    }

# 导入真正的训练服务
from training_service.federated_trainer import federated_trainer, TrainingConfig

# 新增的API端点，用于支持前端Training Controls功能

@router.post("/train")
async def start_training_with_parameters(request: Dict[str, Any]):
    """
    启动训练（支持参数配置）
    """
    try:
        # 从请求中提取参数
        parameters = request.get("parameters", {})
        
        # 创建训练配置
        config = TrainingConfig(
            model_name=parameters.get("model_name", "sshleifer/tiny-gpt2"),
            dataset_name=parameters.get("dataset_name", "vicgalle/alpaca-gpt4"),
            learning_rate=float(parameters.get("learning_rate", 1e-4)),
            num_rounds=int(parameters.get("num_rounds", 10)),
            num_clients=int(parameters.get("num_clients", 2)),
            sample_clients_per_round=int(parameters.get("sample_clients_per_round", 2)),
            batch_size=int(parameters.get("batch_size", 32)),
            epochs_per_round=int(parameters.get("epochs_per_round", 1))
        )
        
        # 启动真正的联邦学习训练
        task_id = await federated_trainer.start_training(config)
        
        return {
            "task_id": task_id,
            "status": "started",
            "message": "Federated training started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitor/{task_id}")
async def monitor_training(task_id: str):
    """
    监控训练进度
    """
    # 使用真正的训练服务获取状态
    task_status = await federated_trainer.get_training_status(task_id)
    
    if not task_status:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "task_id": task_id,
        "current_round": task_status["current_round"],
        "total_rounds": task_status["total_rounds"],
        "loss": task_status["metrics"]["loss"],
        "accuracy": task_status["metrics"]["accuracy"],
        "status": task_status["status"]
    }

@router.get("/tasksList")
async def get_tasks_list():
    """
    获取任务列表
    """
    # 使用真正的训练服务获取任务列表
    tasks = await federated_trainer.get_tasks_list()
    return tasks

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """
    删除任务
    """
    # 使用真正的训练服务删除任务
    success = await federated_trainer.delete_task(task_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "status": "deleted",
        "message": f"Task {task_id} deleted successfully"
    }

@router.get("/monitorRayCluster/node")
async def get_ray_cluster_nodes():
    """
    获取Ray集群节点信息
    """
    # 使用真正的训练服务获取集群节点信息
    nodes = await federated_trainer.get_cluster_nodes()
    return nodes

@router.get("/roundProgress/{task_id}")
async def get_round_progress(task_id: str):
    """
    获取轮次进度
    """
    # 使用真正的训练服务获取轮次进度
    progress_data = await federated_trainer.get_round_progress(task_id)
    
    if not progress_data and task_id not in await federated_trainer.get_tasks_list():
        raise HTTPException(status_code=404, detail="Task not found")
    
    return progress_data

@router.websocket("/ws/{project_id}")
async def training_websocket(websocket: WebSocket, project_id: str):
    """
    训练实时监控WebSocket
    """
    await websocket.accept()
    
    try:
        while True:
            # 使用真正的训练服务获取实时数据
            tasks = await federated_trainer.get_tasks_list()
            running_tasks = [task_id for task_id, status in tasks.items() if status == "running"]
            
            if running_tasks:
                # 获取第一个运行中任务的实时状态
                task_id = running_tasks[0]
                task_status = await federated_trainer.get_training_status(task_id)
                
                if task_status:
                    # 发送真实的训练数据
                    await websocket.send_text(json.dumps({
                        "type": "training_update",
                        "project_id": project_id,
                        "task_id": task_id,
                        "data": {
                            "progress": task_status["progress"],
                            "current_round": task_status["current_round"],
                            "total_rounds": task_status["total_rounds"],
                            "metrics": task_status["metrics"],
                            "status": task_status["status"]
                        }
                    }))
            
            await asyncio.sleep(2)  # 每2秒发送一次更新
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for project {project_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()
