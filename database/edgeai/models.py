from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Should be hashed
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    models = relationship("Model", back_populates="user", cascade="all, delete-orphan")
    nodes = relationship("Node", back_populates="user", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
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
    progress = Column(Float, default=0.0)
    task_id = Column(String(100), default="")

    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="projects")
    models = relationship("Model", back_populates="project", cascade="all, delete-orphan")
    nodes = relationship("Node", back_populates="project", cascade="all, delete-orphan")

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    file_path = Column(String(500), default="")
    version = Column(String(50), default="1.0.0")
    size = Column(Float, default=0.0)  # File size in MB
    class_config = Column(JSON, default={})
    status = Column(String(50), default="created")
    progress = Column(Float, default=0.0)
    loss = Column(Float, default=0.0)
    accuracy = Column(Float, default=0.0)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="models")
    project = relationship("Project", back_populates="models")

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    name = Column(String(200), nullable=False)
    path_ipv4 = Column(String(15), default="")  # IPv4 address
    progress = Column(Float, default=0.0)
    state = Column(String(50), default="idle")
    role = Column(String(50), default="worker")
    cpu = Column(String(100), default="")
    gpu = Column(String(100), default="")
    memory = Column(String(50), default="")
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    last_updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="nodes")
    project = relationship("Project", back_populates="nodes")


