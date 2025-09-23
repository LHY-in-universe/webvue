from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..schemas.edgeai import TrainingMetrics, TrainRequest, TrainingParameters, TrainingResponse
from common.schemas.common import BaseResponse
from database.edgeai import get_db, User, Project, Model, Node
import asyncio
import json
import httpx
import uuid

router = APIRouter()

# Active training sessions (kept in memory for real-time tracking)
active_training_sessions = {}

# Test API Configuration
TEST_API_BASE_URL = "http://localhost:6677"  # Update with actual test API URL

@router.post("/start", response_model=BaseResponse)
async def start_training(project_id: str, node_ids: List[str] = None, db: Session = Depends(get_db)):
    """
    开始训练
    """
    try:
        # Verify project exists in database
        try:
            project_id_int = int(project_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid project ID format")

        project = db.query(Project).filter(Project.id == project_id_int).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Update project status to training
        project.status = "training"
        project.progress = 0.0
        db.commit()

        session_id = f"training_{project_id}_{len(active_training_sessions)}"

        active_training_sessions[session_id] = {
            "project_id": project_id,
            "node_ids": node_ids or [],
            "status": "running",
            "progress": 0.0,
            "current_epoch": 0,
            "total_epochs": project.epoches,
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

@router.get("/config/{project_id}/")
async def get_training_config(project_id: str, db: Session = Depends(get_db)):
    """
    获取特定项目的训练配置
    """
    # Verify project exists and get its configuration from database
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    project = db.query(Project).filter(Project.id == project_id_int).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get related models for this project
    project_models = db.query(Model).filter(Model.project_id == project_id_int).all()
    model_name = project_models[0].name if project_models else "Default AI Model"

    # Build configuration from database project data (使用合并后的字段)
    config = {
        "ai_model": model_name,
        "training_alg": project.training_alg,
        "fed_alg": project.fed_alg,
        "target_accuracy": "≥85%",  # Could be stored in project or model
        "estimated_completion": f"{project.total_epochs // 50} hours",  # Estimate based on total_epochs
        "model_architecture": {
            "type": "neural_network",
            "layers": [
                {"type": "dense", "units": 128, "activation": "relu"},
                {"type": "dropout", "rate": 0.3},
                {"type": "dense", "units": 64, "activation": "relu"},
                {"type": "dropout", "rate": 0.3},
                {"type": "dense", "units": 32, "activation": "relu"},
                {"type": "dense", "units": 10, "activation": "softmax"}
            ]
        },
        "hyperparameters": {
            "batch_size": project.batch_size,
            "lr": project.lr,
            "total_epochs": project.total_epochs,
            "num_rounds": project.num_rounds,
            "optimizer": "adam",
            "loss_function": "categorical_crossentropy"
        },
        "federated_config": {
            "secure_aggregation": project.secure_aggregation,
            "num_computers": project.num_computers,
            "threshold": project.threshold,
            "num_clients": project.num_clients,
            "sample_clients": project.sample_clients,
            "max_steps": project.max_steps,
            "rounds": project.num_rounds,
            "client_fraction": 0.6,
            "local_epochs": 3
        },
        "model_dataset_config": {
            "model_name_or_path": project.model_name_or_path,
            "dataset_name": project.dataset_name,
            "dataset_sample": project.dataset_sample
        }
    }

    return {
        "project_id": project_id,
        "config": config,
        "last_updated": project.updated_time.isoformat() if project.updated_time else project.created_time.isoformat()
    }

@router.post("/start-with-api", response_model=TrainingResponse)
async def start_training_with_api(project_id: str, db: Session = Depends(get_db)):
    """
    Start training using the test API format
    """
    try:
        # Verify project exists in database
        try:
            project_id_int = int(project_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid project ID format")

        project = db.query(Project).filter(Project.id == project_id_int).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Build training parameters from project data (使用合并后的字段)
        training_params = TrainingParameters(
            training_alg=project.training_alg,
            fed_alg=project.fed_alg,
            secure_aggregation=project.secure_aggregation,
            num_computers=project.num_computers,
            threshold=project.threshold,
            num_rounds=project.num_rounds,
            num_clients=project.num_clients,
            sample_clients=project.sample_clients,
            max_steps=project.max_steps,
            lr=project.lr,
            model_name_or_path=project.model_name_or_path,
            dataset_name=project.dataset_name,
            dataset_sample=project.dataset_sample
        )

        train_request = TrainRequest(parameters=training_params)

        # Call the test API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{TEST_API_BASE_URL}/train",
                json=train_request.model_dump(),
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                # Get task ID from response
                task_id = response.json() if isinstance(response.json(), str) else str(uuid.uuid4())

                # Update project with task ID and status
                project.task_id = task_id
                project.status = "training"
                project.progress = 0.0
                db.commit()

                # Store in active sessions for monitoring
                active_training_sessions[task_id] = {
                    "project_id": project_id,
                    "task_id": task_id,
                    "status": "running",
                    "progress": 0.0,
                    "started_at": "2024-01-15T10:30:00Z"
                }

                return TrainingResponse(
                    task_id=task_id,
                    status="started",
                    message=f"Training started successfully for project {project.name}"
                )
            elif response.status_code == 422:
                # Validation error from test API
                error_detail = response.json().get("detail", "Validation error")
                raise HTTPException(status_code=422, detail=f"Training API validation error: {error_detail}")
            else:
                raise HTTPException(status_code=500, detail=f"Training API error: {response.status_code}")

    except httpx.TimeoutException:
        raise HTTPException(status_code=500, detail="Training API timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Training API connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/status/{task_id}")
async def get_training_status(task_id: str):
    """
    Get training status from test API
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{TEST_API_BASE_URL}/tasks/{task_id}")

            if response.status_code == 200:
                status = response.json() if isinstance(response.json(), str) else "unknown"
                return {"task_id": task_id, "status": status}
            elif response.status_code == 422:
                error_detail = response.json().get("detail", "Validation error")
                raise HTTPException(status_code=422, detail=f"API validation error: {error_detail}")
            else:
                raise HTTPException(status_code=500, detail=f"API error: {response.status_code}")

    except httpx.TimeoutException:
        raise HTTPException(status_code=500, detail="API timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"API connection error: {str(e)}")

@router.delete("/stop/{task_id}")
async def stop_training_task(task_id: str, db: Session = Depends(get_db)):
    """
    Stop training task using test API
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.delete(f"{TEST_API_BASE_URL}/tasks/{task_id}")

            if response.status_code == 200:
                message = response.json() if isinstance(response.json(), str) else "Task stopped"

                # Update local project status
                project = db.query(Project).filter(Project.task_id == task_id).first()
                if project:
                    project.status = "paused"
                    db.commit()

                # Remove from active sessions
                active_training_sessions.pop(task_id, None)

                return {"task_id": task_id, "message": message}
            elif response.status_code == 422:
                error_detail = response.json().get("detail", "Validation error")
                raise HTTPException(status_code=422, detail=f"API validation error: {error_detail}")
            else:
                raise HTTPException(status_code=500, detail=f"API error: {response.status_code}")

    except httpx.TimeoutException:
        raise HTTPException(status_code=500, detail="API timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"API connection error: {str(e)}")

@router.get("/monitor/{task_id}")
async def get_training_monitor(task_id: str):
    """
    Get training progress from test API
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{TEST_API_BASE_URL}/monitor/{task_id}")

            if response.status_code == 200:
                monitor_data = response.json() if isinstance(response.json(), str) else "No monitor data"
                return {"task_id": task_id, "monitor_data": monitor_data}
            elif response.status_code == 422:
                error_detail = response.json().get("detail", "Validation error")
                raise HTTPException(status_code=422, detail=f"API validation error: {error_detail}")
            else:
                raise HTTPException(status_code=500, detail=f"API error: {response.status_code}")

    except httpx.TimeoutException:
        raise HTTPException(status_code=500, detail="API timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"API connection error: {str(e)}")
