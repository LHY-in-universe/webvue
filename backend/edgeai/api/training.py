from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..schemas.edgeai import TrainingMetrics, TrainRequest, TrainingParameters, TrainingResponse
from common.schemas.common import BaseResponse
from database.edgeai import get_db, User, Project, Model, Node, TaskQueue
from ..scheduler.task_scheduler import task_scheduler
import asyncio
import json
import httpx
import uuid
from datetime import datetime, timedelta
import logging
import subprocess
import sys

router = APIRouter()

# Active training sessions (kept in memory for real-time tracking)
active_training_sessions = {}

# Background polling tasks
polling_tasks = {}

# Global background tasks for periodic sync
global_sync_task = None

# Test API Configuration
TEST_API_BASE_URL = "http://127.0.0.1:6677"  # Update with actual test API URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_testapi_health():
    """
    Check if TestAPI is accessible
    """
    try:
        # First try with httpx
        async with httpx.AsyncClient(
            timeout=5.0,
            follow_redirects=True,
            verify=False
        ) as client:
            response = await client.get(f"{TEST_API_BASE_URL}/docs")
            if response.status_code == 200:
                logger.info("TestAPI health check passed via httpx")
                return True, "httpx"
    except Exception as e:
        logger.warning(f"httpx health check failed: {e}")

    # Fallback to curl
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"{TEST_API_BASE_URL}/docs"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip() == "200":
            logger.info("TestAPI health check passed via curl")
            return True, "curl"
    except Exception as e:
        logger.warning(f"curl health check failed: {e}")

    logger.error("TestAPI health check failed with both httpx and curl")
    return False, None

async def make_http_request(method: str, url: str, **kwargs):
    """
    Make HTTP request with fallback to curl
    """
    logger.info(f"Making {method} request to {url}")

    # Try httpx first
    try:
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            verify=False,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        ) as client:
            if method.upper() == "GET":
                response = await client.get(url, **kwargs)
            elif method.upper() == "POST":
                response = await client.post(url, **kwargs)
            elif method.upper() == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise ValueError(f"Unsupported method: {method}")

            logger.info(f"httpx {method} {url} -> {response.status_code}")

            # If httpx gets a 5xx status code, treat it as a failure and try curl fallback
            if response.status_code >= 500:
                logger.warning(f"httpx got error status {response.status_code}, trying curl fallback")
                raise httpx.HTTPStatusError("Server error response", request=response.request, response=response)

            return response.status_code, response.json() if response.content else None

    except Exception as e:
        logger.warning(f"httpx {method} request failed: {e}")

        # Fallback to curl
        try:
            logger.info(f"Falling back to curl for {method} {url}")

            if method.upper() == "GET":
                cmd = ["curl", "-s", "-X", "GET", url]
            elif method.upper() == "POST":
                json_data = kwargs.get('json', {})
                cmd = ["curl", "-s", "-X", "POST", "-H", "Content-Type: application/json",
                       "-d", json.dumps(json_data), url]
            elif method.upper() == "DELETE":
                cmd = ["curl", "-s", "-X", "DELETE", url]
            else:
                raise ValueError(f"Unsupported method: {method}")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                try:
                    response_data = json.loads(result.stdout) if result.stdout.strip() else None
                except json.JSONDecodeError:
                    response_data = result.stdout.strip()

                logger.info(f"curl {method} {url} -> success")
                return 200, response_data
            else:
                logger.error(f"curl {method} failed: {result.stderr}")
                return 500, None

        except Exception as curl_e:
            logger.error(f"curl fallback failed: {curl_e}")
            return 502, None

