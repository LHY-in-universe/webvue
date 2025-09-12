from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..schemas.training import ModelExportRequest
from common.schemas.common import BaseResponse
import uuid

router = APIRouter()

# Mock models database
mock_models = [
    {
        "id": "model-001",
        "name": "Federated CNN Model",
        "description": "Convolutional Neural Network trained with federated learning",
        "type": "cnn",
        "project_id": "federated-1",
        "version": "1.0.0",
        "status": "trained",
        "accuracy": 87.5,
        "loss": 0.234,
        "f1_score": 85.2,
        "file_size": 25.6,  # MB
        "created_at": "2024-01-15T10:30:00Z",
        "trained_epochs": 100,
        "hyperparameters": {
            "learning_rate": 0.001,
            "batch_size": 32,
            "optimizer": "adam"
        },
        "file_path": "/models/federated_cnn_v1.0.0.pth"
    },
    {
        "id": "model-002",
        "name": "MPC Privacy Model",
        "description": "Transformer model trained with multi-party computation",
        "type": "transformer",
        "project_id": "mpc-1",
        "version": "1.2.0",
        "status": "training",
        "accuracy": 78.3,
        "loss": 0.412,
        "f1_score": 76.5,
        "file_size": 45.2,  # MB
        "created_at": "2024-01-18T14:20:00Z",
        "trained_epochs": 43,
        "hyperparameters": {
            "learning_rate": 0.0005,
            "batch_size": 16,
            "optimizer": "adamw"
        },
        "file_path": "/models/mpc_transformer_v1.2.0.pth"
    },
    {
        "id": "model-003",
        "name": "Local CNN Model",
        "description": "Local training CNN model for rapid prototyping",
        "type": "cnn",
        "project_id": "local-1",
        "version": "2.0.0",
        "status": "trained",
        "accuracy": 92.1,
        "loss": 0.156,
        "f1_score": 90.8,
        "file_size": 28.3,  # MB
        "created_at": "2024-01-10T09:15:00Z",
        "trained_epochs": 100,
        "hyperparameters": {
            "learning_rate": 0.001,
            "batch_size": 64,
            "optimizer": "sgd"
        },
        "file_path": "/models/local_cnn_v2.0.0.pth"
    }
]

@router.get("/", response_model=List[dict])
async def get_models(
    project_id: Optional[str] = None,
    model_type: Optional[str] = None,
    status: Optional[str] = None
):
    """
    获取模型列表
    支持按项目、类型和状态过滤
    """
    filtered_models = mock_models
    
    if project_id:
        filtered_models = [m for m in filtered_models if m["project_id"] == project_id]
    
    if model_type:
        filtered_models = [m for m in filtered_models if m["type"] == model_type]
    
    if status:
        filtered_models = [m for m in filtered_models if m["status"] == status]
    
    return filtered_models

@router.get("/{model_id}", response_model=dict)
async def get_model(model_id: str):
    """
    获取特定模型详情
    """
    for model in mock_models:
        if model["id"] == model_id:
            return model
    
    raise HTTPException(status_code=404, detail="Model not found")

@router.post("/{model_id}/export", response_model=BaseResponse)
async def export_model(model_id: str, request: ModelExportRequest):
    """
    导出模型
    """
    for model in mock_models:
        if model["id"] == model_id:
            # 模拟模型导出
            export_id = f"export-{uuid.uuid4().hex[:8]}"
            
            return BaseResponse(
                success=True,
                message=f"Model exported successfully: {export_id}",
                data={
                    "export_id": export_id,
                    "format": request.format,
                    "download_url": f"/api/p2pai/models/{model_id}/download/{export_id}",
                    "file_size": model["file_size"]
                }
            )
    
    raise HTTPException(status_code=404, detail="Model not found")

@router.post("/{model_id}/deploy", response_model=BaseResponse)
async def deploy_model(model_id: str, deployment_config: dict = None):
    """
    部署模型
    """
    for model in mock_models:
        if model["id"] == model_id:
            if model["status"] != "trained":
                raise HTTPException(status_code=400, detail="Model must be trained before deployment")
            
            # 模拟模型部署
            deployment_id = f"deployment-{uuid.uuid4().hex[:8]}"
            
            return BaseResponse(
                success=True,
                message=f"Model deployed successfully: {deployment_id}",
                data={
                    "deployment_id": deployment_id,
                    "endpoint": f"/api/p2pai/models/{model_id}/predict",
                    "status": "deployed"
                }
            )
    
    raise HTTPException(status_code=404, detail="Model not found")

