# EdgeAI Database

This directory contains the database configuration and models for the EdgeAI system.

## Structure

```
edgeai/
├── __init__.py          # Module exports
├── database.py          # Database connection and configuration
├── models.py           # SQLAlchemy ORM models
├── init_db.py          # Database initialization script
├── alembic/            # Alembic migration files
└── README.md           # This file
```

## Database Models

### User
- **id**: Primary key
- **name**: User's display name
- **email**: Unique email address
- **password**: Hashed password
- **created_time**: Record creation timestamp
- **updated_time**: Record update timestamp

### Project
- **id**: Primary key
- **user_id**: Foreign key to User
- **name**: Project name
- **description**: Project description
- **strategy**: AI/ML strategy (e.g., Computer Vision, NLP)
- **protocol**: Communication protocol (HTTP, gRPC, etc.)
- **epoches**: Number of training epochs
- **learning_rate**: Learning rate for training
- **batch_size**: Batch size for training
- **status**: Current status (pending, active, completed)
- **progress**: Completion percentage
- **task_id**: Associated task identifier
- **created_time**: Record creation timestamp
- **updated_time**: Record update timestamp

### Model
- **id**: Primary key
- **user_id**: Foreign key to User
- **project_id**: Foreign key to Project (optional)
- **name**: Model name
- **description**: Model description
- **file_path**: Path to model file
- **version**: Model version
- **size**: File size in MB
- **class_config**: JSON configuration
- **status**: Training status (created, training, trained)
- **progress**: Training progress percentage
- **loss**: Training loss value
- **accuracy**: Model accuracy score
- **created_time**: Record creation timestamp
- **updated_time**: Record update timestamp

### Node
- **id**: Primary key
- **user_id**: Foreign key to User
- **project_id**: Foreign key to Project (optional)
- **name**: Node name
- **path_ipv4**: IPv4 address of the node
- **progress**: Current task progress
- **state**: Current state (idle, training, processing)
- **role**: Node role (worker, trainer, etc.)
- **cpu**: CPU specification
- **gpu**: GPU specification
- **memory**: Memory specification
- **created_time**: Record creation timestamp
- **last_updated_time**: Last update timestamp

## Initialization

### First Time Setup

1. Initialize the database:
```bash
python database/edgeai/init_db.py
```

2. Create migration (if models change):
```bash
alembic revision --autogenerate -m "Initial migration"
```

3. Apply migration:
```bash
alembic upgrade head
```

### Reset Database

To completely reset the database:
```bash
python database/edgeai/init_db.py --reset
```

## Environment Variables

- `EDGEAI_DATABASE_URL`: Database connection URL (default: sqlite:///./database/edgeai/edgeai.db)

## Usage in FastAPI

```python
from database.edgeai import get_db, User, Project, Model, Node
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}/projects")
def get_user_projects(user_id: int, db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.user_id == user_id).all()

@app.get("/projects/{project_id}/models")
def get_project_models(project_id: int, db: Session = Depends(get_db)):
    return db.query(Model).filter(Model.project_id == project_id).all()

@app.get("/projects/{project_id}/nodes")
def get_project_nodes(project_id: int, db: Session = Depends(get_db)):
    return db.query(Node).filter(Node.project_id == project_id).all()
```

## Migration Commands

- Create new migration: `alembic revision --autogenerate -m "description"`
- Apply migrations: `alembic upgrade head`
- Downgrade: `alembic downgrade -1`
- Show current revision: `alembic current`
- Show migration history: `alembic history`