async def sync_nodes_from_testapi(db: Session):
    """
    Sync node information from testapi with enhanced error handling
    """
    try:
        logger.info("Starting node synchronization from TestAPI")
        status_code, nodes_data = await make_http_request("GET", f"{TEST_API_BASE_URL}/monitorRayCluster/node")

        if status_code == 200 and nodes_data:
            if not isinstance(nodes_data, list):
                logger.error(f"Expected list of nodes, got {type(nodes_data)}: {nodes_data}")
                return False

            logger.info(f"Retrieved {len(nodes_data)} nodes from testapi")
            updated_count = 0
            created_count = 0

            for i, node_data in enumerate(nodes_data):
                try:
                    # Validate node data
                    if not isinstance(node_data, dict) or "ip" not in node_data:
                        logger.warning(f"Invalid node data at index {i}: {node_data}")
                        continue

                    ip_address = node_data["ip"]

                    # Find existing node by IP or create new one
                    node = db.query(Node).filter(Node.path_ipv4 == ip_address).first()

                    if node:
                        # Update existing node with validation
                        try:
                            node.cpu_usage = round(float(node_data.get("cpu_usage", 0.0)), 2)
                            node.memory_usage = round(float(node_data.get("memory_usage", 0.0)), 2)
                            node.disk_usage = round(float(node_data.get("disk_usage", 0.0)), 2)
                            node.role = str(node_data.get("role", "worker"))
                            node.state = str(node_data.get("status", "idle"))
                            node.sent = round(float(node_data.get("sent", 0.0)), 2)
                            node.received = round(float(node_data.get("received", 0.0)), 2)
                            node.heartbeat = str(node_data.get("heartbeat", ""))
                            node.last_updated_time = datetime.utcnow()
                            updated_count += 1
                            logger.debug(f"Updated existing node {node.name} ({node.path_ipv4})")
                        except (ValueError, TypeError) as ve:
                            logger.warning(f"Invalid data types for node {ip_address}: {ve}")
                            continue
                    else:
                        # Create new node with validation
                        try:
                            new_node = Node(
                                user_id=1,  # Default user, should be parameterized
                                name=f"Node-{ip_address}",
                                path_ipv4=ip_address,
                                cpu_usage=round(float(node_data.get("cpu_usage", 0.0)), 2),
                                memory_usage=round(float(node_data.get("memory_usage", 0.0)), 2),
                                disk_usage=round(float(node_data.get("disk_usage", 0.0)), 2),
                                role=str(node_data.get("role", "worker")),
                                state=str(node_data.get("status", "idle")),
                                sent=round(float(node_data.get("sent", 0.0)), 2),
                                received=round(float(node_data.get("received", 0.0)), 2),
                                heartbeat=str(node_data.get("heartbeat", ""))
                            )
                            db.add(new_node)
                            created_count += 1
                            logger.debug(f"Created new node {new_node.name} ({new_node.path_ipv4})")
                        except (ValueError, TypeError) as ve:
                            logger.warning(f"Invalid data types for new node {ip_address}: {ve}")
                            continue

                except Exception as node_error:
                    logger.error(f"Error processing node at index {i}: {node_error}")
                    continue

            # Commit changes
            try:
                db.commit()
                logger.info(f"Node sync completed successfully: {updated_count} updated, {created_count} created")
                return True
            except Exception as commit_error:
                logger.error(f"Failed to commit node changes: {commit_error}")
                db.rollback()
                return False

        elif status_code == 200:
            logger.warning("TestAPI returned empty or null nodes data")
            return False
        else:
            logger.error(f"Failed to get nodes from testapi: HTTP {status_code}")
            return False

    except Exception as e:
        logger.error(f"Critical error syncing nodes from testapi: {str(e)}")
        # Rollback any changes if there was an error
        try:
            db.rollback()
        except:
            pass
        return False

def validate_training_status(status_response):
    """
    Validate and normalize training status from TestAPI response
    """
    # Valid training statuses
    valid_statuses = ["running", "completed", "failed", "cancelled", "paused", "pending"]

    # If response is a string, check if it's valid
    if isinstance(status_response, str):
        if status_response in valid_statuses:
            return status_response
        else:
            logger.warning(f"Unknown status string: {status_response}, defaulting to 'running'")
            return "running"

    # If response is a dict (error response), extract meaningful status
    if isinstance(status_response, dict):
        if "detail" in status_response:
            logger.warning(f"TestAPI returned error: {status_response}, defaulting to 'failed'")
            return "failed"

    # For any other type, default to running
    logger.warning(f"Unexpected status response type: {type(status_response)}, defaulting to 'running'")
    return "running"

