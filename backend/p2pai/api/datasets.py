from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from ..schemas.training import DatasetUploadRequest
from common.schemas.common import BaseResponse
import uuid

router = APIRouter()

# Mock datasets database
mock_datasets = [
    {
        "id": "dataset-001",
        "name": "CIFAR-10 Training Set",
        "description": "Standard CIFAR-10 dataset for image classification",
        "type": "image_classification",
        "size": 50000,
        "format": "hdf5",
        "privacy_level": "public",
        "project_id": "federated-1",
        "uploaded_at": "2024-01-15T10:30:00Z",
        "file_path": "/datasets/cifar10_train.h5"
    },
    {
        "id": "dataset-002",
        "name": "Medical Images Dataset",
        "description": "Private medical imaging dataset for diagnosis",
        "type": "medical_imaging",
        "size": 15000,
        "format": "dicom",
        "privacy_level": "private",
        "project_id": "mpc-1",
        "uploaded_at": "2024-01-18T14:20:00Z",
        "file_path": "/datasets/medical_images.dicom"
    },
    {
        "id": "dataset-003",
        "name": "Financial Transaction Data",
        "description": "Encrypted financial transaction dataset for fraud detection",
        "type": "tabular",
        "size": 100000,
        "format": "csv",
        "privacy_level": "encrypted",
        "project_id": "local-1",
        "uploaded_at": "2024-01-10T09:15:00Z",
        "file_path": "/datasets/financial_encrypted.csv"
    }
]

@router.get("/", response_model=List[dict])
async def get_datasets(
    project_id: Optional[str] = None,
    privacy_level: Optional[str] = None,
    dataset_type: Optional[str] = None
):
    """
    获取数据集列表
    支持按项目、隐私级别和类型过滤
    """
    filtered_datasets = mock_datasets
    
    if project_id:
        filtered_datasets = [d for d in filtered_datasets if d["project_id"] == project_id]
    
    if privacy_level:
        filtered_datasets = [d for d in filtered_datasets if d["privacy_level"] == privacy_level]
    
    if dataset_type:
        filtered_datasets = [d for d in filtered_datasets if d["type"] == dataset_type]
    
    return filtered_datasets

@router.get("/{dataset_id}", response_model=dict)
async def get_dataset(dataset_id: str):
    """
    获取特定数据集详情
    """
    for dataset in mock_datasets:
        if dataset["id"] == dataset_id:
            return dataset
    
    raise HTTPException(status_code=404, detail="Dataset not found")

@router.post("/upload", response_model=BaseResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    project_id: str = None,
    dataset_name: str = None,
    privacy_level: str = "private"
):
    """
    上传数据集
    """
    try:
        # 生成数据集ID
        dataset_id = f"dataset-{uuid.uuid4().hex[:8]}"
        
        # 模拟文件保存
        file_path = f"/datasets/{dataset_id}_{file.filename}"
        
        # 创建数据集记录
        new_dataset = {
            "id": dataset_id,
            "name": dataset_name or file.filename,
            "description": f"Uploaded dataset: {file.filename}",
            "type": "custom",
            "size": file.size,
            "format": file.filename.split('.')[-1],
            "privacy_level": privacy_level,
            "project_id": project_id,
            "uploaded_at": "2024-01-15T10:30:00Z",
            "file_path": file_path
        }
        
        mock_datasets.append(new_dataset)
        
        return BaseResponse(
            success=True,
            message=f"Dataset uploaded successfully: {dataset_id}"
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            error=str(e)
        )

@router.post("/", response_model=BaseResponse)
async def create_dataset(request: DatasetUploadRequest):
    """
    创建数据集记录
    """
    try:
        dataset_id = f"dataset-{uuid.uuid4().hex[:8]}"
        
        new_dataset = {
            "id": dataset_id,
            "name": request.dataset_name,
            "description": request.description or f"Dataset: {request.dataset_name}",
            "type": request.dataset_type,
            "size": 0,  # 将在实际上传时更新
            "format": "unknown",
            "privacy_level": request.privacy_level,
            "project_id": request.project_id,
            "uploaded_at": "2024-01-15T10:30:00Z",
            "file_path": ""
        }
        
        mock_datasets.append(new_dataset)
        
        return BaseResponse(
            success=True,
            message=f"Dataset created successfully: {dataset_id}"
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            error=str(e)
        )

@router.delete("/{dataset_id}", response_model=BaseResponse)
async def delete_dataset(dataset_id: str):
    """
    删除数据集
    """
    global mock_datasets
    original_count = len(mock_datasets)
    mock_datasets = [d for d in mock_datasets if d["id"] != dataset_id]
    
    if len(mock_datasets) < original_count:
        return BaseResponse(
            success=True,
            message="Dataset deleted successfully"
        )
    else:
        raise HTTPException(status_code=404, detail="Dataset not found")

@router.get("/{dataset_id}/download")
async def download_dataset(dataset_id: str):
    """
    下载数据集
    """
    for dataset in mock_datasets:
        if dataset["id"] == dataset_id:
            # 模拟文件下载
            return {
                "dataset_id": dataset_id,
                "download_url": f"/api/p2pai/datasets/{dataset_id}/file",
                "filename": dataset["name"],
                "size": dataset["size"]
            }
    
    raise HTTPException(status_code=404, detail="Dataset not found")

@router.get("/stats/overview")
async def get_dataset_stats():
    """
    获取数据集统计信息
    """
    total_datasets = len(mock_datasets)
    total_size = sum(d["size"] for d in mock_datasets)
    
    privacy_levels = {}
    dataset_types = {}
    
    for dataset in mock_datasets:
        privacy_levels[dataset["privacy_level"]] = privacy_levels.get(dataset["privacy_level"], 0) + 1
        dataset_types[dataset["type"]] = dataset_types.get(dataset["type"], 0) + 1
    
    return {
        "total_datasets": total_datasets,
        "total_size": total_size,
        "privacy_levels": privacy_levels,
        "dataset_types": dataset_types,
        "avg_size": total_size / total_datasets if total_datasets > 0 else 0
    }

@router.post("/{dataset_id}/validate")
async def validate_dataset(dataset_id: str):
    """
    验证数据集
    """
    for dataset in mock_datasets:
        if dataset["id"] == dataset_id:
            # 模拟数据集验证
            return {
                "dataset_id": dataset_id,
                "valid": True,
                "validation_results": {
                    "format_valid": True,
                    "data_integrity": True,
                    "privacy_compliance": True,
                    "size_verified": True
                },
                "issues": []
            }
    
    raise HTTPException(status_code=404, detail="Dataset not found")
# dewdwe