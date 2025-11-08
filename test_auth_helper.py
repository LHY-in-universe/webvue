#!/usr/bin/env python3
"""
测试认证辅助工具
提供注册、登录、登出等认证功能
"""
import requests
import time
import sys
import os

class TestAuthHelper:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.auth_token = None
        self.user_id = None
        self.user_email = None
        
    def register_user(self, email: str = None, password: str = "test123456") -> bool:
        """注册新用户"""
        if not email:
            import time
            timestamp = int(time.time() * 1000000)  # Use microseconds for better uniqueness
            email = f"testuser{timestamp}@example.com"
        
        register_data = {
            "name": "测试用户",
            "email": email,
            "password": password,
            "confirm_password": password,
            "module": "edgeai"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/common/auth/register", json=register_data)
            if response.status_code == 200:
                auth_data = response.json()
                if auth_data.get("success"):
                    self.auth_token = auth_data.get("token")
                    self.user_id = auth_data.get("user", {}).get("id")
                    self.user_email = email
                    print(f"✅ 用户注册成功: {email}")
                    print(f"   Token: {self.auth_token[:20]}...")
                    print(f"   User ID: {self.user_id}")
                    return True
                else:
                    print(f"❌ 用户注册失败: {auth_data.get('error')}")
                    return False
            else:
                print(f"❌ 注册请求失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 注册请求异常: {e}")
            return False
    
    def login_user(self, email: str = None, password: str = "test123456") -> bool:
        """登录用户"""
        if not email:
            # 尝试使用已注册的用户邮箱
            if self.user_email:
                email = self.user_email
            else:
                print("❌ 没有可用的用户邮箱进行登录")
                return False
        
        login_data = {
            "username": email,
            "password": password,
            "module": "edgeai"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/common/auth/login", json=login_data)
            if response.status_code == 200:
                auth_data = response.json()
                if auth_data.get("success"):
                    self.auth_token = auth_data.get("token")
                    self.user_id = auth_data.get("user", {}).get("id")
                    self.user_email = email
                    print(f"✅ 用户登录成功: {email}")
                    print(f"   Token: {self.auth_token[:20]}...")
                    print(f"   User ID: {self.user_id}")
                    return True
                else:
                    print(f"❌ 用户登录失败: {auth_data.get('error')}")
                    return False
            else:
                print(f"❌ 登录请求失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 登录请求异常: {e}")
            return False
    
    def logout_user(self) -> bool:
        """登出用户"""
        if not self.auth_token:
            print("⚠️  没有活跃的认证token，无需登出")
            return True
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.post(f"{self.base_url}/api/common/auth/logout", headers=headers)
            if response.status_code == 200:
                logout_data = response.json()
                if logout_data.get("success"):
                    print(f"✅ 用户登出成功")
                    self.auth_token = None
                    self.user_id = None
                    return True
                else:
                    print(f"❌ 用户登出失败: {logout_data.get('error')}")
                    return False
            else:
                print(f"❌ 登出请求失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 登出请求异常: {e}")
            return False
    
    def get_headers(self):
        """获取带认证的请求头"""
        if self.auth_token:
            return {"Authorization": f"Bearer {self.auth_token}", "Content-Type": "application/json"}
        return {"Content-Type": "application/json"}
    
    def is_authenticated(self) -> bool:
        """检查是否已认证"""
        return self.auth_token is not None
    
    def setup_auth(self, use_existing_user: bool = False) -> bool:
        """设置认证（注册新用户或登录现有用户）"""
        if use_existing_user:
            # 尝试登录现有用户
            return self.login_user()
        else:
            # 注册新用户
            return self.register_user()
    
    def cleanup_auth(self) -> bool:
        """清理认证（登出）"""
        return self.logout_user()
