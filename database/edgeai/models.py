from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, DECIMAL, Index
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Should be hashed
    active_token = Column(String(255), nullable=True, index=True)  # 用户当前活跃的token
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")

    # Training algorithm configuration (统一使用training_alg，删除重复的strategy)
    training_alg = Column(String(100), default="sft")
    fed_alg = Column(String(100), default="fedavg")  # 统一使用fed_alg，删除重复的protocol
    secure_aggregation = Column(String(100), default="shamir_threshold")

    # Training parameters
    total_epochs = Column(Integer, default=100)  # 重命名epoches为total_epochs
    num_rounds = Column(Integer, default=10)     # 联邦学习轮次，与total_epochs区分
    batch_size = Column(Integer, default=32)
    lr = Column(String(50), default="1e-4")      # 统一使用String类型的lr，删除Float类型的learning_rate

    # Advanced training parameters
    num_computers = Column(Integer, default=3)
    threshold = Column(Integer, default=2)
    num_clients = Column(Integer, default=2)
    sample_clients = Column(Integer, default=2)
    max_steps = Column(Integer, default=100)

    # Model and dataset configuration
    model_name_or_path = Column(String(500), default="sshleifer/tiny-gpt2")
    dataset_name = Column(String(200), default="vicgalle/alpaca-gpt4")
    dataset_sample = Column(Integer, default=50)

    # Project status
    status = Column(String(50), default="pending")
    progress = Column(DECIMAL(5,2), default=0.00)
    task_id = Column(String(100), default="")

    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    project_id = Column(Integer, nullable=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    file_path = Column(String(500), default="")
    version = Column(String(50), default="1.0.0")
    size = Column(DECIMAL(10,2), default=0.00)  # File size in MB
    class_config = Column(JSON, default={})
    status = Column(String(50), default="created")
    progress = Column(DECIMAL(5,2), default=0.00)
    loss = Column(DECIMAL(8,2), default=0.00)
    accuracy = Column(DECIMAL(5,2), default=0.00)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    cluster_id = Column(Integer, nullable=True)
    name = Column(String(200), nullable=False)
    path_ipv4 = Column(String(15), default="")  # IPv4 address
    progress = Column(DECIMAL(5,2), default=0.00)
    state = Column(String(50), default="idle")  # alive, dead, idle
    type = Column(String(50), nullable=False)

    # Resource information to match testapi format
    cpu_usage = Column(DECIMAL(5,2), default=0.00)     # CPU usage percentage
    memory_usage = Column(DECIMAL(5,2), default=0.00)  # Memory usage percentage
    disk_usage = Column(DECIMAL(5,2), default=0.00)    # Disk usage percentage
    sent = Column(DECIMAL(10,2), default=0.00)          # Data sent (MB)
    received = Column(DECIMAL(10,2), default=0.00)      # Data received (MB)
    heartbeat = Column(String(50), default="") # Heartbeat timestamp

    # Legacy fields (keeping for backward compatibility)
    cpu = Column(String(100), default="")
    gpu = Column(String(100), default="")
    memory = Column(String(50), default="")

    created_time = Column(DateTime(timezone=True), server_default=func.now())
    last_updated_time = Column(DateTime(timezone=True), onupdate=func.now())


class TaskQueue(Base):
    """
    任务队列表 - 管理训练任务的排队和调度
    """
    __tablename__ = "task_queue"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)

    # 队列状态: queued, running, completed, failed, cancelled
    status = Column(String(20), default="queued", nullable=False)

    # 优先级 (数字越小优先级越高, 默认为5)
    priority = Column(Integer, default=5, nullable=False)

    # 任务配置信息 (JSON格式)
    task_config = Column(JSON, default={})

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # 重试相关
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    # 错误信息
    error_message = Column(Text, nullable=True)

    # 外部任务ID (如TestAPI返回的task_id)
    external_task_id = Column(String(100), nullable=True)

    # 创建索引以优化查询性能
    __table_args__ = (
        # 复合索引：按状态、优先级、创建时间排序
        Index('idx_queue_order', 'status', 'priority', 'created_at'),
        # 项目ID索引
        Index('idx_project_queue', 'project_id', 'status'),
    )



class Cluster(Base):
    """
    集群表 - 管理集群信息
    """
    __tablename__ = "cluster"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)
    project_id = Column(Integer, nullable=True)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    last_updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    # 创建索引以优化查询性能
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_project_id', 'project_id'),
    )



# 更新Project模型，添加与TaskQueue的关系
# 需要在Project类中添加：
# task_queues = relationship("TaskQueue", back_populates="project", cascade="all, delete-orphan")


