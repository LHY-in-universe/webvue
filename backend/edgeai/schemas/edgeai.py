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

class TrainingStrategy(str, Enum):
    SFT = "sft"
    DPO = "dpo"
    GRPO = "grpo"
    IPO = "ipo"
    KTO = "kto"

class Protocol(str, Enum):
    FEDAVG = "fedavg"
    FEDYGI = "fedygi"
    FEDADAM = "fedadam"
    FEDAVGM = "fedavgm"

class ProjectCreateRequest(BaseModel):
    name: str
    description: str
    model: str  # 与数据库table IP连接的字段
    training_strategy: TrainingStrategy
    protocol: Protocol
    epochs: int
    batch_size: int
    learning_rate: float
    node_ip: str  # 与数据库node table连接的字段
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
    total_epochs: int
    training_strategy: TrainingStrategy
    protocol: Protocol
    epochs: int
    batch_size: int
    learning_rate: float
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
