from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    CREATED = "created"
    TRAINING = "training"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"
    IDLE = "idle"

class NodeStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    TRAINING = "training"
    IDLE = "idle"
    ERROR = "error"

class NodeType(str, Enum):
    CONTROL = "control"
    EDGE = "edge"
    GATEWAY = "gateway"

class ProjectType(str, Enum):
    MANUFACTURING = "manufacturing"
    TRAFFIC = "traffic"
    MEDICAL = "medical"
    RETAIL = "retail"
    AGRICULTURE = "agriculture"
    FINANCE = "finance"
    ENERGY = "energy"
    SECURITY = "security"
    LOGISTICS = "logistics"
    EDUCATION = "education"
    AUTOMOTIVE = "automotive"
    ENVIRONMENT = "environment"

class ModelType(str, Enum):
    CNN = "cnn"
    RNN = "rnn"
    TRANSFORMER = "transformer"
    LSTM = "lstm"
    GRU = "gru"
    GEMMA = "Gemma"
    OPENVLA = "OpenVLA"
    LLAMA = "LLaMA"
    QWEN = "Qwen"

# 训练算法选项 (不再使用枚举，直接使用字符串以提高灵活性)
# Available training algorithms: "sft", "dpo", "grpo", "ipo", "kto"
# Available federated algorithms: "fedavg", "fedygi", "fedadam", "fedavgm"

class NodeCreateRequest(BaseModel):
    ip: str
    name: Optional[str] = None

class ProjectCreateRequest(BaseModel):
    name: str
    description: str
    model: str  # 与数据库table IP连接的字段
    nodes: List[NodeCreateRequest]  # 与数据库node table连接的字段，支持多个节点

    # 统一的训练参数 (合并后的字段)
    training_alg: str = "sft"           # 合并 training_strategy
    fed_alg: str = "fedavg"             # 合并 protocol
    secure_aggregation: str = "shamir_threshold"

    # 训练配置
    total_epochs: int = 100             # 合并 epochs，重命名为total_epochs
    num_rounds: int = 10                # 联邦学习轮次
    batch_size: int = 32
    lr: str = "1e-4"                    # 合并 learning_rate，统一使用String类型

    # 高级训练参数
    num_computers: int = 3
    threshold: int = 2
    num_clients: int = 2
    sample_clients: int = 2
    max_steps: int = 100

    # 模型和数据集配置
    model_name_or_path: str = "sshleifer/tiny-gpt2"
    dataset_name: str = "vicgalle/alpaca-gpt4"
    dataset_sample: int = 50

    created_time: Optional[datetime] = None  # 建立时间

class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    model: str
    status: ProjectStatus
    progress: float
    connected_nodes: int
    current_epoch: int

    # 统一的训练参数 (合并后的字段)
    training_alg: str                   # 原 training_strategy
    fed_alg: str                        # 原 protocol
    secure_aggregation: str

    # 训练配置
    total_epochs: int                   # 原 epochs，重命名为total_epochs
    num_rounds: int                     # 联邦学习轮次
    batch_size: int
    lr: str                             # 原 learning_rate，改为String类型

    # 高级训练参数
    num_computers: int
    threshold: int
    num_clients: int
    sample_clients: int
    max_steps: int

    # 模型和数据集配置
    model_name_or_path: str
    dataset_name: str
    dataset_sample: int

    # 其他信息
    node_ip: str
    created_time: str
    last_update: str
    metrics: Optional[Dict[str, float]] = None

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
    current_epoch: Optional[int] = None
    total_epochs: Optional[int] = None
    last_seen: str
    connections: List[str]

class SystemStats(BaseModel):
    total_projects: int
    active_projects: int
    total_nodes: int
    online_nodes: int
    training_nodes: int
    error_nodes: int
    completion_rate: float

class TrainingMetrics(BaseModel):
    accuracy: float
    loss: float
    f1_score: float
    precision: float
    recall: float

class NodeOperationRequest(BaseModel):
    operation: str  # start, stop, restart, assign
    project_id: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

class ProjectImportRequest(BaseModel):
    project_data: Dict[str, Any]
    overwrite: bool = False

class ProjectExportRequest(BaseModel):
    include_models: bool = True
    include_data: bool = False
    format: str = "json"

class PerformanceMetrics(BaseModel):
    node_id: str
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    gpu_usage: float
    network_usage: float
    temperature: Optional[float] = None
    power_consumption: Optional[float] = None

class LogEntry(BaseModel):
    id: str
    level: str
    message: str
    timestamp: datetime
    node_id: Optional[str] = None
    project_id: Optional[str] = None

class TaskRequest(BaseModel):
    project_id: str
    task_type: str
    priority: int = 1
    config: Optional[Dict[str, Any]] = None
    target_nodes: Optional[List[str]] = None

class TaskResponse(BaseModel):
    id: str
    project_id: str
    task_type: str
    status: str
    priority: int
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float
    assigned_nodes: List[str]
    config: Dict[str, Any]

# Test API Training Schemas
class TrainingParameters(BaseModel):
    training_alg: str = "sft"
    fed_alg: str = "fedavg"
    secure_aggregation: str = "shamir_threshold"
    num_computers: int = 3
    threshold: int = 2
    num_rounds: int = 10
    num_clients: int = 2
    sample_clients: int = 2
    max_steps: int = 100
    lr: str = "1e-4"
    model_name_or_path: str = "sshleifer/tiny-gpt2"
    dataset_name: str = "vicgalle/alpaca-gpt4"
    dataset_sample: int = 50

class TrainRequest(BaseModel):
    parameters: TrainingParameters

class TrainingResponse(BaseModel):
    task_id: str
    status: str
    message: Optional[str] = None