async def poll_training_status(task_id: str, project_id: str, db_session_factory):
    """
    Background task to poll training status and sync node data
    """
    logger.info(f"Starting polling for task {task_id}, project {project_id}")

    while task_id in polling_tasks:
        try:
            # Create new database session for this background task
            db = db_session_factory()

            # Poll training status
            status_code, status_response = await make_http_request("GET", f"{TEST_API_BASE_URL}/tasks/{task_id}")

            # Validate and normalize the status
            if status_code == 200:
                normalized_status = validate_training_status(status_response)
            elif status_code >= 500:
                # TestAPI server error - keep current status or mark as failed if unknown
                logger.warning(f"TestAPI server error (status {status_code}), keeping current project status")
                normalized_status = None  # Don't update status on server errors
            elif status_code == 422:
                # Validation error - mark as failed
                logger.warning(f"TestAPI validation error for task {task_id}")
                normalized_status = "failed"
            else:
                # Other errors - mark as failed
                logger.warning(f"TestAPI returned status {status_code} for task {task_id}")
                normalized_status = "failed"

            # Update project status in database only if we have a valid status
            if normalized_status:
                project = db.query(Project).filter(Project.id == int(project_id)).first()
                if project:
                    project.status = normalized_status
                    # Update progress based on status
                    if normalized_status == "completed":
                        project.progress = round(100.0, 2)
                    elif normalized_status == "running":
                        project.progress = round(min(project.progress + 5.0, 95.0), 2)  # Gradual progress
                    elif normalized_status == "failed":
                        project.progress = round(0.0, 2)
                    elif normalized_status == "cancelled":
                        project.progress = round(0.0, 2)

                    db.commit()
                    logger.info(f"Updated project {project_id} status to {normalized_status}")

            # Sync node data from testapi
            await sync_nodes_from_testapi(db)

            db.close()

            # Check if training is completed or failed (use the normalized status)
            if normalized_status and normalized_status in ["completed", "failed", "cancelled"]:
                logger.info(f"Training {task_id} finished with status: {normalized_status}")
                break

            # Wait before next poll
            await asyncio.sleep(10)  # Poll every 10 seconds

        except Exception as e:
            logger.error(f"Error in polling task {task_id}: {str(e)}")
            await asyncio.sleep(10)  # Wait before retrying

    # Cleanup
    if task_id in polling_tasks:
        polling_tasks.pop(task_id)
    logger.info(f"Stopped polling for task {task_id}")

async def periodic_sync_task(db_session_factory):
    """
    定期同步TestAPI数据到数据库的全局后台任务
    """
    logger.info("Started periodic sync task for TestAPI data synchronization")

    while True:
        try:
            # 创建新的数据库会话
            db = db_session_factory()

            # 同步节点数据
            success = await sync_nodes_from_testapi(db)
            if success:
                logger.info("Periodic node data sync completed successfully")
            else:
                logger.warning("Periodic node data sync failed")

            # 检查是否有运行中的训练任务需要状态同步
            running_projects = db.query(Project).filter(
                Project.status.in_(["training", "running"])
            ).all()

            for project in running_projects:
                if project.task_id:
                    try:
                        logger.debug(f"Checking status for project {project.id} with task_id {project.task_id}")
                        # 获取训练状态
                        status_code, status_response = await make_http_request(
                            "GET", f"{TEST_API_BASE_URL}/tasks/{project.task_id}"
                        )

                        if status_code == 200:
                            normalized_status = validate_training_status(status_response)
                            if normalized_status and normalized_status != project.status:
                                old_status = project.status
                                project.status = normalized_status

                                # 更新进度
                                if normalized_status == "completed":
                                    project.progress = round(100.0, 2)
                                elif normalized_status == "running":
                                    project.progress = round(min(project.progress + 2.0, 95.0), 2)
                                elif normalized_status in ["failed", "cancelled"]:
                                    project.progress = round(0.0, 2)

                                logger.info(f"Updated project {project.id} status: {old_status} → {normalized_status} (progress: {project.progress}%)")
                            else:
                                logger.debug(f"Project {project.id} status unchanged: {project.status}")
                        else:
                            logger.warning(f"Failed to get status for project {project.id}: HTTP {status_code}")

                    except Exception as project_error:
                        logger.error(f"Error updating project {project.id} status: {project_error}")
                        continue

            db.commit()
            db.close()

            # 等待30秒后继续下一轮同步
            await asyncio.sleep(30)

        except Exception as e:
            logger.error(f"Error in periodic sync task: {str(e)}")
            await asyncio.sleep(30)  # 出错时也等待30秒

