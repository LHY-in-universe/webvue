#!/usr/bin/env python3
"""
简单的数据库初始化脚本
"""
import os
import sys

# 添加路径
sys.path.append('/home/webvue/database/edgeai')
sys.path.append('/home/webvue/backend')

try:
    from database.edgeai.database import engine, Base
    from database.edgeai.models import User, Project, Model, Node, Connection, Metric
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime
    import hashlib
    
    print("🔧 开始初始化数据库...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建完成")
    
    # 创建会话
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"📊 数据库已有 {existing_users} 个用户，跳过初始化")
            return
        
        # 创建测试用户
        def hash_password(password: str) -> str:
            return hashlib.sha256(password.encode()).hexdigest()
        
        admin_user = User(
            name="EdgeAI Demo",
            email="edgeai_demo@example.com",
            password=hash_password("demo123")
        )
        db.add(admin_user)
        db.flush()
        
        # 创建测试项目
        test_project = Project(
            name="Federated Learning Demo",
            description="Distributed machine learning with privacy preservation",
            training_alg="sft",
            fed_alg="fedavg",
            num_rounds=10,
            num_clients=2,
            sample_clients=2,
            max_steps=100,
            lr="1e-4",
            dataset_sample=50,
            model_name_or_path="sshleifer/tiny-gpt2",
            dataset_name="vicgalle/alpaca-gpt4",
            status="completed",
            progress=100.0,
            user_id=admin_user.id,
            created_time=datetime.now(),
            updated_time=datetime.now()
        )
        db.add(test_project)
        db.flush()
        
        # 创建测试节点
        test_node = Node(
            name="Control Center",
            node_type="control",
            status="online",
            ip_address="127.0.0.1",
            project_id=test_project.id,
            user_id=admin_user.id,
            created_time=datetime.now(),
            updated_time=datetime.now()
        )
        db.add(test_node)
        
        # 提交所有更改
        db.commit()
        print("✅ 测试数据创建完成")
        print(f"   - 用户: {admin_user.name} ({admin_user.email})")
        print(f"   - 项目: {test_project.name}")
        print(f"   - 节点: {test_node.name}")
        
    except Exception as e:
        print(f"❌ 创建数据时出错: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        
    print("🎉 数据库初始化完成！")
    
except Exception as e:
    print(f"❌ 数据库初始化失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


