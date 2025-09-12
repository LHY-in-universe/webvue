# OpenTMP LLM Engine Backend API

基于FastAPI构建的分布式机器学习后端API，支持P2P AI和Edge AI两个主要模块。

## 项目结构

```
backend/
├── main.py                 # FastAPI应用入口
├── requirements.txt        # Python依赖
├── global/                 # 全局模块
│   ├── api/               # API路由
│   │   ├── auth.py        # 认证相关接口
│   │   └── system.py      # 系统相关接口
│   └── schemas/           # 数据模型
│       ├── auth.py        # 认证数据模型
│       └── common.py      # 通用数据模型
├── p2pai/                 # P2P AI模块
│   ├── api/               # API路由
│   │   ├── projects.py    # 项目管理
│   │   ├── training.py    # 训练管理
│   │   ├── nodes.py       # 节点管理
│   │   ├── datasets.py    # 数据集管理
│   │   └── models.py      # 模型管理
│   └── schemas/           # 数据模型
│       └── training.py    # 训练相关数据模型
└── edgeai/                # Edge AI模块
    ├── api/               # API路由
    │   ├── projects.py    # 项目管理
    │   ├── nodes.py       # 节点管理
    │   ├── training.py    # 训练管理
    │   ├── performance.py # 性能监控
    │   ├── logs.py        # 日志管理
    │   └── tasks.py       # 任务管理
    └── schemas/           # 数据模型
        └── edgeai.py      # Edge AI数据模型
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

```bash
python3 main.py
```

服务将在 `http://localhost:8000` 启动

### API文档

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API模块说明

### 全局模块 (Global)

#### 认证接口 (`/api/global/auth`)

- `POST /login` - 用户登录
- `POST /logout` - 用户登出
- `GET /user/{user_id}` - 获取用户信息
- `PUT /user/{user_id}/preferences` - 更新用户偏好

#### 系统接口 (`/api/global/system`)

- `GET /health` - 系统健康检查
- `GET /system-info` - 获取系统信息
- `GET /logs` - 获取系统日志
- `GET /notifications` - 获取通知列表
- `GET /stats` - 获取全局统计

### P2P AI模块 (`/api/p2pai`)

#### 项目管理 (`/api/p2pai/projects`)

- `GET /` - 获取项目列表
- `GET /{project_id}` - 获取项目详情
- `POST /` - 创建项目
- `PUT /{project_id}` - 更新项目
- `DELETE /{project_id}` - 删除项目
- `GET /stats/overview` - 获取项目统计

#### 训练管理 (`/api/p2pai/training`)

- `POST /start` - 开始训练
- `POST /stop` - 停止训练
- `POST /local` - 开始本地训练
- `POST /federated/start` - 开始联邦学习
- `POST /mpc/start` - 开始MPC训练
- `GET /sessions` - 获取训练会话
- `GET /metrics/{project_id}` - 获取训练指标
- `WebSocket /ws/{project_id}` - 训练实时监控

#### 节点管理 (`/api/p2pai/nodes`)

- `GET /` - 获取节点列表
- `GET /{node_id}` - 获取节点详情
- `POST /{node_id}/start` - 启动节点
- `POST /{node_id}/stop` - 停止节点
- `POST /{node_id}/restart` - 重启节点
- `GET /stats/overview` - 获取节点统计

#### 数据集管理 (`/api/p2pai/datasets`)

- `GET /` - 获取数据集列表
- `POST /upload` - 上传数据集
- `POST /` - 创建数据集记录
- `DELETE /{dataset_id}` - 删除数据集
- `GET /{dataset_id}/download` - 下载数据集
- `GET /stats/overview` - 获取数据集统计

#### 模型管理 (`/api/p2pai/models`)

- `GET /` - 获取模型列表
- `POST /{model_id}/export` - 导出模型
- `POST /{model_id}/deploy` - 部署模型
- `POST /{model_id}/evaluate` - 评估模型
- `GET /{model_id}/versions` - 获取模型版本
- `GET /stats/overview` - 获取模型统计

