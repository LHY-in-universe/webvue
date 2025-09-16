from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..schemas.edgeai import PerformanceMetrics
from common.schemas.common import BaseResponse
from datetime import datetime, timedelta
import random

router = APIRouter()

# Mock performance data
mock_performance_data = []

def generate_dynamic_performance_data():
    """Generate realistic performance data with patterns and trends"""
    performance_data = []
    nodes = [f"edge-{i:02d}" for i in range(1, 21)]  # 20 nodes

    for i in range(500):  # Generate more data points
        timestamp = datetime.now() - timedelta(minutes=i)
        node_id = random.choice(nodes)

        # Create realistic patterns based on time of day
        hour_of_day = timestamp.hour
        is_business_hours = 9 <= hour_of_day <= 17
        is_peak_hours = hour_of_day in [10, 11, 14, 15]  # Peak usage times

        # Base load factors
        base_cpu = 30 if is_business_hours else 15
        base_memory = 40 if is_business_hours else 25
        base_network = 20 if is_business_hours else 5

        # Add peak hour multipliers
        if is_peak_hours:
            base_cpu += 25
            base_memory += 20
            base_network += 15

        # Node-specific characteristics
        node_num = int(node_id.split('-')[1])
        if node_num <= 5:  # High-performance nodes
            base_cpu += 10
            base_memory += 15
            base_gpu = 40
        elif node_num <= 10:  # Medium-performance nodes
            base_gpu = 25
        else:  # Low-performance nodes
            base_cpu -= 5
            base_memory -= 10
            base_gpu = 10

        # Add random variations
        cpu_usage = max(5, min(95, base_cpu + random.uniform(-15, 25)))
        memory_usage = max(10, min(90, base_memory + random.uniform(-10, 20)))
        gpu_usage = max(0, min(100, base_gpu + random.uniform(-20, 30)))
        network_usage = max(0, min(80, base_network + random.uniform(-10, 25)))

        # Temperature correlates with CPU usage
        temp_base = 35 + (cpu_usage * 0.4) + random.uniform(-5, 5)
        temperature = max(30, min(85, temp_base))

        # Power consumption correlates with overall usage
        power_base = 80 + (cpu_usage * 0.8) + (gpu_usage * 0.6) + random.uniform(-20, 20)
        power_consumption = max(50, min(300, power_base))

        performance_data.append({
            "node_id": node_id,
            "timestamp": timestamp,
            "cpu_usage": round(cpu_usage, 2),
            "memory_usage": round(memory_usage, 2),
            "gpu_usage": round(gpu_usage, 2),
            "network_usage": round(network_usage, 2),
            "temperature": round(temperature, 2),
            "power_consumption": round(power_consumption, 2)
        })

    return sorted(performance_data, key=lambda x: x["timestamp"], reverse=True)

# Generate comprehensive mock performance data
mock_performance_data = generate_dynamic_performance_data()

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

