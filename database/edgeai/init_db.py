"""
Database initialization script for EdgeAI
"""
import os
import sys
from pathlib import Path

# Add the current directory to Python path for direct imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from sqlalchemy.exc import IntegrityError
from .database import engine, SessionLocal, create_tables
from .models import User, Project, Model, Node, Cluster
from passlib.context import CryptContext
from datetime import datetime

# Password hashing
import hashlib

def hash_password(password: str) -> str:
    # 使用简单的SHA256哈希，避免bcrypt兼容性问题
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_database():
    """Initialize the EdgeAI database with tables and sample data"""
    print("Initializing EdgeAI database...")

    # Create all tables
    create_tables()
    print("✓ Database tables created")

    # Create sample data
    db = SessionLocal()
    try:
        # Create sample users
        users_data = [
            {
                "name": "Admin User",
                "email": "admin@edgeai.com",
                "password": hash_password("admin123")
            },
            {
                "name": "Test User",
                "email": "user@edgeai.com",
                "password": hash_password("user123")
            }
        ]

        created_users = []
        for user_data in users_data:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(**user_data)
                db.add(user)
                db.flush()  # Flush to get the ID
                created_users.append(user)
                print(f"✓ Created user: {user.email}")
            else:
                created_users.append(existing_user)
                print(f"• User already exists: {existing_user.email}")
                
        print(f"✓ Created users: {created_users}")

        # Create sample clusters  
        if created_users:
            admin_user = created_users[0]      
            clusters_data = [
                {
                    "name": "Cluster 1 (db)",
                "user_id": admin_user.id
                },
                {
                "name": "Cluster 2 (db)",
                "user_id": admin_user.id
                }
            ]
            created_clusters = []
            for cluster_data in clusters_data:
                existing_cluster = db.query(Cluster).filter(
                    Cluster.name == cluster_data["name"],
                    Cluster.user_id == cluster_data["user_id"]
                ).first()
                if not existing_cluster:
                    cluster = Cluster(**cluster_data)
                    db.add(cluster)
                    db.flush()
                    created_clusters.append(cluster)
                    print(f"✓ Created cluster: {cluster.name}")
                else:
                    created_clusters.append(existing_cluster)
                    print(f"• Cluster already exists: {existing_cluster.name}")

        print(f"✓ Created clusters: {created_clusters}")            

        # Create sample projects
        if created_clusters:
            cluster_1 = created_clusters[0]
            projects_data = [
                {
                    "name": "1Image Recognition Model (db)",
                    "description": "A deep learning model for image classification",
                    "training_alg": "sft",
                    "fed_alg": "fedavg",
                    "total_epochs": 100,
                    "lr": "1e-3",
                    "batch_size": 32,
                    "status": "active",
                    "progress": 25.5,
                    "task_id": "task_001",
                    "user_id": admin_user.id
                },
                {
                    "name": "2NLP Sentiment Analysis (db)",
                    "description": "Natural language processing for sentiment analysis",
                    "training_alg": "sft",
                    "fed_alg": "fedavg",
                    "total_epochs": 50,
                    "lr": "1e-4",
                    "batch_size": 16,
                    "status": "pending",
                    "progress": 0.0,
                    "task_id": "task_002",
                    "user_id": admin_user.id
                }
            ]

            created_projects = []
            for project_data in projects_data:
                existing_project = db.query(Project).filter(
                    Project.name == project_data["name"],
                    Project.user_id == project_data["user_id"]
                ).first()

                if not existing_project:
                    project = Project(**project_data)
                    db.add(project)
                    db.flush()
                    created_projects.append(project)
                    print(f"✓ Created project: {project.name}")
                else:
                    created_projects.append(existing_project)
                    print(f"• Project already exists: {existing_project.name}")

            print(f"✓ Created projects: {created_projects}")

            # Create sample models
            if created_projects:
                models_data = [
                    {
                        "name": "21ResNet-50 Custom (db)",
                        "description": "Custom ResNet-50 model for image classification",
                        "file_path": "/models/resnet50_custom.pth",
                        "version": "1.0.0",
                        "size": 97.8,
                        "class_config": {"layers": 50, "classes": 1000, "input_size": [224, 224, 3]},
                        "status": "trained",
                        "progress": 100.0,
                        "loss": 0.15,
                        "accuracy": 0.95,
                        "user_id": admin_user.id,
                        "project_id": created_projects[0].id
                    },
                    {
                        "name": "21BERT Base (db)",
                        "description": "BERT base model for sentiment analysis",
                        "file_path": "/models/bert_base.bin",
                        "version": "1.1.0",
                        "size": 440.0,
                        "class_config": {"vocab_size": 30522, "hidden_size": 768, "num_layers": 12},
                        "status": "training",
                        "progress": 65.0,
                        "loss": 0.34,
                        "accuracy": 0.82,
                        "user_id": admin_user.id,
                        "project_id": created_projects[1].id if len(created_projects) > 1 else created_projects[0].id
                    }
                ]

                for model_data in models_data:
                    existing_model = db.query(Model).filter(
                        Model.name == model_data["name"],
                        Model.user_id == model_data["user_id"]
                    ).first()

                    if not existing_model:
                        model = Model(**model_data)
                        db.add(model)
                        print(f"✓ Created model: {model.name}")
                    else:
                        print(f"• Model already exists: {existing_model.name}")

                print(f"✓ Created models: {models_data}")

                # Create sample nodes
                nodes_data = [
                    {
                        "name": "22GPU Training Node 1 (db)",
                        "path_ipv4": "192.168.1.101",
                        "progress": 45.0,
                        "state": "training",
                        "type": "training",
                        "cpu": "Intel i9-12900K",
                        "gpu": "RTX 4090 24GB",
                        "memory": "32GB DDR4",
                        "user_id": admin_user.id
                    },
                    {
                        "name": "122GPU Training Node 1 (db)",
                        "path_ipv4": "192.168.1.101",
                        "progress": 45.0,
                        "state": "training",
                        "type": "training",
                        "cpu": "Intel i9-12900K",
                        "gpu": "RTX 4090 24GB",
                        "memory": "32GB DDR4",
                        "user_id": admin_user.id
                    },
                    {
                        "name": "2122GPU Training Node 1 (db)",
                        "path_ipv4": "192.168.1.101",
                        "progress": 45.0,
                        "state": "training",
                        "type": "training",
                        "cpu": "Intel i9-12900K",
                        "gpu": "RTX 4090 24GB",
                        "memory": "32GB DDR4",
                        "user_id": admin_user.id
                    },
                    {
                        "name": "222222GPU Training Node 1 (db)",
                        "path_ipv4": "192.168.1.101",
                        "progress": 45.0,
                        "state": "training",
                        "type": "training",
                        "cpu": "Intel i9-12900K",
                        "gpu": "RTX 4090 24GB",
                        "memory": "32GB DDR4",
                        "user_id": admin_user.id
                    },
                    {
                        "name": "322GPU Training Node 1 (db)",
                        "path_ipv4": "192.168.1.101",
                        "progress": 45.0,
                        "state": "training",
                        "type": "training",
                        "cpu": "Intel i9-12900K",
                        "gpu": "RTX 4090 24GB",
                        "memory": "32GB DDR4",
                        "user_id": admin_user.id
                    },
                    {
                        "name": "3422GPU Training Node 1 (db)",
                        "path_ipv4": "192.168.1.101",
                        "progress": 45.0,
                        "state": "training",
                        "type": "training",
                        "cpu": "Intel i9-12900K",
                        "gpu": "RTX 4090 24GB",
                        "memory": "32GB DDR4",
                        "user_id": admin_user.id
                    },
                    {
                        "name": "11CPU Processing Node 1 (db)",
                        "path_ipv4": "192.168.1.102",
                        "progress": 30.0,
                        "state": "training",
                        "type": "worker",
                        "cpu": "AMD Ryzen 7 5800X",
                        "gpu": "",
                        "memory": "16GB DDR4",
                        "user_id": admin_user.id
                    }
                ]

                for node_data in nodes_data:
                    existing_node = db.query(Node).filter(
                        Node.name == node_data["name"],
                        Node.user_id == node_data["user_id"]
                    ).first()
                    if not existing_node:
                        node = Node(**node_data)
                        db.add(node)
                        print(f"✓ Created node: {node.name}")
                    else:
                        print(f"• Node already exists: {existing_node.name}")


        # Commit all changes
        db.commit()
        print("✓ Sample data inserted successfully")

    except IntegrityError as e:
        db.rollback()
        print(f"⚠ Some data already exists, skipping duplicates: {e}")
    except Exception as e:
        db.rollback()
        print(f"✗ Error inserting sample data: {e}")
        raise
    finally:
        db.close()

    print("✅ EdgeAI database initialization completed!")

def reset_database():
    """Reset the database by dropping and recreating all tables"""
    print("⚠ Resetting EdgeAI database...")
    from .database import drop_tables

    # Drop all tables
    drop_tables()
    print("✓ All tables dropped")

    # Recreate tables and sample data
    init_database()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="EdgeAI Database Initialization")
    parser.add_argument("--reset", action="store_true", help="Reset database (drop and recreate)")
    args = parser.parse_args()

    if args.reset:
        reset_database()
    else:
        init_database()