### Edge AI模块 (`/api/edgeai`)

#### 项目管理 (`/api/edgeai/projects`)

- `GET /` - 获取项目列表
- `POST /` - 创建项目
- `POST /import` - 导入项目
- `POST /{project_id}/export` - 导出项目
- `POST /{project_id}/start` - 启动项目
- `POST /{project_id}/pause` - 暂停项目
- `POST /{project_id}/stop` - 停止项目

#### 节点管理 (`/api/edgeai/nodes`)

- `GET /` - 获取节点列表
- `POST /{node_id}/operation` - 执行节点操作
- `POST /{node_id}/start-training` - 启动节点训练
- `POST /{node_id}/stop-training` - 停止节点训练
- `WebSocket /ws/{node_id}` - 节点实时监控

#### 训练管理 (`/api/edgeai/training`)

- `POST /start` - 开始训练
- `POST /stop` - 停止训练
- `POST /batch-start` - 批量开始训练
- `POST /batch-stop` - 批量停止训练
- `WebSocket /ws/{project_id}` - 训练实时监控

#### 性能监控 (`/api/edgeai/performance`)

- `GET /metrics` - 获取性能指标
- `GET /summary` - 获取性能摘要
- `GET /alerts` - 获取性能告警
- `GET /trends` - 获取性能趋势
- `GET /health` - 获取系统健康状态

#### 日志管理 (`/api/edgeai/logs`)

- `GET /` - 获取日志列表
- `GET /search` - 搜索日志
- `GET /export` - 导出日志
- `POST /cleanup` - 清理日志
- `GET /realtime` - 获取实时日志

#### 任务管理 (`/api/edgeai/tasks`)

- `GET /` - 获取任务列表
- `POST /` - 创建任务
- `PUT /{task_id}/start` - 启动任务
- `PUT /{task_id}/stop` - 停止任务
- `POST /batch-create` - 批量创建任务
- `GET /queue` - 获取任务队列

## 数据模型

### 用户认证

```python
class LoginRequest(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    module: ModuleType

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    module: ModuleType
    user_type: UserType
    preferences: dict
    created_at: str
    last_login: str
```

### 项目模型

```python
class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    training_type: TrainingType
    model_type: ModelType
    status: TrainingStatus
    progress: float
    connected_nodes: int
    current_epoch: int
    total_epochs: int
    batch_size: int
    learning_rate: float
    created: str
    last_update: str
    metrics: Dict[str, float]
```

### 节点模型

```python
class NodeResponse(BaseModel):
    id: str
    name: str
    type: NodeType
    status: NodeStatus
    project: Optional[str] = None
    location: str
    cpu_usage: float
    memory_usage: float
    gpu_usage: float
    progress: float
    last_seen: str
    connections: List[str]
```

## WebSocket支持

### 训练监控

连接到 `ws://localhost:8000/api/p2pai/training/ws/{project_id}` 或 `ws://localhost:8000/api/edgeai/training/ws/{project_id}` 获取实时训练数据。

### 节点监控

连接到 `ws://localhost:8000/api/edgeai/nodes/ws/{node_id}` 获取实时节点性能数据。

## 错误处理

所有API都返回统一的错误格式：

```json
{
    "success": false,
    "error": "错误描述",
    "message": "详细错误信息"
}
```

## 认证

目前使用模拟认证，支持快速登录。在生产环境中应集成JWT或OAuth2认证。

## 开发说明

- 所有接口都包含完整的类型注解
- 使用Pydantic进行数据验证
- 支持CORS跨域请求
- 包含WebSocket实时通信
- 提供完整的API文档

## 部署

1. 安装依赖：`pip install -r requirements.txt`
2. 启动服务：`python main.py`
3. 或使用uvicorn：`uvicorn main:app --host 0.0.0.0 --port 8000`

## 注意事项

- 当前使用模拟数据，生产环境需要连接真实数据库
- WebSocket连接需要处理断线重连
- 大文件上传需要配置适当的超时时间
- 建议使用Redis进行会话管理和缓存
