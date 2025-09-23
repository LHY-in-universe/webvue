#!/usr/bin/env python3
"""
测试项目删除功能
验证数据库删除是否正常工作
"""

import sys
import os
import requests
import json

# 添加数据库路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'database', 'edgeai'))

def test_project_deletion():
    """测试项目删除功能"""
    
    base_url = "http://localhost:8000/api/edgeai/projects/"
    
    print("🧪 开始测试项目删除功能...")
    
    # 1. 首先获取现有项目列表
    print("\n1️⃣ 获取现有项目列表...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ 成功获取项目列表，共 {len(projects)} 个项目")
            for project in projects:
                print(f"   - ID: {project['id']}, 名称: {project['name']}")
        else:
            print(f"❌ 获取项目列表失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return
    
    if not projects:
        print("⚠️ 没有找到项目，无法测试删除功能")
        return
    
    # 2. 选择第一个项目进行删除测试
    test_project = projects[0]
    project_id = test_project['id']
    project_name = test_project['name']
    
    print(f"\n2️⃣ 准备删除项目: {project_name} (ID: {project_id})")
    
    # 3. 执行删除操作
    print("\n3️⃣ 执行删除操作...")
    try:
        delete_url = f"{base_url}{project_id}"
        response = requests.delete(delete_url)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 删除成功: {result.get('message', 'Project deleted successfully')}")
        else:
            print(f"❌ 删除失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return
    except Exception as e:
        print(f"❌ 删除请求失败: {e}")
        return
    
    # 4. 验证删除结果
    print("\n4️⃣ 验证删除结果...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            updated_projects = response.json()
            print(f"✅ 删除后项目数量: {len(updated_projects)}")
            
            # 检查被删除的项目是否还在列表中
            deleted_project_exists = any(p['id'] == project_id for p in updated_projects)
            if deleted_project_exists:
                print(f"❌ 项目 {project_name} 仍然存在于列表中！")
            else:
                print(f"✅ 项目 {project_name} 已成功从列表中移除")
                
            # 显示剩余项目
            if updated_projects:
                print("\n剩余项目:")
                for project in updated_projects:
                    print(f"   - ID: {project['id']}, 名称: {project['name']}")
            else:
                print("📝 没有剩余项目")
        else:
            print(f"❌ 验证失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 验证请求失败: {e}")
    
    print("\n🎉 项目删除功能测试完成！")

def test_database_consistency():
    """测试数据库一致性"""
    print("\n🔍 检查数据库一致性...")
    
    try:
        # 导入数据库模块
        from database import get_db
        from models import Project, User
        
        # 获取数据库会话
        db = next(get_db())
        
        # 查询所有项目
        projects = db.query(Project).all()
        print(f"📊 数据库中的项目数量: {len(projects)}")
        
        # 显示项目详情
        for project in projects:
            print(f"   - ID: {project.id}, 名称: {project.name}, 用户ID: {project.user_id}")
        
        # 查询用户
        users = db.query(User).all()
        print(f"👥 数据库中的用户数量: {len(users)}")
        
        for user in users:
            print(f"   - ID: {user.id}, 名称: {user.name}, 邮箱: {user.email}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")

if __name__ == "__main__":
    print("🚀 EdgeAI 项目删除功能测试")
    print("=" * 50)
    
    # 检查数据库一致性
    test_database_consistency()
    
    # 测试删除功能
    test_project_deletion()
    
    print("\n" + "=" * 50)
    print("✨ 测试完成！")
