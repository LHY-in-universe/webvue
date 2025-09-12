from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..schemas.edgeai import PerformanceMetrics
from common.schemas.common import BaseResponse
from datetime import datetime, timedelta
import random

router = APIRouter()

# Mock performance data
mock_performance_data = []

# Generate some mock historical data
for i in range(100):
    timestamp = datetime.now() - timedelta(minutes=i)
    mock_performance_data.append({
        "node_id": f"edge-{(i % 4) + 1}",
        "timestamp": timestamp,
        "cpu_usage": random.uniform(10, 90),
        "memory_usage": random.uniform(20, 80),
        "gpu_usage": random.uniform(0, 95),
        "network_usage": random.uniform(0, 50),
        "temperature": random.uniform(40, 80),
        "power_consumption": random.uniform(50, 200)
    })

@router.get("/metrics", response_model=List[PerformanceMetrics])
async def get_performance_metrics(
    node_id: Optional[str] = None,
    hours: int = 24,
    limit: int = 100
):
    """
    获取性能指标
    支持按节点ID和时间范围过滤
    """
    filtered_data = mock_performance_data
    
    if node_id:
        filtered_data = [d for d in filtered_data if d["node_id"] == node_id]
    
    # 按时间过滤
    cutoff_time = datetime.now() - timedelta(hours=hours)
    filtered_data = [d for d in filtered_data if d["timestamp"] >= cutoff_time]
    
    # 限制返回数量
    filtered_data = filtered_data[:limit]
    
    return [PerformanceMetrics(**data) for data in filtered_data]

@router.get("/metrics/{node_id}", response_model=List[PerformanceMetrics])
async def get_node_performance_metrics(
    node_id: str,
    hours: int = 24,
    limit: int = 100
):
    """
    获取特定节点的性能指标
    """
    filtered_data = [
        d for d in mock_performance_data 
        if d["node_id"] == node_id
    ]
    
    # 按时间过滤
    cutoff_time = datetime.now() - timedelta(hours=hours)
    filtered_data = [d for d in filtered_data if d["timestamp"] >= cutoff_time]
    
    # 限制返回数量
    filtered_data = filtered_data[:limit]
    
    return [PerformanceMetrics(**data) for data in filtered_data]

@router.get("/summary")
async def get_performance_summary(
    node_id: Optional[str] = None,
    hours: int = 24
):
    """
    获取性能摘要
    """
    filtered_data = mock_performance_data
    
    if node_id:
        filtered_data = [d for d in filtered_data if d["node_id"] == node_id]
    
    # 按时间过滤
    cutoff_time = datetime.now() - timedelta(hours=hours)
    filtered_data = [d for d in filtered_data if d["timestamp"] >= cutoff_time]
    
    if not filtered_data:
        return {
            "node_id": node_id,
            "period_hours": hours,
            "data_points": 0,
            "summary": "No data available"
        }
    
    # 计算统计信息
    cpu_values = [d["cpu_usage"] for d in filtered_data]
    memory_values = [d["memory_usage"] for d in filtered_data]
    gpu_values = [d["gpu_usage"] for d in filtered_data]
    network_values = [d["network_usage"] for d in filtered_data]
    
    return {
        "node_id": node_id,
        "period_hours": hours,
        "data_points": len(filtered_data),
        "cpu": {
            "avg": round(sum(cpu_values) / len(cpu_values), 2),
            "min": round(min(cpu_values), 2),
            "max": round(max(cpu_values), 2)
        },
        "memory": {
            "avg": round(sum(memory_values) / len(memory_values), 2),
            "min": round(min(memory_values), 2),
            "max": round(max(memory_values), 2)
        },
        "gpu": {
            "avg": round(sum(gpu_values) / len(gpu_values), 2),
            "min": round(min(gpu_values), 2),
            "max": round(max(gpu_values), 2)
        },
        "network": {
            "avg": round(sum(network_values) / len(network_values), 2),
            "min": round(min(network_values), 2),
            "max": round(max(network_values), 2)
        }
    }

