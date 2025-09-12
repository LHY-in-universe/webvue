from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
from ..schemas.edgeai import TrainingMetrics
from common.schemas.common import BaseResponse
import asyncio
import json

router = APIRouter()

# Mock training sessions
active_training_sessions = {}

@router.post("/start", response_model=BaseResponse)
async def start_training(project_id: str, node_ids: List[str] = None):
    """
    开始训练
    """
    try:
        session_id = f"training_{project_id}_{len(active_training_sessions)}"
        
        active_training_sessions[session_id] = {
            "project_id": project_id,
            "node_ids": node_ids or [],
            "status": "running",
            "progress": 0.0,
            "current_epoch": 0,
            "total_epochs": 100,
            "metrics": {
                "accuracy": 0.0,
                "loss": 1.0,
                "f1_score": 0.0
            },
            "started_at": "2024-01-15T10:30:00Z"
        }
        
        return BaseResponse(
            success=True,
            message=f"Training started for project {project_id}"
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            error=str(e)
        )

@router.post("/stop", response_model=BaseResponse)
async def stop_training(project_id: str):
    """
    停止训练
    """
    try:
        sessions_to_stop = [
            session_id for session_id, session in active_training_sessions.items()
            if session["project_id"] == project_id
        ]
        
        for session_id in sessions_to_stop:
            active_training_sessions[session_id]["status"] = "stopped"
        
        return BaseResponse(
            success=True,
            message=f"Training stopped for project {project_id}"
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
        "current_epoch": latest_session["current_epoch"],
        "total_epochs": latest_session["total_epochs"]
    }

@router.websocket("/ws/{project_id}")
async def training_websocket(websocket: WebSocket, project_id: str):
    """
    训练实时监控WebSocket
    """
    await websocket.accept()
    
    try:
        while True:
            # 查找项目训练会话
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
                    "type": "training_update",
                    "project_id": project_id,
                    "data": {
                        "progress": session["progress"],
                        "current_epoch": session["current_epoch"],
                        "total_epochs": session["total_epochs"],
                        "metrics": session["metrics"],
                        "status": session["status"]
                    }
                }))
            else:
                # 没有活跃训练会话
                await websocket.send_text(json.dumps({
                    "type": "no_training",
                    "project_id": project_id,
                    "message": "No active training session found"
                }))
            
            await asyncio.sleep(2)  # 每2秒发送一次更新
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for project {project_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

@router.post("/batch-start")
async def start_batch_training(project_ids: List[str], node_ids: List[str] = None):
    """
    批量开始训练
    """
    results = []
    
    for project_id in project_ids:
        try:
            session_id = f"batch_training_{project_id}_{len(active_training_sessions)}"
            
            active_training_sessions[session_id] = {
                "project_id": project_id,
                "node_ids": node_ids or [],
                "status": "running",
                "progress": 0.0,
                "current_epoch": 0,
                "total_epochs": 100,
                "metrics": {
                    "accuracy": 0.0,
                    "loss": 1.0,
                    "f1_score": 0.0
                },
                "started_at": "2024-01-15T10:30:00Z"
            }
            
            results.append({
                "project_id": project_id,
                "success": True,
                "message": "Training started"
            })
        except Exception as e:
            results.append({
                "project_id": project_id,
                "success": False,
                "error": str(e)
            })
    
    return {
        "results": results,
        "total_started": len([r for r in results if r["success"]])
    }

@router.post("/batch-stop")
async def stop_batch_training(project_ids: List[str]):
    """
    批量停止训练
    """
    results = []
    
    for project_id in project_ids:
        try:
            sessions_to_stop = [
                session_id for session_id, session in active_training_sessions.items()
                if session["project_id"] == project_id
            ]
            
            for session_id in sessions_to_stop:
                active_training_sessions[session_id]["status"] = "stopped"
            
            results.append({
                "project_id": project_id,
                "success": True,
                "message": "Training stopped"
            })
        except Exception as e:
            results.append({
                "project_id": project_id,
                "success": False,
                "error": str(e)
            })
    
    return {
        "results": results,
        "total_stopped": len([r for r in results if r["success"]])
    }
