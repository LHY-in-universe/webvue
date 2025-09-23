# Training Monitor API Mock

这是一个模拟训练监控API的服务，提供与原始API相同的接口格式，但返回随机生成的数据。

## 功能特性

- 🎯 **完全兼容**: 输入输出格式与原始API完全相同
- 🎲 **随机数据**: 所有输出数据都是随机生成的
- 📊 **实时模拟**: 模拟真实的训练监控场景
- 🚀 **快速部署**: 一键启动，无需复杂配置

## API接口

### 1. 集群节点信息
```
GET /monitor/ray/cluster/node
```
返回集群中所有节点的信息和状态。

### 2. 集群状态
```
GET /monitor/ray/cluster/status
```
返回集群的整体状态和统计信息。

### 3. 训练监控
```
GET /monitor/training/{task_id}
```
返回指定训练任务的监控信息，包括进度、损失、准确率等。

### 4. 节点指标
```
GET /monitor/ray/cluster/node/{node_id}/metrics
```
返回特定节点的详细性能指标。

## 快速开始

### 方法1: 使用启动脚本（推荐）
```bash
chmod +x start.sh
./start.sh
```

### 方法2: 手动启动
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

## 访问地址

- **API服务**: http://localhost:6677
- **API文档**: http://localhost:6677/docs
- **健康检查**: http://localhost:6677/health

## 数据模型

### 节点信息 (RayNode)
- `id`: 节点唯一标识
- `name`: 节点名称
- `ip`: 节点IP地址
- `state`: 节点状态 (ALIVE/DEAD/UNKNOWN)
- `resources`: 资源信息 (CPU/内存/GPU)
- `training`: 训练任务信息（可选）

### 训练监控 (TrainingMonitorResponse)
- `task_id`: 任务ID
- `status`: 任务状态
- `progress`: 训练进度 (0-1)
- `current_epoch`: 当前轮次
- `total_epochs`: 总轮次
- `loss`: 损失值
- `accuracy`: 准确率（可选）
- `estimated_time_remaining`: 预估剩余时间
- `nodes_involved`: 参与节点列表

## 测试示例

### 获取集群节点
```bash
curl http://localhost:6677/monitor/ray/cluster/node
```

### 获取训练监控
```bash
curl http://localhost:6677/monitor/training/task_123
```

### 获取节点指标
```bash
curl http://localhost:6677/monitor/ray/cluster/node/node_1234/metrics
```

## 配置说明

- **端口**: 6677 (与原始API保持一致)
- **主机**: 0.0.0.0 (允许外部访问)
- **数据**: 完全随机生成，每次请求都不同

## 注意事项

1. 这是一个模拟服务，所有数据都是随机生成的
2. 每次重启服务，生成的节点ID和任务ID都会变化
3. 数据不持久化，重启后丢失
4. 主要用于开发和测试环境

## 故障排除

### 端口被占用
如果6677端口被占用，可以修改 `main.py` 文件中的端口号：
```python
uvicorn.run(app, host="0.0.0.0", port=6678)  # 改为6678或其他端口
```

### 依赖安装失败
确保Python版本 >= 3.8：
```bash
python3 --version
```

### 虚拟环境问题
删除并重新创建虚拟环境：
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