@router.get("/alerts")
async def get_performance_alerts():
    """
    获取性能告警
    """
    # 模拟告警数据
    alerts = [
        {
            "id": "alert-001",
            "node_id": "edge-4",
            "type": "high_cpu",
            "message": "CPU usage exceeded 90%",
            "severity": "warning",
            "timestamp": datetime.now() - timedelta(minutes=5),
            "resolved": False
        },
        {
            "id": "alert-002",
            "node_id": "edge-2",
            "type": "high_memory",
            "message": "Memory usage exceeded 85%",
            "severity": "critical",
            "timestamp": datetime.now() - timedelta(minutes=15),
            "resolved": False
        },
        {
            "id": "alert-003",
            "node_id": "edge-1",
            "type": "high_temperature",
            "message": "Temperature exceeded 75°C",
            "severity": "warning",
            "timestamp": datetime.now() - timedelta(minutes=30),
            "resolved": True
        }
    ]
    
    return {
        "alerts": alerts,
        "total": len(alerts),
        "unresolved": len([a for a in alerts if not a["resolved"]])
    }

@router.post("/alerts/{alert_id}/resolve", response_model=BaseResponse)
async def resolve_alert(alert_id: str):
    """
    解决告警
    """
    # 模拟告警解决
    return BaseResponse(
        success=True,
        message=f"Alert {alert_id} resolved successfully"
    )

@router.get("/trends")
async def get_performance_trends(
    node_id: Optional[str] = None,
    metric: str = "cpu_usage",
    hours: int = 24
):
    """
    获取性能趋势
    """
    filtered_data = mock_performance_data
    
    if node_id:
        filtered_data = [d for d in filtered_data if d["node_id"] == node_id]
    
    # 按时间过滤
    cutoff_time = datetime.now() - timedelta(hours=hours)
    filtered_data = [d for d in filtered_data if d["timestamp"] >= cutoff_time]
    
    # 按时间排序
    filtered_data.sort(key=lambda x: x["timestamp"])
    
    # 提取趋势数据
    trend_data = []
    for data in filtered_data:
        trend_data.append({
            "timestamp": data["timestamp"].isoformat(),
            "value": data[metric]
        })
    
    return {
        "node_id": node_id,
        "metric": metric,
        "period_hours": hours,
        "trend_data": trend_data
    }

@router.get("/comparison")
async def compare_node_performance(
    node_ids: List[str],
    metric: str = "cpu_usage",
    hours: int = 24
):
    """
    比较节点性能
    """
    comparison_data = {}
    
    for node_id in node_ids:
        node_data = [
            d for d in mock_performance_data 
            if d["node_id"] == node_id
        ]
        
        # 按时间过滤
        cutoff_time = datetime.now() - timedelta(hours=hours)
        node_data = [d for d in node_data if d["timestamp"] >= cutoff_time]
        
        if node_data:
            values = [d[metric] for d in node_data]
            comparison_data[node_id] = {
                "avg": round(sum(values) / len(values), 2),
                "min": round(min(values), 2),
                "max": round(max(values), 2),
                "data_points": len(values)
            }
        else:
            comparison_data[node_id] = {
                "avg": 0,
                "min": 0,
                "max": 0,
                "data_points": 0
            }
    
    return {
        "metric": metric,
        "period_hours": hours,
        "comparison": comparison_data
    }

@router.get("/health")
async def get_system_health():
    """
    获取系统健康状态
    """
    # 获取最新数据
    latest_data = mock_performance_data[:4]  # 假设有4个节点
    
    health_status = {
        "overall": "healthy",
        "nodes": [],
        "issues": []
    }
    
    for data in latest_data:
        node_health = "healthy"
        issues = []
        
        if data["cpu_usage"] > 90:
            node_health = "warning"
            issues.append("High CPU usage")
        
        if data["memory_usage"] > 85:
            node_health = "critical"
            issues.append("High memory usage")
        
        if data["temperature"] and data["temperature"] > 75:
            node_health = "warning"
            issues.append("High temperature")
        
        health_status["nodes"].append({
            "node_id": data["node_id"],
            "status": node_health,
            "issues": issues
        })
        
        if issues:
            health_status["issues"].extend(issues)
    
    # 确定整体健康状态
    if any(node["status"] == "critical" for node in health_status["nodes"]):
        health_status["overall"] = "critical"
    elif any(node["status"] == "warning" for node in health_status["nodes"]):
        health_status["overall"] = "warning"
    
    return health_status
