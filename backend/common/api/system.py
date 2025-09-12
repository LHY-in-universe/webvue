from fastapi import APIRouter
from ..schemas.common import HealthCheck, SystemInfo, LogEntry, PaginatedResponse
from typing import List
import time
import psutil
from datetime import datetime

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """
    系统健康检查
    """
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        uptime=time.time()
    )

@router.get("/system-info", response_model=SystemInfo)
async def get_system_info():
    """
    获取系统信息
    """
    return SystemInfo(
        cpu_usage=psutil.cpu_percent(),
        memory_usage=psutil.virtual_memory().percent,
        disk_usage=psutil.disk_usage('/').percent,
        network_usage=0.0,  # 需要更复杂的网络监控
        active_connections=0  # 需要连接池监控
    )

@router.get("/logs", response_model=PaginatedResponse)
async def get_system_logs(
    page: int = 1,
    size: int = 10,
    level: str = None,
    module: str = None
):
    """
    获取系统日志
    """
    # 模拟日志数据
    mock_logs = [
        LogEntry(
            id="log_001",
            level="INFO",
            message="System started successfully",
            timestamp=datetime.now(),
            module="system",
            user_id=None
        ),
        LogEntry(
            id="log_002",
            level="INFO",
            message="User admin logged in",
            timestamp=datetime.now(),
            module="auth",
            user_id="1"
        ),
        LogEntry(
            id="log_003",
            level="WARNING",
            message="High memory usage detected",
            timestamp=datetime.now(),
            module="monitor",
            user_id=None
        )
    ]
    
    # 过滤日志
    filtered_logs = mock_logs
    if level:
        filtered_logs = [log for log in filtered_logs if log.level.lower() == level.lower()]
    if module:
        filtered_logs = [log for log in filtered_logs if log.module == module]
    
    # 分页
    start = (page - 1) * size
    end = start + size
    paginated_logs = filtered_logs[start:end]
    
    return PaginatedResponse(
        items=paginated_logs,
        total=len(filtered_logs),
        page=page,
        size=size,
        pages=(len(filtered_logs) + size - 1) // size
    )

@router.get("/notifications")
async def get_notifications(user_id: str = None):
    """
    获取通知列表
    """
    # 模拟通知数据
    mock_notifications = [
        {
            "id": "notif_001",
            "title": "系统维护通知",
            "message": "系统将在今晚进行维护，预计停机2小时",
            "type": "info",
            "timestamp": datetime.now().isoformat(),
            "read": False
        },
        {
            "id": "notif_002",
            "title": "训练任务完成",
            "message": "您的模型训练任务已完成",
            "type": "success",
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
    ]
    
    return mock_notifications

@router.post("/notifications/mark-read")
async def mark_notification_read(notification_id: str):
    """
    标记通知为已读
    """
    return {"success": True, "message": "Notification marked as read"}

@router.get("/stats")
async def get_global_stats():
    """
    获取全局统计信息
    """
    return {
        "total_users": 150,
        "active_sessions": 25,
        "total_projects": 45,
        "system_uptime": "99.9%",
        "api_requests_today": 1250,
        "last_updated": datetime.now().isoformat()
    }
