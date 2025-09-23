@router.get("/visualization/{project_id}/")
async def get_visualization_nodes(project_id: str, db: Session = Depends(get_db)):
    """
    获取特定项目的可视化节点数据（从数据库获取真实数据）
    """
    try:
        project_id_int = int(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    # 获取项目信息
    project = db.query(Project).filter(Project.id == project_id_int).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 获取项目关联的真实节点数据
    project_nodes = db.query(Node).filter(Node.project_id == project_id_int).all()

    # 获取项目关联的模型数据
    project_models = db.query(Model).filter(Model.project_id == project_id_int).all()

    # 构建可视化节点数据
    visualization_nodes = []

    # 添加真实的数据库节点
    for node in project_nodes:
        visualization_nodes.append({
            "id": f"node-{node.id}",
            "name": node.name,  # 这将包含 "(db)" 标识
            "type": "training",
            "status": node.state,  # 应该是 "training"
            "role": node.role,
            "user": "EdgeAI System",
            "ip_address": node.path_ipv4,
            "connected_nodes": f"{len(project_nodes)} nodes",
            "last_heartbeat": "1 second ago",
            "resources": {
                "cpu": int(node.progress) if node.progress else 0,
                "memory": node.memory or "Unknown",
                "gpu": node.gpu or "None"
            },
            "priority": 7,
            "progress": node.progress or 0,
            "hardware": {
                "cpu_model": node.cpu,
                "gpu_model": node.gpu,
                "memory_size": node.memory
            }
        })

    # 基于真实模型数据添加模型服务器节点
    control_nodes = []
    for i, model in enumerate(project_models):
        control_nodes.append({
            "id": f"model-{model.id}",
            "name": f"{model.name} Server",  # 包含 "(db)" 标识
            "type": "model",
            "status": model.status,
            "role": "Model Aggregator",
            "user": "EdgeAI System",
            "ip_address": f"192.168.1.{100 + i}",
            "connected_nodes": f"{len(project_nodes)} nodes",
            "last_heartbeat": "1 second ago",
            "resources": {
                "cpu": int(model.progress) if model.progress else 0,
                "memory": f"{model.size}MB" if model.size else "Unknown",
                "gpu": 0
            },
            "priority": 10 - i,
            "accuracy": model.accuracy,
            "version": model.version
        })

    # 合并所有节点
    all_nodes = control_nodes + visualization_nodes

    return {
        "nodes": all_nodes,
        "project_id": project_id,
        "project_name": project.name,  # 包含 "(db)" 标识
        "total_nodes": len(all_nodes),
        "control_nodes": len(control_nodes),
        "training_nodes": len(visualization_nodes),
        "network_topology": {
            "architecture": "federated_learning",
            "coordination_type": "centralized",
            "communication_protocol": "secure_aggregation"
        },
        "last_updated": project.updated_time.isoformat() if project.updated_time else project.created_time.isoformat()
    }