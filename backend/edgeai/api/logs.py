from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..schemas.edgeai import LogEntry
from common.schemas.common import PaginatedResponse
from datetime import datetime, timedelta
import random

router = APIRouter()

# Mock logs database
mock_logs = []

# Generate some mock log data
log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
log_messages = [
    "Node connected successfully",
    "Training started",
    "Training completed",
    "High CPU usage detected",
    "Memory usage exceeded threshold",
    "Model saved successfully",
    "Connection lost",
    "Node restarted",
    "Error in training process",
    "Data validation failed"
]

for i in range(200):
    mock_logs.append({
        "id": f"log-{i:03d}",
        "level": random.choice(log_levels),
        "message": random.choice(log_messages),
        "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 1440)),
        "node_id": f"edge-{(i % 4) + 1}",
        "project_id": f"proj-{(i % 3) + 1:03d}"
    })

@router.get("/", response_model=PaginatedResponse)
async def get_logs(
    level: Optional[str] = None,
    node_id: Optional[str] = None,
    project_id: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    hours: int = 24
):
    """
    获取日志列表
    支持按级别、节点ID、项目ID过滤和分页
    """
    filtered_logs = mock_logs
    
    # 按级别过滤
    if level:
        filtered_logs = [log for log in filtered_logs if log["level"] == level.upper()]
    
    # 按节点ID过滤
    if node_id:
        filtered_logs = [log for log in filtered_logs if log["node_id"] == node_id]
    
    # 按项目ID过滤
    if project_id:
        filtered_logs = [log for log in filtered_logs if log["project_id"] == project_id]
    
    # 按时间过滤
    cutoff_time = datetime.now() - timedelta(hours=hours)
    filtered_logs = [log for log in filtered_logs if log["timestamp"] >= cutoff_time]
    
    # 按时间排序（最新的在前）
    filtered_logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # 分页
    start = (page - 1) * size
    end = start + size
    paginated_logs = filtered_logs[start:end]
    
    return PaginatedResponse(
        items=[LogEntry(**log) for log in paginated_logs],
        total=len(filtered_logs),
        page=page,
        size=size,
        pages=(len(filtered_logs) + size - 1) // size
    )

@router.get("/{log_id}", response_model=LogEntry)
async def get_log(log_id: str):
    """
    获取特定日志详情
    """
    for log in mock_logs:
        if log["id"] == log_id:
            return LogEntry(**log)
    
    raise HTTPException(status_code=404, detail="Log not found")

@router.get("/stats/summary")
async def get_log_stats(
    hours: int = 24,
    node_id: Optional[str] = None,
    project_id: Optional[str] = None
):
    """
    获取日志统计摘要
    """
    filtered_logs = mock_logs
    
    # 按节点ID过滤
    if node_id:
        filtered_logs = [log for log in filtered_logs if log["node_id"] == node_id]
    
    # 按项目ID过滤
    if project_id:
        filtered_logs = [log for log in filtered_logs if log["project_id"] == project_id]
    
    # 按时间过滤
    cutoff_time = datetime.now() - timedelta(hours=hours)
    filtered_logs = [log for log in filtered_logs if log["timestamp"] >= cutoff_time]
    
    # 统计各级别日志数量
    level_counts = {}
    for log in filtered_logs:
        level_counts[log["level"]] = level_counts.get(log["level"], 0) + 1
    
    # 统计各节点日志数量
    node_counts = {}
    for log in filtered_logs:
        node_counts[log["node_id"]] = node_counts.get(log["node_id"], 0) + 1
    
    # 统计各项目日志数量
    project_counts = {}
    for log in filtered_logs:
        project_counts[log["project_id"]] = project_counts.get(log["project_id"], 0) + 1
    
    return {
        "period_hours": hours,
        "total_logs": len(filtered_logs),
        "level_distribution": level_counts,
        "node_distribution": node_counts,
        "project_distribution": project_counts,
        "error_rate": round(level_counts.get("ERROR", 0) / len(filtered_logs) * 100, 2) if filtered_logs else 0
    }