@router.post("/{model_id}/undeploy", response_model=BaseResponse)
async def undeploy_model(model_id: str):
    """
    取消部署模型
    """
    for model in mock_models:
        if model["id"] == model_id:
            return BaseResponse(
                success=True,
                message="Model undeployed successfully"
            )
    
    raise HTTPException(status_code=404, detail="Model not found")

@router.post("/{model_id}/evaluate", response_model=BaseResponse)
async def evaluate_model(model_id: str, test_data: dict = None):
    """
    评估模型
    """
    for model in mock_models:
        if model["id"] == model_id:
            # 模拟模型评估
            evaluation_id = f"eval-{uuid.uuid4().hex[:8]}"
            
            return BaseResponse(
                success=True,
                message="Model evaluation completed",
                data={
                    "evaluation_id": evaluation_id,
                    "metrics": {
                        "accuracy": model["accuracy"],
                        "loss": model["loss"],
                        "f1_score": model["f1_score"],
                        "precision": 0.89,
                        "recall": 0.87
                    },
                    "test_samples": 1000,
                    "evaluation_time": "2.5s"
                }
            )
    
    raise HTTPException(status_code=404, detail="Model not found")

@router.get("/{model_id}/versions")
async def get_model_versions(model_id: str):
    """
    获取模型版本历史
    """
    # 模拟版本历史
    versions = [
        {
            "version": "1.0.0",
            "created_at": "2024-01-15T10:30:00Z",
            "accuracy": 85.2,
            "status": "archived"
        },
        {
            "version": "1.1.0",
            "created_at": "2024-01-16T14:20:00Z",
            "accuracy": 87.1,
            "status": "archived"
        },
        {
            "version": "1.2.0",
            "created_at": "2024-01-18T09:15:00Z",
            "accuracy": 87.5,
            "status": "current"
        }
    ]
    
    return {
        "model_id": model_id,
        "versions": versions
    }

@router.post("/{model_id}/rollback")
async def rollback_model(model_id: str, target_version: str):
    """
    回滚模型到指定版本
    """
    for model in mock_models:
        if model["id"] == model_id:
            # 模拟版本回滚
            model["version"] = target_version
            
            return BaseResponse(
                success=True,
                message=f"Model rolled back to version {target_version}"
            )
    
    raise HTTPException(status_code=404, detail="Model not found")

@router.get("/stats/overview")
async def get_model_stats():
    """
    获取模型统计信息
    """
    total_models = len(mock_models)
    trained_models = len([m for m in mock_models if m["status"] == "trained"])
    training_models = len([m for m in mock_models if m["status"] == "training"])
    
    model_types = {}
    for model in mock_models:
        model_types[model["type"]] = model_types.get(model["type"], 0) + 1
    
    avg_accuracy = sum(m["accuracy"] for m in mock_models) / total_models if total_models > 0 else 0
    
    return {
        "total_models": total_models,
        "trained_models": trained_models,
        "training_models": training_models,
        "model_types": model_types,
        "avg_accuracy": round(avg_accuracy, 2),
        "total_size": sum(m["file_size"] for m in mock_models)
    }

@router.post("/{model_id}/compare")
async def compare_models(model_id: str, compare_with: List[str]):
    """
    比较模型性能
    """
    # 模拟模型比较
    comparison_results = {
        "primary_model": model_id,
        "compared_models": compare_with,
        "metrics_comparison": {
            "accuracy": {
                model_id: 87.5,
                **{mid: 85.2 for mid in compare_with}
            },
            "loss": {
                model_id: 0.234,
                **{mid: 0.256 for mid in compare_with}
            },
            "f1_score": {
                model_id: 85.2,
                **{mid: 83.1 for mid in compare_with}
            }
        },
        "recommendation": f"Model {model_id} performs best overall"
    }
    
    return comparison_results