async def start_global_sync_task():
    """
    启动全局同步任务
    """
    global global_sync_task
    if global_sync_task is None or global_sync_task.done():
        from database.edgeai.database import SessionLocal
        global_sync_task = asyncio.create_task(periodic_sync_task(SessionLocal))
        logger.info("Global sync task started")

async def stop_global_sync_task():
    """
    停止全局同步任务
    """
    global global_sync_task
    if global_sync_task and not global_sync_task.done():
        global_sync_task.cancel()
        try:
            await global_sync_task
        except asyncio.CancelledError:
            pass
        global_sync_task = None
        logger.info("Global sync task stopped")

@router.post("/start/{project_id}", response_model=TrainingResponse)
async def start_training(project_id: str, node_ids: List[str] = None, priority: int = 5, db: Session = Depends(get_db)):
    """
    启动训练任务 - 使用任务队列和并发控制
    """
    try:
        # 确保任务调度器正在运行
        if not task_scheduler._is_running:
            await task_scheduler.start()

        # 确保全局同步任务正在运行
        await start_global_sync_task()

        # 将任务添加到队列而不是直接执行
        try:
            queue_task = task_scheduler.add_task_to_queue(
                project_id=int(project_id),
                priority=priority,
                task_config={
                    'node_ids': node_ids or [],
                    'requested_at': datetime.utcnow().isoformat()
                },
                db=db
            )

            return TrainingResponse(
                success=True,
                message=f"Training task queued successfully. Queue position: {queue_task.id}",
                task_id=str(queue_task.id),
                status="queued",
                progress=0.0
            )

        except ValueError as e:
            # 项目不存在或已有任务在队列中
            raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Failed to queue training task: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to queue training task: {str(e)}")