@router.get("/search")
async def search_logs(
    query: str,
    level: Optional[str] = None,
    node_id: Optional[str] = None,
    project_id: Optional[str] = None,
    page: int = 1,
    size: int = 20
):
    """
    搜索日志
    """
    filtered_logs = mock_logs
    
    # 按级别过滤
    if level:
        filtered_logs = [log for log in filtered_logs if log["level"] == level.upper()]
    
    # 按节点ID过滤
    if node_id:
        filtered_logs = [log for log in filtered_logs if log["node_id"] == node_id]
    
    # 按项目ID过滤
    if project_id:
        filtered_logs = [log for log in filtered_logs if log["project_id"] == project_id]
    
    # 按查询字符串过滤
    query_lower = query.lower()
    filtered_logs = [
        log for log in filtered_logs 
        if query_lower in log["message"].lower()
    ]
    
    # 按时间排序（最新的在前）
    filtered_logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # 分页
    start = (page - 1) * size
    end = start + size
    paginated_logs = filtered_logs[start:end]
    
    return {
        "query": query,
        "results": [LogEntry(**log) for log in paginated_logs],
        "total": len(filtered_logs),
        "page": page,
        "size": size,
        "pages": (len(filtered_logs) + size - 1) // size
    }

@router.get("/export")
async def export_logs(
    level: Optional[str] = None,
    node_id: Optional[str] = None,
    project_id: Optional[str] = None,
    hours: int = 24,
    format: str = "json"
):
    """
    导出日志
    """
    filtered_logs = mock_logs
    
    # 应用过滤条件
    if level:
        filtered_logs = [log for log in filtered_logs if log["level"] == level.upper()]
    
    if node_id:
        filtered_logs = [log for log in filtered_logs if log["node_id"] == node_id]
    
    if project_id:
        filtered_logs = [log for log in filtered_logs if log["project_id"] == project_id]
    
    # 按时间过滤
    cutoff_time = datetime.now() - timedelta(hours=hours)
    filtered_logs = [log for log in filtered_logs if log["timestamp"] >= cutoff_time]
    
    # 按时间排序
    filtered_logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    if format == "csv":
        # 模拟CSV导出
        csv_content = "timestamp,level,message,node_id,project_id\n"
        for log in filtered_logs:
            csv_content += f"{log['timestamp'].isoformat()},{log['level']},{log['message']},{log['node_id']},{log['project_id']}\n"
        
        return {
            "format": "csv",
            "content": csv_content,
            "filename": f"logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    else:
        # JSON格式
        return {
            "format": "json",
            "logs": [LogEntry(**log) for log in filtered_logs],
            "total": len(filtered_logs),
            "exported_at": datetime.now().isoformat()
        }

@router.delete("/cleanup")
async def cleanup_logs(
    older_than_hours: int = 168,  # 默认清理7天前的日志
    dry_run: bool = True
):
    """
    清理旧日志
    """
    global mock_logs
    cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
    
    logs_to_delete = [log for log in mock_logs if log["timestamp"] < cutoff_time]
    
    if dry_run:
        return {
            "dry_run": True,
            "logs_to_delete": len(logs_to_delete),
            "cutoff_time": cutoff_time.isoformat(),
            "message": f"Would delete {len(logs_to_delete)} logs older than {older_than_hours} hours"
        }
    else:
        # 实际删除日志
        original_logs = mock_logs
        mock_logs = [log for log in original_logs if log["timestamp"] >= cutoff_time]
        
        return {
            "dry_run": False,
            "deleted_logs": len(logs_to_delete),
            "remaining_logs": len(mock_logs),
            "message": f"Deleted {len(logs_to_delete)} logs older than {older_than_hours} hours"
        }

@router.get("/realtime")
async def get_realtime_logs(limit: int = 50):
    """
    获取实时日志（最新的日志）
    """
    # 获取最新的日志
    recent_logs = sorted(mock_logs, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    return {
        "logs": [LogEntry(**log) for log in recent_logs],
        "total": len(recent_logs),
        "timestamp": datetime.now().isoformat()
    }
