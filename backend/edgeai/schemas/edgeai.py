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
    
    # Training configuration fields (from frontend form)
    training_alg: Optional[str] = "sft"
    fed_alg: Optional[str] = "fedavg"
    num_rounds: Optional[int] = 10
    num_clients: Optional[int] = 2
    sample_clients: Optional[int] = 2
    max_steps: Optional[int] = 100
    lr: Optional[str] = "1e-4"
    dataset_sample: Optional[int] = 50
    model_name_or_path: Optional[str] = ""
    dataset_name: Optional[str] = ""
    
    # Legacy fields (for backward compatibility)
    model: Optional[str] = ""
    training_strategy: Optional[TrainingStrategy] = TrainingStrategy.SFT
    protocol: Optional[Protocol] = Protocol.FEDAVG
    epochs: Optional[int] = 100
    batch_size: Optional[int] = 32
    learning_rate: Optional[float] = 0.001
    node_ip: Optional[str] = ""
    created_time: Optional[datetime] = None

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