@router.get("/realtime")
async def get_realtime_performance():
    """
    获取实时性能数据 - 模拟实时状态变化
    """
    nodes = [f"edge-{i:02d}" for i in range(1, 21)]
    realtime_data = []

    current_time = datetime.now()
    is_business_hours = 9 <= current_time.hour <= 17
    is_peak_hours = current_time.hour in [10, 11, 14, 15]

    for node_id in nodes:
        node_num = int(node_id.split('-')[1])

        # Simulate different load patterns per node
        base_load = 20 + (node_num * 2)  # Each node has slightly different baseline
        if is_business_hours:
            base_load += 25
        if is_peak_hours:
            base_load += 15

        # Add some random variations for real-time feel
        cpu_variation = random.uniform(-10, 15)
        memory_variation = random.uniform(-8, 12)

        # High-performance nodes (1-5) tend to have higher usage
        if node_num <= 5:
            cpu_usage = max(15, min(90, base_load + 20 + cpu_variation))
            memory_usage = max(20, min(85, base_load + 15 + memory_variation))
            gpu_usage = max(10, min(95, 50 + random.uniform(-20, 25)))
        # Medium-performance nodes (6-10)
        elif node_num <= 10:
            cpu_usage = max(10, min(80, base_load + 10 + cpu_variation))
            memory_usage = max(15, min(75, base_load + 10 + memory_variation))
            gpu_usage = max(5, min(70, 35 + random.uniform(-15, 20)))
        # Lower-performance nodes (11-20)
        else:
            cpu_usage = max(5, min(70, base_load + cpu_variation))
            memory_usage = max(10, min(65, base_load + memory_variation))
            gpu_usage = max(0, min(50, 20 + random.uniform(-10, 15)))

        network_usage = max(0, min(60, base_load * 0.6 + random.uniform(-5, 15)))
        temperature = max(35, min(80, 40 + (cpu_usage * 0.35) + random.uniform(-3, 3)))
        power_consumption = max(60, min(280, 90 + (cpu_usage * 0.7) + (gpu_usage * 0.5)))

        # Simulate some nodes having alerts
        alerts = []
        status = "healthy"

        if cpu_usage > 85:
            alerts.append("High CPU usage")
            status = "warning"
        if memory_usage > 80:
            alerts.append("High memory usage")
            status = "critical" if status != "warning" else status
        if temperature > 75:
            alerts.append("High temperature")
            status = "warning" if status == "healthy" else status

        realtime_data.append({
            "node_id": node_id,
            "timestamp": current_time.isoformat(),
            "cpu_usage": round(cpu_usage, 1),
            "memory_usage": round(memory_usage, 1),
            "gpu_usage": round(gpu_usage, 1),
            "network_usage": round(network_usage, 1),
            "temperature": round(temperature, 1),
            "power_consumption": round(power_consumption, 0),
            "status": status,
            "alerts": alerts,
            "uptime": f"{random.randint(1, 30)}d {random.randint(0, 23)}h {random.randint(0, 59)}m"
        })

    # Calculate cluster-wide statistics
    avg_cpu = sum(node["cpu_usage"] for node in realtime_data) / len(realtime_data)
    avg_memory = sum(node["memory_usage"] for node in realtime_data) / len(realtime_data)
    total_alerts = sum(len(node["alerts"]) for node in realtime_data)
    healthy_nodes = len([node for node in realtime_data if node["status"] == "healthy"])

    return {
        "timestamp": current_time.isoformat(),
        "cluster_stats": {
            "total_nodes": len(realtime_data),
            "healthy_nodes": healthy_nodes,
            "nodes_with_alerts": len(realtime_data) - healthy_nodes,
            "avg_cpu_usage": round(avg_cpu, 1),
            "avg_memory_usage": round(avg_memory, 1),
            "total_active_alerts": total_alerts
        },
        "nodes": realtime_data
    }

@router.get("/simulate")
async def simulate_performance_event():
    """
    模拟性能事件 - 用于演示动态数据变化
    """
    events = [
        {
            "type": "cpu_spike",
            "node_id": f"edge-{random.randint(1, 20):02d}",
            "message": "CPU usage spiked to 92%",
            "severity": "warning",
            "duration": "2-3 minutes expected"
        },
        {
            "type": "memory_leak",
            "node_id": f"edge-{random.randint(1, 20):02d}",
            "message": "Memory leak detected in inference service",
            "severity": "critical",
            "duration": "Restart required"
        },
        {
            "type": "training_completed",
            "node_id": f"edge-{random.randint(1, 20):02d}",
            "message": "Model training completed successfully",
            "severity": "info",
            "duration": "N/A"
        },
        {
            "type": "node_recovery",
            "node_id": f"edge-{random.randint(1, 20):02d}",
            "message": "Node performance normalized after optimization",
            "severity": "info",
            "duration": "N/A"
        }
    ]

    event = random.choice(events)
    event["timestamp"] = datetime.now().isoformat()
    event["id"] = f"event-{random.randint(1000, 9999)}"

    return {
        "event": event,
        "message": f"Simulated performance event: {event['type']}"
    }
