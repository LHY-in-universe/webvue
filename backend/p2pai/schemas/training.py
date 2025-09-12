from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class TrainingType(str, Enum):
    LOCAL = "local"
    FEDERATED = "federated"
    MPC = "mpc"

class TrainingStatus(str, Enum):
    CREATED = "created"
    TRAINING = "training"
    COMPLETED = "completed"
    PAUSED = "paused"
    ERROR = "error"
    IDLE = "idle"

class ModelType(str, Enum):
    CNN = "cnn"
    RNN = "rnn"
    TRANSFORMER = "transformer"
    LSTM = "lstm"
    GRU = "gru"

class ProjectCreateRequest(BaseModel):
    name: str
    description: str
    training_type: TrainingType
    model_type: ModelType
    dataset_path: Optional[str] = None
    hyperparameters: Optional[Dict[str, Any]] = None

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

class TrainingMetrics(BaseModel):
    accuracy: float
    loss: float
    f1_score: float
    precision: float
    recall: float

class NodeInfo(BaseModel):
    id: str
    name: str
    type: str
    status: str
    project: Optional[str] = None
    location: str
    cpu_usage: float
    memory_usage: float
    gpu_usage: float
    progress: float
    last_seen: str
    connections: List[str]

class FederatedRound(BaseModel):
    round_number: int
    participants: List[str]
    global_accuracy: float
    local_accuracies: Dict[str, float]
    aggregation_method: str
    completed_at: datetime

class MPCTrainingRequest(BaseModel):
    project_id: str
    participants: List[str]
    privacy_level: str
    encryption_method: str
    threshold: int

class LocalTrainingRequest(BaseModel):
    project_id: str
    dataset_config: Dict[str, Any]
    training_config: Dict[str, Any]

class TrainingStartRequest(BaseModel):
    project_id: str
    training_type: TrainingType
    config: Optional[Dict[str, Any]] = None

class TrainingStopRequest(BaseModel):
    project_id: str
    save_model: bool = True

class DatasetUploadRequest(BaseModel):
    project_id: str
    dataset_name: str
    dataset_type: str
    privacy_level: str
    description: Optional[str] = None

class ModelExportRequest(BaseModel):
    project_id: str
    format: str = "pytorch"  # pytorch, onnx, tensorflow
    include_weights: bool = True
    include_metadata: bool = True

class SystemStats(BaseModel):
    total_projects: int
    active_projects: int
    total_nodes: int
    online_nodes: int
    training_nodes: int
    error_nodes: int
    completion_rate: float
