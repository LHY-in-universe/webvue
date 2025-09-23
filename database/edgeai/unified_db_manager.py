#!/usr/bin/env python3
"""
统一的 EdgeAI 数据库管理文件
整合所有数据库相关功能：初始化、数据创建、测试、迁移等
"""

import sys
import os
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

# 添加项目根目录到路径
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from database import engine, SessionLocal, create_tables, drop_tables, get_db
from models import User, Project, Model, Node, NodeConnection, NodeMetric

# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class EdgeAIDatabaseManager:
    """EdgeAI 数据库统一管理器"""
    
    def __init__(self):
        self.db = None
    
    def get_session(self):
        """获取数据库会话"""
        if self.db is None:
            self.db = SessionLocal()
        return self.db
    
    def close_session(self):
        """关闭数据库会话"""
        if self.db:
            self.db.close()
            self.db = None
    
    def hash_password(self, password: str) -> str:
        """哈希密码"""
        return pwd_context.hash(password)
    
    def init_database(self, reset: bool = False):
        """初始化数据库"""
        print("🚀 开始初始化 EdgeAI 数据库...")
        
        if reset:
            print("⚠️ 重置数据库...")
            drop_tables()
            print("✅ 所有表已删除")
        
        # 创建所有表
        create_tables()
        print("✅ 数据库表创建完成")
        
        # 创建基础数据
        self._create_basic_data()
        
        print("🎉 EdgeAI 数据库初始化完成！")
    
    def _create_basic_data(self):
        """创建基础数据"""
        db = self.get_session()
        
        try:
            # 创建用户
            users = self._create_users(db)
            
            # 创建项目
            projects = self._create_projects(db, users)
            
            # 创建模型
            self._create_models(db, users, projects)
            
            # 创建节点
            self._create_nodes(db, users, projects)
            
            # 创建连接关系
            self._create_connections(db)
            
            # 创建性能指标
            self._create_metrics(db)
            
            db.commit()
            print("✅ 基础数据创建完成")
            
        except Exception as e:
            db.rollback()
            print(f"❌ 创建基础数据失败: {e}")
            raise
        finally:
            self.close_session()
    
    def _create_users(self, db) -> List[User]:
        """创建用户数据"""
        print("👤 创建用户数据...")
        
        users_data = [
            {
                "name": "System Administrator",
                "email": "admin@system.local",
                "password": self.hash_password("admin123")
            },
            {
                "name": "Test User",
                "email": "test@example.com", 
                "password": self.hash_password("test123")
            },
            {
                "name": "EdgeAI Developer",
                "email": "dev@edgeai.com",
                "password": self.hash_password("dev123")
            }
        ]
        
        created_users = []
        for user_data in users_data:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(**user_data)
                db.add(user)
                db.flush()
                created_users.append(user)
                print(f"  ✅ 创建用户: {user.name}")
            else:
                created_users.append(existing_user)
                print(f"  ⚠️ 用户已存在: {existing_user.name}")
        
        return created_users
    
    def _create_projects(self, db, users: List[User]) -> List[Project]:
        """创建项目数据"""
        print("📁 创建项目数据...")
        
        if not users:
            print("  ❌ 没有用户，跳过项目创建")
            return []
        
        admin_user = users[0]
        
        projects_data = [
            {
                "name": "Federated Learning Project",
                "description": "Distributed machine learning with privacy preservation",
                "training_alg": "sft",
                "fed_alg": "fedavg",
                "num_rounds": 10,
                "num_clients": 2,
                "sample_clients": 2,
                "max_steps": 100,
                "lr": "1e-4",
                "dataset_sample": 50,
                "model_name_or_path": "sshleifer/tiny-gpt2",
                "dataset_name": "vicgalle/alpaca-gpt4",
                "status": "completed",
                "progress": 100.0,
                "user_id": admin_user.id
            },
            {
                "name": "MPC Training Project",
                "description": "Multi-party computation for secure training",
                "training_alg": "dpo",
                "fed_alg": "fedprox",
                "num_rounds": 15,
                "num_clients": 3,
                "sample_clients": 2,
                "max_steps": 150,
                "lr": "2e-4",
                "dataset_sample": 100,
                "model_name_or_path": "microsoft/DialoGPT-medium",
                "dataset_name": "wikitext",
                "status": "training",
                "progress": 65.0,
                "user_id": admin_user.id
            },
            {
                "name": "Edge AI Inference",
                "description": "Real-time AI inference on edge devices",
                "training_alg": "ppo",
                "fed_alg": "scaffold",
                "num_rounds": 5,
                "num_clients": 1,
                "sample_clients": 1,
                "max_steps": 50,
                "lr": "5e-4",
                "dataset_sample": 25,
                "model_name_or_path": "gpt2",
                "dataset_name": "squad",
                "status": "pending",
                "progress": 0.0,
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
                print(f"  ✅ 创建项目: {project.name}")
            else:
                created_projects.append(existing_project)
                print(f"  ⚠️ 项目已存在: {existing_project.name}")
        
        return created_projects
    
    def _create_models(self, db, users: List[User], projects: List[Project]):
        """创建模型数据"""
        print("🤖 创建模型数据...")
        
        if not users or not projects:
            print("  ❌ 缺少用户或项目，跳过模型创建")
            return
        
        admin_user = users[0]
        main_project = projects[0]
        
        models_data = [
            {
                "name": "ResNet-50 Custom",
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
                "project_id": main_project.id
            },
            {
                "name": "BERT Base",
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
                "project_id": main_project.id
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
                print(f"  ✅ 创建模型: {model.name}")
            else:
                print(f"  ⚠️ 模型已存在: {existing_model.name}")
    
    def _create_nodes(self, db, users: List[User], projects: List[Project]):
        """创建节点数据"""
        print("🔧 创建节点数据...")
        
        if not users or not projects:
            print("  ❌ 缺少用户或项目，跳过节点创建")
            return
        
        admin_user = users[0]
        main_project = projects[0]
        
        # 检查是否已有节点数据
        existing_nodes = db.query(Node).count()
        if existing_nodes > 0:
            print(f"  ⚠️ 已存在 {existing_nodes} 个节点，跳过创建")
            return
        
        nodes_data = [
            # Model Nodes (模型节点)
            {
                "name": "database_model_001_ResNet50_Custom",
                "node_type": "model",
                "role": "Model Server",
                "state": "online",
                "responsible_user": "System",
                "path_ipv4": "192.168.1.100",
                "connected_nodes_count": 5,
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "gpu_usage": 82.1,
                "priority": 1,
                "location": "Data Center A",
                "specialty": "Computer Vision",
                "progress": 100.0,
                "cpu": "Intel Xeon E5-2680 v4",
                "gpu": "NVIDIA Tesla V100",
                "memory": "64GB DDR4",
                "hardware_info": '{"cores": 14, "threads": 28, "gpu_memory": "32GB", "storage": "1TB SSD"}',
                "network_latency": 12,
                "uptime": 99.5,
                "is_active": True,
                "user_id": admin_user.id,
                "project_id": main_project.id
            },
            {
                "name": "database_model_002_VGG16_ImageNet",
                "node_type": "model",
                "role": "Model Server",
                "state": "online",
                "responsible_user": "System",
                "path_ipv4": "192.168.1.101",
                "connected_nodes_count": 5,
                "cpu_usage": 38.7,
                "memory_usage": 52.3,
                "gpu_usage": 75.6,
                "priority": 1,
                "location": "Data Center A",
                "specialty": "Image Classification",
                "progress": 100.0,
                "cpu": "Intel Xeon E5-2680 v4",
                "gpu": "NVIDIA Tesla V100",
                "memory": "64GB DDR4",
                "hardware_info": '{"cores": 14, "threads": 28, "gpu_memory": "32GB", "storage": "1TB SSD"}',
                "network_latency": 15,
                "uptime": 98.8,
                "is_active": True,
                "user_id": admin_user.id,
                "project_id": main_project.id
            },
            {
                "name": "database_model_003_EfficientNet_B0",
                "node_type": "model",
                "role": "Model Server",
                "state": "training",
                "responsible_user": "System",
                "path_ipv4": "192.168.1.102",
                "connected_nodes_count": 5,
                "cpu_usage": 67.3,
                "memory_usage": 78.9,
                "gpu_usage": 89.2,
                "priority": 1,
                "location": "Data Center A",
                "specialty": "Efficient Networks",
                "progress": 75.0,
                "cpu": "Intel Xeon E5-2680 v4",
                "gpu": "NVIDIA Tesla V100",
                "memory": "64GB DDR4",
                "hardware_info": '{"cores": 14, "threads": 28, "gpu_memory": "32GB", "storage": "1TB SSD"}',
                "network_latency": 18,
                "uptime": 97.2,
                "is_active": True,
                "user_id": admin_user.id,
                "project_id": main_project.id
            },
            # Control Nodes (控制节点)
            {
                "name": "Coordination Center",
                "node_type": "control",
                "role": "Network Coordinator",
                "state": "online",
                "responsible_user": "System",
                "path_ipv4": "192.168.1.200",
                "connected_nodes_count": 5,
                "cpu_usage": 25.1,
                "memory_usage": 34.6,
                "gpu_usage": 0.0,
                "priority": 1,
                "location": "Control Center",
                "specialty": "Network Management",
                "progress": 0.0,
                "cpu": "Intel Xeon E5-2680 v4",
                "gpu": "None",
                "memory": "32GB DDR4",
                "hardware_info": '{"cores": 8, "threads": 16, "storage": "500GB SSD"}',
                "network_latency": 5,
                "uptime": 99.9,
                "is_active": True,
                "user_id": admin_user.id,
                "project_id": main_project.id
            },
            # Data Nodes (数据节点)
            {
                "name": "database_node_001_GPU_Training",
                "node_type": "data",
                "role": "Training Node",
                "state": "training",
                "responsible_user": "System",
                "path_ipv4": "192.168.1.201",
                "connected_nodes_count": 1,
                "cpu_usage": 80.4,
                "memory_usage": 76.1,
                "gpu_usage": 71.6,
                "priority": 2,
                "location": "Edge Location 1",
                "specialty": "GPU Training",
                "progress": 45.0,
                "cpu": "Intel Core i7-10700K",
                "gpu": "NVIDIA RTX 3080",
                "memory": "32GB DDR4",
                "hardware_info": '{"cores": 8, "threads": 16, "gpu_memory": "10GB", "storage": "1TB NVMe"}',
                "network_latency": 25,
                "uptime": 95.3,
                "is_active": True,
                "user_id": admin_user.id,
                "project_id": main_project.id
            },
            {
                "name": "database_node_002_GPU_Inference",
                "node_type": "data",
                "role": "Inference Node",
                "state": "inference",
                "responsible_user": "System",
                "path_ipv4": "192.168.1.202",
                "connected_nodes_count": 1,
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "gpu_usage": 0.0,
                "priority": 2,
                "location": "Edge Location 2",
                "specialty": "Real-time Inference",
                "progress": 80.0,
                "cpu": "Intel Core i5-10400",
                "gpu": "NVIDIA RTX 3060",
                "memory": "16GB DDR4",
                "hardware_info": '{"cores": 6, "threads": 12, "gpu_memory": "8GB", "storage": "500GB SSD"}',
                "network_latency": 30,
                "uptime": 92.1,
                "is_active": True,
                "user_id": admin_user.id,
                "project_id": main_project.id
            },
            {
                "name": "database_node_003_Edge_Processing",
                "node_type": "data",
                "role": "Processing Node",
                "state": "processing",
                "responsible_user": "System",
                "path_ipv4": "192.168.1.203",
                "connected_nodes_count": 1,
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "gpu_usage": 0.0,
                "priority": 2,
                "location": "Edge Location 3",
                "specialty": "Data Processing",
                "progress": 60.0,
                "cpu": "AMD Ryzen 7 3700X",
                "gpu": "NVIDIA GTX 1660",
                "memory": "16GB DDR4",
                "hardware_info": '{"cores": 8, "threads": 16, "gpu_memory": "6GB", "storage": "500GB SSD"}',
                "network_latency": 35,
                "uptime": 88.7,
                "is_active": True,
                "user_id": admin_user.id,
                "project_id": main_project.id
            },
            {
                "name": "database_node_004_Data_Processing",
                "node_type": "data",
                "role": "Data Processor",
                "state": "idle",
                "responsible_user": "System",
                "path_ipv4": "192.168.1.204",
                "connected_nodes_count": 1,
                "cpu_usage": 24.1,
                "memory_usage": 34.7,
                "gpu_usage": 0.0,
                "priority": 2,
                "location": "Edge Location 4",
                "specialty": "Data Analysis",
                "progress": 25.0,
                "cpu": "Intel Core i3-10100",
                "gpu": "None",
                "memory": "8GB DDR4",
                "hardware_info": '{"cores": 4, "threads": 8, "storage": "250GB SSD"}',
                "network_latency": 40,
                "uptime": 85.2,
                "is_active": True,
                "user_id": admin_user.id,
                "project_id": main_project.id
            },
            {
                "name": "database_node_005_Model_Validation",
                "node_type": "data",
                "role": "Validation Node",
                "state": "validation",
                "responsible_user": "System",
                "path_ipv4": "192.168.1.205",
                "connected_nodes_count": 1,
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "gpu_usage": 0.0,
                "priority": 2,
                "location": "Edge Location 5",
                "specialty": "Model Validation",
                "progress": 90.0,
                "cpu": "Intel Core i7-9700K",
                "gpu": "NVIDIA RTX 2070",
                "memory": "32GB DDR4",
                "hardware_info": '{"cores": 8, "threads": 8, "gpu_memory": "8GB", "storage": "1TB SSD"}',
                "network_latency": 22,
                "uptime": 91.8,
                "is_active": True,
                "user_id": admin_user.id,
                "project_id": main_project.id
            }
        ]
        
        created_nodes = []
        for node_data in nodes_data:
            node = Node(**node_data)
            db.add(node)
            db.flush()  # 获取ID
            created_nodes.append(node)
            print(f"  ✅ 创建节点: {node_data['name']} ({node_data['node_type']})")
        
        return created_nodes
    
    def _create_connections(self, db):
        """创建节点连接关系"""
        print("🔗 创建节点连接关系...")
        
        # 获取所有节点
        nodes = db.query(Node).all()
        model_nodes = [n for n in nodes if n.node_type == 'model']
        data_nodes = [n for n in nodes if n.node_type == 'data']
        control_nodes = [n for n in nodes if n.node_type == 'control']
        
        # 模型节点连接到所有数据节点
        for model_node in model_nodes:
            for data_node in data_nodes:
                connection = NodeConnection(
                    from_node_id=model_node.id,
                    to_node_id=data_node.id,
                    connection_type='data',
                    strength=1.0,
                    is_active=True
                )
                db.add(connection)
        
        # 控制节点连接到所有其他节点
        all_other_nodes = [n for n in nodes if n.node_type != 'control']
        for control_node in control_nodes:
            for other_node in all_other_nodes:
                connection = NodeConnection(
                    from_node_id=control_node.id,
                    to_node_id=other_node.id,
                    connection_type='control',
                    strength=0.8,
                    is_active=True
                )
                db.add(connection)
        
        print(f"  ✅ 创建了 {len(model_nodes) * len(data_nodes) + len(control_nodes) * len(all_other_nodes)} 个连接关系")
    
    def _create_metrics(self, db):
        """创建性能指标数据"""
        print("📊 创建性能指标数据...")
        
        nodes = db.query(Node).all()
        
        for node in nodes:
            # 为每个节点创建过去24小时的历史数据
            for hours_ago in range(24, 0, -1):
                timestamp = datetime.now() - timedelta(hours=hours_ago)
                
                # 模拟性能数据变化
                base_cpu = node.cpu_usage or 0
                base_memory = node.memory_usage or 0
                base_gpu = node.gpu_usage or 0
                
                # 添加一些随机变化
                cpu_variation = random.uniform(-10, 10)
                memory_variation = random.uniform(-5, 5)
                gpu_variation = random.uniform(-15, 15)
                
                metric = NodeMetric(
                    node_id=node.id,
                    timestamp=timestamp,
                    cpu_usage=max(0, min(100, base_cpu + cpu_variation)),
                    memory_usage=max(0, min(100, base_memory + memory_variation)),
                    gpu_usage=max(0, min(100, base_gpu + gpu_variation)),
                    network_usage=random.uniform(10, 50),
                    temperature=random.uniform(35, 75),
                    power_consumption=random.uniform(50, 200),
                    disk_usage=random.uniform(20, 80)
                )
                db.add(metric)
        
        print(f"  ✅ 为 {len(nodes)} 个节点创建了历史性能数据")
    
    def get_database_stats(self) -> Dict[str, Any]:
        """获取数据库统计信息"""
        db = self.get_session()
        
        try:
            stats = {
                "users": db.query(User).count(),
                "projects": db.query(Project).count(),
                "models": db.query(Model).count(),
                "nodes": db.query(Node).count(),
                "connections": db.query(NodeConnection).count(),
                "metrics": db.query(NodeMetric).count()
            }
            
            # 按类型统计节点
            stats["nodes_by_type"] = {
                "model": db.query(Node).filter(Node.node_type == 'model').count(),
                "control": db.query(Node).filter(Node.node_type == 'control').count(),
                "data": db.query(Node).filter(Node.node_type == 'data').count()
            }
            
            return stats
            
        finally:
            self.close_session()
    
    def test_database(self) -> bool:
        """测试数据库功能"""
        print("🧪 测试数据库功能...")
        
        try:
            # 测试连接
            db = self.get_session()
            
            # 测试查询
            user_count = db.query(User).count()
            project_count = db.query(Project).count()
            node_count = db.query(Node).count()
            
            print(f"  ✅ 数据库连接正常")
            print(f"  ✅ 用户数量: {user_count}")
            print(f"  ✅ 项目数量: {project_count}")
            print(f"  ✅ 节点数量: {node_count}")
            
            # 测试新字段
            project = db.query(Project).first()
            if project:
                new_fields = [
                    'training_alg', 'fed_alg', 'num_rounds', 'num_clients',
                    'sample_clients', 'max_steps', 'lr', 'dataset_sample',
                    'model_name_or_path', 'dataset_name'
                ]
                
                for field in new_fields:
                    value = getattr(project, field, None)
                    if value is not None:
                        print(f"  ✅ 字段 {field}: {value}")
                    else:
                        print(f"  ❌ 字段 {field} 不存在")
            
            self.close_session()
            return True
            
        except Exception as e:
            print(f"  ❌ 数据库测试失败: {e}")
            return False
    
    def reset_database(self):
        """重置数据库"""
        print("⚠️ 重置数据库...")
        self.init_database(reset=True)
    
    def cleanup_old_files(self):
        """清理旧的数据库文件"""
        print("🧹 清理旧的数据库文件...")
        
        old_files = [
            "init_db.py",
            "init_test_data.py", 
            "init_nodes_data.py",
            "seed_node_data.py",
            "test_new_fields.py",
            "migrate_enhanced_nodes.py",
            "migrate_add_training_fields.py"
        ]
        
        for filename in old_files:
            filepath = Path(__file__).parent / filename
            if filepath.exists():
                filepath.unlink()
                print(f"  ✅ 删除文件: {filename}")
        
        print("  ✅ 旧文件清理完成")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EdgeAI 统一数据库管理器")
    parser.add_argument("--init", action="store_true", help="初始化数据库")
    parser.add_argument("--reset", action="store_true", help="重置数据库")
    parser.add_argument("--test", action="store_true", help="测试数据库")
    parser.add_argument("--stats", action="store_true", help="显示数据库统计")
    parser.add_argument("--cleanup", action="store_true", help="清理旧文件")
    
    args = parser.parse_args()
    
    manager = EdgeAIDatabaseManager()
    
    try:
        if args.reset:
            manager.reset_database()
        elif args.init:
            manager.init_database()
        elif args.test:
            success = manager.test_database()
            sys.exit(0 if success else 1)
        elif args.stats:
            stats = manager.get_database_stats()
            print("\n📊 数据库统计信息:")
            print(f"  👥 用户数量: {stats['users']}")
            print(f"  📁 项目数量: {stats['projects']}")
            print(f"  🤖 模型数量: {stats['models']}")
            print(f"  🔧 节点数量: {stats['nodes']}")
            print(f"  🔗 连接关系: {stats['connections']}")
            print(f"  📊 性能指标: {stats['metrics']}")
            print(f"\n🔧 节点类型分布:")
            for node_type, count in stats['nodes_by_type'].items():
                print(f"  - {node_type}: {count}")
        elif args.cleanup:
            manager.cleanup_old_files()
        else:
            # 默认行为：初始化数据库
            manager.init_database()
            
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        sys.exit(1)
    finally:
        manager.close_session()


if __name__ == "__main__":
    main()
