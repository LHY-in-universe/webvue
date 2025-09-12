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

class ModelType(str, Enum):
    CNN = "cnn"
    RNN = "rnn"
    TRANSFORMER = "transformer"
    LSTM = "lstm"
    GRU = "gru"

class ProjectCreateRequest(BaseModel):
    name: str
    description: str
    type: ProjectType
    model_type: ModelType
    hyperparameters: Optional[Dict[str, Any]] = None
    target_nodes: Optional[List[str]] = None

class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    type: ProjectType
    status: ProjectStatus
    progress: float
    connected_nodes: int
    current_epoch: int
    total_epochs: int
    model_type: ModelType
    batch_size: int
    learning_rate: float
    created: str
    last_update: str
    metrics: Dict[str, float]

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
