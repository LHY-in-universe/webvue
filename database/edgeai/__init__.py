"""
EdgeAI Database Module

This module provides database models, connections, and utilities for the EdgeAI system.
"""

from .database import Base, engine, SessionLocal, get_db, create_tables, drop_tables, get_database_info
from .models import User, Project, Model, Node, TaskQueue

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "create_tables",
    "drop_tables",
    "get_database_info",
    "User",
    "Project",
    "Model",
    "Node",
    "TaskQueue"
]