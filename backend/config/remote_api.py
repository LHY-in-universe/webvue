"""
Remote API Configuration
统一管理远程API的配置信息
"""

# 远程API基础配置
REMOTE_API_CONFIG = {
    # 基础URL
    "BASE_URL": "http://12.148.158.61:6677",

    # 请求超时时间（秒）
    "TIMEOUT": 30.0,

    # ============ 训练任务端点 ============
    # 启动训练任务
    "TRAIN": "/train",

    # 获取任务状态
    "TASK_STATUS": "/tasks/{task_id}",

    # 删除/停止任务
    "TASK_DELETE": "/tasks/{task_id}",

    # 获取任务列表
    "TASKS_LIST": "/tasksList",

    # 检查是否有运行中的任务
    "HAS_RUNNING_TASK": "/hasRunningTask",

    # ============ 集群管理端点 ============
    # 创建Ray集群
    "CLUSTER_CREATE": "/cluster/create",

    # 停止Ray集群
    "CLUSTER_STOP": "/cluster/stop",

    # 向集群添加节点
    "CLUSTER_ADD_NODES": "/cluster/add-nodes",

    # 从集群移除节点
    "CLUSTER_REMOVE_NODES": "/cluster/remove-nodes",

    # 验证节点是否可用
    "CLUSTER_VALIDATE_NODES": "/cluster/validate-nodes",

    # 获取可用节点列表
    "CLUSTER_AVAILABLE_NODES": "/cluster/available-nodes",

    # ============ Ray监控端点 ============
    # 获取集群节点信息
    "MONITOR_CLUSTER_NODES": "/monitor/ray/cluster/node",

    # 获取集群状态
    "MONITOR_CLUSTER_STATUS": "/monitor/ray/cluster/status",

    # 获取节点指标
    "MONITOR_NODE_METRICS": "/monitor/ray/cluster/node/{node_id}/metrics",
}


def get_remote_api_url(endpoint_key: str, **kwargs) -> str:
    """
    获取完整的远程API URL

    Args:
        endpoint_key: 端点配置键名
        **kwargs: 用于格式化路径参数（如 {task_id}）

    Returns:
        完整的API URL

    Example:
        get_remote_api_url("TASK_STATUS", task_id="abc123")
        # 返回: "http://12.148.158.61:6677/tasks/abc123"
    """
    base_url = REMOTE_API_CONFIG["BASE_URL"]
    endpoint = REMOTE_API_CONFIG.get(endpoint_key, "")

    # 格式化路径参数
    if kwargs:
        endpoint = endpoint.format(**kwargs)

    return f"{base_url}{endpoint}"