@router.post("/start", response_model=BaseResponse)
async def start_training_legacy(project_id: str, node_ids: List[str] = None, db: Session = Depends(get_db)):
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
        project.progress = round(0.0, 2)
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
            else:
                # 没有活跃训练会话
                await websocket.send_text(json.dumps({
                    "type": "no_training",
                    "payload": {
                        "project_id": project_id,
                        "message": "No active training session found"
                    }
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

        # Check TestAPI health first
        health_ok, method = await check_testapi_health()
        if not health_ok:
            raise HTTPException(status_code=503, detail="TestAPI is not accessible")

        logger.info(f"TestAPI is accessible via {method}")

        # Call the test API
        status_code, response_data = await make_http_request(
            "POST",
            f"{TEST_API_BASE_URL}/train",
            json=train_request.dict()
        )

        if status_code == 200:
            # Get task ID from response
            task_id = response_data if isinstance(response_data, str) else str(uuid.uuid4())

            # Update project with task ID and status
            project.task_id = task_id
            project.status = "training"
            project.progress = round(0.0, 2)
            db.commit()

            # Store in active sessions for monitoring
            active_training_sessions[task_id] = {
                "project_id": project_id,
                "task_id": task_id,
                "status": "running",
                "progress": 0.0,
                "started_at": datetime.utcnow().isoformat()
            }

            # Start background polling task
            from database.edgeai.database import SessionLocal
            polling_tasks[task_id] = asyncio.create_task(
                poll_training_status(task_id, project_id, SessionLocal)
            )
            logger.info(f"Started background polling for task {task_id}")

            return TrainingResponse(
                task_id=task_id,
                status="started",
                message=f"Training started successfully for project {project.name}"
            )
        elif status_code == 422:
            # Validation error from test API
            error_detail = response_data.get("detail", "Validation error") if isinstance(response_data, dict) else "Validation error"
            raise HTTPException(status_code=422, detail=f"Training API validation error: {error_detail}")
        else:
            raise HTTPException(status_code=500, detail=f"Training API error: status {status_code}")

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

                # Stop background polling task
                if task_id in polling_tasks:
                    polling_tasks[task_id].cancel()
                    polling_tasks.pop(task_id)
                    logger.info(f"Stopped polling task for {task_id}")

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

@router.post("/sync-nodes")
async def sync_nodes_manually(db: Session = Depends(get_db)):
    """
    Manually sync node data from test API
    """
    try:
        success = await sync_nodes_from_testapi(db)
        if success:
            return BaseResponse(success=True, message="Nodes synchronized successfully")
        else:
            return BaseResponse(success=False, error="Failed to sync nodes from test API")
    except Exception as e:
        return BaseResponse(success=False, error=f"Error syncing nodes: {str(e)}")

@router.get("/polling-status")
async def get_polling_status():
    """
    Get status of all active polling tasks
    """
    active_polls = []
    for task_id, task in polling_tasks.items():
        active_polls.append({
            "task_id": task_id,
            "done": task.done(),
            "cancelled": task.cancelled()
        })

    return {
        "active_polling_tasks": len(polling_tasks),
        "details": active_polls,
        "active_sessions": len(active_training_sessions)
    }

@router.post("/start-sync")
async def start_sync_task():
    """
    手动启动全局同步任务
    """
    try:
        await start_global_sync_task()
        return BaseResponse(success=True, message="Global sync task started")
    except Exception as e:
        return BaseResponse(success=False, error=f"Failed to start sync task: {str(e)}")

@router.post("/stop-sync")
async def stop_sync_task():
    """
    停止全局同步任务
    """
    try:
        await stop_global_sync_task()
        return BaseResponse(success=True, message="Global sync task stopped")
    except Exception as e:
        return BaseResponse(success=False, error=f"Failed to stop sync task: {str(e)}")

@router.get("/sync-status")
async def get_sync_status():
    """
    获取同步任务状态
    """
    global global_sync_task
    return {
        "global_sync_active": global_sync_task is not None and not global_sync_task.done(),
        "active_polling_tasks": len(polling_tasks),
        "active_sessions": len(active_training_sessions)
    }

@router.get("/health-check")
async def health_check():
    """
    Check system health including TestAPI connectivity
    """
    try:
        # Check TestAPI health
        testapi_health, method = await check_testapi_health()

        # Check database connectivity
        db_health = True
        try:
            from database.edgeai.database import SessionLocal
            from sqlalchemy import text
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
        except Exception as e:
            db_health = False
            logger.error(f"Database health check failed: {e}")

        health_status = {
            "system": "healthy" if testapi_health and db_health else "unhealthy",
            "testapi": {
                "status": "healthy" if testapi_health else "unhealthy",
                "method": method if testapi_health else None,
                "url": TEST_API_BASE_URL
            },
            "database": {
                "status": "healthy" if db_health else "unhealthy"
            },
            "active_tasks": len(polling_tasks),
            "active_sessions": len(active_training_sessions)
        }

        return health_status

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "system": "error",
            "error": str(e)
        }

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


# ===============================
# 任务队列管理API接口
# ===============================

@router.get("/queue/status")
async def get_queue_status(db: Session = Depends(get_db)):
    """
    获取任务队列状态
    """
    try:
        # 确保任务调度器已启动
        if not task_scheduler._is_running:
            await task_scheduler.start()

        status = task_scheduler.get_queue_status(db)
        return {
            "success": True,
            "data": status
        }
    except Exception as e:
        logger.error(f"Failed to get queue status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get queue status: {str(e)}")


@router.post("/queue/cancel/{queue_task_id}")
async def cancel_queued_task(queue_task_id: int, db: Session = Depends(get_db)):
    """
    取消排队中的任务
    """
    try:
        success = task_scheduler.cancel_queued_task(queue_task_id, db)

        if success:
            return {
                "success": True,
                "message": f"Task {queue_task_id} cancelled successfully"
            }
        else:
            raise HTTPException(status_code=404, detail=f"Task {queue_task_id} not found or cannot be cancelled")

    except Exception as e:
        logger.error(f"Failed to cancel task {queue_task_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cancel task: {str(e)}")


@router.get("/queue/project/{project_id}")
async def get_project_queue_status(project_id: int, db: Session = Depends(get_db)):
    """
    获取特定项目的队列状态
    """
    try:
        # 查询项目的所有队列任务
        project_tasks = db.query(TaskQueue).filter(TaskQueue.project_id == project_id).order_by(
            TaskQueue.created_at.desc()
        ).all()

        tasks_data = []
        for task in project_tasks:
            tasks_data.append({
                'id': task.id,
                'project_id': task.project_id,
                'status': task.status,
                'priority': task.priority,
                'created_at': task.created_at.isoformat(),
                'started_at': task.started_at.isoformat() if task.started_at else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'retry_count': task.retry_count,
                'max_retries': task.max_retries,
                'error_message': task.error_message,
                'external_task_id': task.external_task_id
            })

        return {
            "success": True,
            "project_id": project_id,
            "tasks": tasks_data,
            "total_tasks": len(tasks_data)
        }

    except Exception as e:
        logger.error(f"Failed to get project queue status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get project queue status: {str(e)}")


@router.post("/scheduler/start")
async def start_scheduler():
    """
    启动任务调度器
    """
    try:
        if task_scheduler._is_running:
            return {
                "success": True,
                "message": "Task scheduler is already running"
            }

        await task_scheduler.start()
        return {
            "success": True,
            "message": "Task scheduler started successfully"
        }

    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start scheduler: {str(e)}")


@router.post("/scheduler/stop")
async def stop_scheduler():
    """
    停止任务调度器
    """
    try:
        if not task_scheduler._is_running:
            return {
                "success": True,
                "message": "Task scheduler is already stopped"
            }

        await task_scheduler.stop()
        return {
            "success": True,
            "message": "Task scheduler stopped successfully"
        }

    except Exception as e:
        logger.error(f"Failed to stop scheduler: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to stop scheduler: {str(e)}")


@router.get("/scheduler/config")
async def get_scheduler_config():
    """
    获取调度器配置
    """
    try:
        config = {
            "MAX_CONCURRENT_TASKS": task_scheduler.config.MAX_CONCURRENT_TASKS,
            "QUEUE_CHECK_INTERVAL": task_scheduler.config.QUEUE_CHECK_INTERVAL,
            "TASK_TIMEOUT": task_scheduler.config.TASK_TIMEOUT,
            "MAX_RETRY_COUNT": task_scheduler.config.MAX_RETRY_COUNT,
            "CLEANUP_INTERVAL": task_scheduler.config.CLEANUP_INTERVAL
        }

        return {
            "success": True,
            "config": config,
            "is_running": task_scheduler._is_running
        }

    except Exception as e:
        logger.error(f"Failed to get scheduler config: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get scheduler config: {str(e)}")


@router.post("/queue/priority")
async def update_task_priority(queue_task_id: int, new_priority: int, db: Session = Depends(get_db)):
    """
    更新排队任务的优先级
    """
    try:
        if new_priority < 1 or new_priority > 10:
            raise HTTPException(status_code=400, detail="Priority must be between 1 and 10")

        task = db.query(TaskQueue).filter(
            TaskQueue.id == queue_task_id,
            TaskQueue.status == 'queued'
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Queued task not found")

        old_priority = task.priority
        task.priority = new_priority
        db.commit()

        logger.info(f"Updated task {queue_task_id} priority: {old_priority} -> {new_priority}")

        return {
            "success": True,
            "message": f"Task priority updated from {old_priority} to {new_priority}",
            "task_id": queue_task_id,
            "old_priority": old_priority,
            "new_priority": new_priority
        }

    except Exception as e:
        logger.error(f"Failed to update task priority: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update task priority: {str(e)}")


# 应用启动时自动启动任务调度器
@router.on_event("startup")
async def startup_event():
    """应用启动事件 - 自动启动任务调度器"""
    try:
        await task_scheduler.start()
        logger.info("Task scheduler auto-started on application startup")
    except Exception as e:
        logger.error(f"Failed to auto-start task scheduler: {e}")


@router.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件 - 停止任务调度器"""
    try:
        await task_scheduler.stop()
        logger.info("Task scheduler stopped on application shutdown")
    except Exception as e:
        logger.error(f"Failed to stop task scheduler on shutdown: {e}")
