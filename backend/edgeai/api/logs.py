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

def generate_dynamic_logs():
    """Generate 500 realistic log entries with diverse scenarios"""
    detailed_log_scenarios = [
        # Training and Model Operations
        {"level": "INFO", "message": "Model training initialized for {project}", "category": "training"},
        {"level": "INFO", "message": "Training epoch {epoch}/100 completed - Loss: {loss:.4f}", "category": "training"},
        {"level": "INFO", "message": "Model checkpoint saved successfully", "category": "training"},
        {"level": "WARNING", "message": "Training convergence slower than expected", "category": "training"},
        {"level": "ERROR", "message": "Training interrupted due to insufficient memory", "category": "training"},
        {"level": "INFO", "message": "Model validation completed - Accuracy: {accuracy:.2f}%", "category": "training"},

        # Node Operations
        {"level": "INFO", "message": "Edge node successfully connected to cluster", "category": "node"},
        {"level": "INFO", "message": "Node health check completed - All systems operational", "category": "node"},
        {"level": "WARNING", "message": "Node CPU usage reached 85% - Scaling recommended", "category": "node"},
        {"level": "WARNING", "message": "Network latency increased to {latency}ms", "category": "node"},
        {"level": "ERROR", "message": "Node connection lost - Attempting reconnection", "category": "node"},
        {"level": "INFO", "message": "Node firmware updated to version {version}", "category": "node"},
        {"level": "CRITICAL", "message": "Node temperature exceeded safe threshold: {temp}°C", "category": "node"},

        # Data Processing
        {"level": "INFO", "message": "Data preprocessing completed for {dataset} samples", "category": "data"},
        {"level": "INFO", "message": "Feature extraction completed in {time:.2f}s", "category": "data"},
        {"level": "WARNING", "message": "Data quality check found {issues} anomalies", "category": "data"},
        {"level": "ERROR", "message": "Data validation failed - Schema mismatch detected", "category": "data"},
        {"level": "INFO", "message": "Dataset synchronization completed", "category": "data"},

        # Inference and Deployment
        {"level": "INFO", "message": "Model deployed to edge device successfully", "category": "inference"},
        {"level": "INFO", "message": "Inference request processed in {time}ms", "category": "inference"},
        {"level": "WARNING", "message": "Inference queue backlog reached {count} requests", "category": "inference"},
        {"level": "ERROR", "message": "Model inference failed - Input tensor size mismatch", "category": "inference"},
        {"level": "INFO", "message": "Batch inference completed - {count} predictions generated", "category": "inference"},

        # System Monitoring
        {"level": "INFO", "message": "System monitoring dashboard updated", "category": "system"},
        {"level": "WARNING", "message": "Disk usage reached 90% capacity", "category": "system"},
        {"level": "WARNING", "message": "Memory usage spike detected: {usage}%", "category": "system"},
        {"level": "ERROR", "message": "Database connection pool exhausted", "category": "system"},
        {"level": "CRITICAL", "message": "System backup failed - Manual intervention required", "category": "system"},
        {"level": "INFO", "message": "Security scan completed - No vulnerabilities found", "category": "system"},

        # Performance and Optimization
        {"level": "INFO", "message": "Performance optimization completed - {improvement}% faster", "category": "performance"},
        {"level": "WARNING", "message": "Model performance degradation detected", "category": "performance"},
        {"level": "INFO", "message": "Auto-scaling triggered - Adding {count} instances", "category": "performance"},
        {"level": "ERROR", "message": "Performance benchmark failed to meet SLA requirements", "category": "performance"},

        # Network and Communication
        {"level": "INFO", "message": "WebSocket connection established with client", "category": "network"},
        {"level": "WARNING", "message": "API rate limit exceeded for endpoint {endpoint}", "category": "network"},
        {"level": "ERROR", "message": "Network timeout occurred during data transfer", "category": "network"},
        {"level": "INFO", "message": "SSL certificate renewed successfully", "category": "network"},

        # Configuration and Setup
        {"level": "INFO", "message": "Configuration updated for {component}", "category": "config"},
        {"level": "WARNING", "message": "Deprecated configuration parameter detected", "category": "config"},
        {"level": "ERROR", "message": "Configuration validation failed - Invalid format", "category": "config"},

        # User Actions
        {"level": "INFO", "message": "User {user} logged in successfully", "category": "user"},
        {"level": "INFO", "message": "Project {project} created by user {user}", "category": "user"},
        {"level": "WARNING", "message": "Multiple failed login attempts detected", "category": "user"},
        {"level": "ERROR", "message": "Unauthorized access attempt blocked", "category": "user"}
    ]

    projects = ["Smart Manufacturing", "Healthcare Analytics", "Autonomous Driving", "IoT Sensors", "Financial Risk", "Retail Optimization", "Energy Management", "Security Monitoring", "Agricultural AI", "Traffic Control"]
    nodes = [f"edge-{i:02d}" for i in range(1, 21)]
    project_ids = [f"proj-{i:03d}" for i in range(1, 11)]
    users = ["admin", "researcher", "engineer", "analyst", "operator"]

    logs = []
    for i in range(500):
        scenario = random.choice(detailed_log_scenarios)
        message = scenario["message"]

        # Format message with dynamic values
        if "{project}" in message:
            message = message.replace("{project}", random.choice(projects))
        if "{epoch}" in message:
            message = message.replace("{epoch}", str(random.randint(1, 100)))
        if "{loss}" in message:
            message = message.replace("{loss}", str(random.uniform(0.001, 0.5)))
        if "{accuracy}" in message:
            message = message.replace("{accuracy}", str(random.uniform(75, 99)))
        if "{latency}" in message:
            message = message.replace("{latency}", str(random.randint(50, 500)))
        if "{version}" in message:
            message = message.replace("{version}", f"{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,9)}")
        if "{temp}" in message:
            message = message.replace("{temp}", str(random.randint(75, 95)))
        if "{dataset}" in message:
            message = message.replace("{dataset}", str(random.randint(1000, 50000)))
        if "{time}" in message:
            if "ms" in message:
                message = message.replace("{time}", str(random.randint(10, 1000)))
            else:
                message = message.replace("{time}", str(random.uniform(0.5, 30)))
        if "{issues}" in message:
            message = message.replace("{issues}", str(random.randint(1, 20)))
        if "{count}" in message:
            message = message.replace("{count}", str(random.randint(1, 100)))
        if "{usage}" in message:
            message = message.replace("{usage}", str(random.randint(80, 95)))
        if "{improvement}" in message:
            message = message.replace("{improvement}", str(random.randint(10, 50)))
        if "{endpoint}" in message:
            endpoints = ["/api/models", "/api/training", "/api/inference", "/api/data"]
            message = message.replace("{endpoint}", random.choice(endpoints))
        if "{component}" in message:
            components = ["model", "node", "database", "monitoring", "scheduler"]
            message = message.replace("{component}", random.choice(components))
        if "{user}" in message:
            message = message.replace("{user}", random.choice(users))

        # Create timestamp with more realistic distribution
        # More recent logs are more frequent
        hours_ago = random.choices(
            range(0, 168),  # 7 days
            weights=[max(1, 168-h) for h in range(168)]  # Weight recent logs more heavily
        )[0]

        logs.append({
            "id": f"log-{i:03d}",
            "level": scenario["level"],
            "message": message,
            "timestamp": datetime.now() - timedelta(hours=hours_ago, minutes=random.randint(0, 59)),
            "node_id": random.choice(nodes),
            "project_id": random.choice(project_ids),
            "category": scenario["category"]
        })

    return sorted(logs, key=lambda x: x["timestamp"], reverse=True)

# Generate comprehensive mock logs
mock_logs = generate_dynamic_logs()

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
