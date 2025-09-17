from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from datetime import datetime

class BaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None
    data: Optional[Any] = None

class PaginationParams(BaseModel):
    page: int = 1
    size: int = 10
    sort_by: Optional[str] = None
    sort_order: str = "asc"

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
    uptime: float

class SystemInfo(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_usage: float
    active_connections: int

class LogEntry(BaseModel):
    id: str
    level: str
    message: str
    timestamp: datetime
    module: str
    user_id: Optional[str] = None

class NotificationRequest(BaseModel):
    title: str
    message: str
    type: str = "info"  # info, success, warning, error
    user_id: Optional[str] = None
    module: Optional[str] = None

class FileUploadResponse(BaseModel):
    success: bool
    file_id: str
    filename: str
    size: int
    url: str
    error: Optional[str] = None
