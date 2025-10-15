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
    return {
        "sessions": list(active_training_sessions.values()),
        "total": len(active_training_sessions)
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
    project_sessions = [
        session for session in active_training_sessions.values()
        if session["project_id"] == project_id and session["status"] == "running"
    ]
    
    if not project_sessions:
        raise HTTPException(status_code=404, detail="No active training session found")
    
    latest_session = project_sessions[0]
    return {
        "project_id": project_id,
        "metrics": latest_session["metrics"],
        "progress": latest_session["progress"],
        "current_epoch": latest_session.get("current_epoch", 0),
        "total_epochs": latest_session.get("total_epochs", 100)
    }

@router.websocket("/ws/{project_id}")
async def training_websocket(websocket: WebSocket, project_id: str):
    """
    训练实时监控WebSocket
    """
    await websocket.accept()
    
    try:
        while True:
            # 模拟实时训练数据
            project_sessions = [
                session for session in active_training_sessions.values()
                if session["project_id"] == project_id and session["status"] == "running"
            ]
            
            if project_sessions:
                session = project_sessions[0]
                
                # 模拟训练进度更新
                if session["progress"] < 100:
                    session["progress"] += 1.0
                    session["current_epoch"] = int(session["progress"])
                    
                    # 模拟指标更新
                    session["metrics"]["accuracy"] = min(95.0, session["metrics"]["accuracy"] + 0.5)
                    session["metrics"]["loss"] = max(0.1, session["metrics"]["loss"] - 0.01)
                    session["metrics"]["f1_score"] = min(95.0, session["metrics"]["f1_score"] + 0.3)
                
                # 发送更新数据
                await websocket.send_text(json.dumps({
                    "type": "training_progress",
                    "payload": {
                        "project_id": project_id,
                        "progress": session["progress"],
                        "current_epoch": session["current_epoch"],
                        "total_epochs": session["total_epochs"],
                        "metrics": session["metrics"],
                        "status": session["status"]
                    }
                }))
            
            await asyncio.sleep(2)  # 每2秒发送一次更新
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for project {project_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()
