from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from sqlalchemy.orm import Session
import bcrypt
import hashlib
from ..schemas.auth import LoginRequest, RegisterRequest, AuthResponse, UserResponse, UpdatePreferencesRequest
from ..schemas.common import BaseResponse

# Import EdgeAI database components
import sys
import os
from pathlib import Path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.append(str(root_dir))

from database.edgeai.database import SessionLocal, get_db
from database.edgeai.models import User

router = APIRouter()

# Authentication dependency
async def get_current_user_id(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> int:
    """
    从Authorization header中获取当前用户ID
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    try:
        # 解析Bearer token
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization format")
        
        token = authorization.replace("Bearer ", "")
        
        # 解析token格式: edgeai_token_{user_id}_{module} 或 mock_token_{user_id}_{module}
        if token.startswith("edgeai_token_"):
            # 从数据库token中提取用户ID
            parts = token.split("_")
            if len(parts) >= 3:
                user_id = int(parts[2])
                # 验证用户是否存在
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    return user_id
                else:
                    raise HTTPException(status_code=401, detail="User not found")
            else:
                raise HTTPException(status_code=401, detail="Invalid token format")
        
        elif token.startswith("mock_token_"):
            # 从mock token中提取用户ID
            parts = token.split("_")
            if len(parts) >= 3:
                user_id = int(parts[2])
                # 验证mock用户是否存在
                if user_id in [user_data["id"] for user_data in mock_users.values()]:
                    return user_id
                else:
                    raise HTTPException(status_code=401, detail="Mock user not found")
            else:
                raise HTTPException(status_code=401, detail="Invalid mock token format")
        
        else:
            raise HTTPException(status_code=401, detail="Invalid token type")
    
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID in token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

# Password hashing using bcrypt directly
def hash_password(password: str) -> str:
    """
    使用 bcrypt 直接哈希密码
    """
    # 将密码编码为字节
    password_bytes = password.encode('utf-8')
    # 生成盐并哈希密码
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否匹配
    """
    try:
        # 将密码编码为字节
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        # 使用 bcrypt 验证密码
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

# Mock fallback users (for demo purposes)
mock_users = {
    "admin": {
        "id": 999,
        "username": "admin",
        "email": "admin@opentmp.com",
        "password": "admin123",
        "user_type": "admin",
        "preferences": {
            "theme": "auto",
            "auto_theme": True,
            "language": "zh",
            "notifications": True
        },
        "created_at": "2024-01-01T00:00:00Z",
        "last_login": "2024-01-15T10:30:00Z"
    }
}

@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    用户注册接口
    """
    try:
        # 验证密码匹配
        request.validate_passwords_match()

        # 检查邮箱是否已存在
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            return AuthResponse(
                success=False,
                error="邮箱已被注册"
            )

        # 生成用户名（如果没有提供）
        username = request.username or request.email.split('@')[0]

        # 创建新用户
        hashed_password = hash_password(request.password)
        new_user = User(
            name=request.name,
            email=request.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 生成token
        token = f"edgeai_token_{new_user.id}_{request.module}"

        # 构建用户响应
        user_response = UserResponse(
            id=new_user.id,
            username=username,
            email=new_user.email,
            module=request.module,
            user_type="client",
            preferences={
                "theme": "auto",
                "auto_theme": True,
                "language": "zh",
                "notifications": True
            },
            created_at=new_user.created_time.isoformat() if new_user.created_time else "",
            last_login=new_user.created_time.isoformat() if new_user.created_time else ""
        )

        return AuthResponse(
            success=True,
            user=user_response,
            token=token
        )

    except ValueError as e:
        return AuthResponse(
            success=False,
            error=str(e)
        )
    except Exception as e:
        db.rollback()
        return AuthResponse(
            success=False,
            error=f"注册失败: {str(e)}"
        )

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录接口
    支持用户名或邮箱登录
    """
    try:
        # 首先尝试从EdgeAI数据库查找用户
        user = None

        # 尝试通过邮箱查找
        if request.email:
            user = db.query(User).filter(User.email == request.email).first()

        # 如果没有找到，尝试通过用户名匹配邮箱
        if not user and request.username:
            # 检查用户名是否是邮箱格式
            if '@' in request.username:
                user = db.query(User).filter(User.email == request.username).first()
            else:
                # 尝试匹配名字
                user = db.query(User).filter(User.name == request.username).first()

        if user and request.password:
            # 验证密码
            if verify_password(request.password, user.password):
                token = f"edgeai_token_{user.id}_{request.module}"

                user_response = UserResponse(
                    id=user.id,
                    username=user.name,
                    email=user.email,
                    module=request.module,
                    user_type="client",
                    preferences={
                        "theme": "auto",
                        "auto_theme": True,
                        "language": "zh",
                        "notifications": True
                    },
                    created_at=user.created_time.isoformat() if user.created_time else "",
                    last_login=user.updated_time.isoformat() if user.updated_time else ""
                )

                return AuthResponse(
                    success=True,
                    user=user_response,
                    token=token
                )

        # 如果数据库中没有找到，回退到mock用户（为了兼容性）
        if request.username in mock_users:
            user_data = mock_users[request.username]
            token = f"mock_token_{user_data['id']}_{request.module}"

            user_response = UserResponse(
                id=user_data["id"],
                username=user_data["username"],
                email=user_data["email"],
                module=request.module,
                user_type=user_data["user_type"],
                preferences=user_data["preferences"],
                created_at=user_data["created_at"],
                last_login=user_data["last_login"]
            )

            return AuthResponse(
                success=True,
                user=user_response,
                token=token
            )

        # 登录失败
        return AuthResponse(
            success=False,
            error="用户名/邮箱或密码错误"
        )

    except Exception as e:
        return AuthResponse(
            success=False,
            error=str(e)
        )

@router.post("/logout", response_model=BaseResponse)
async def logout():
    """
    用户登出接口
    """
    return BaseResponse(
        success=True,
        message="Logout successful"
    )

@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """
    获取用户信息
    """
    for user in mock_users.values():
        if user["id"] == user_id:
            return UserResponse(**user)
    
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/user/{user_id}/preferences", response_model=BaseResponse)
async def update_user_preferences(
    user_id: int, 
    preferences: UpdatePreferencesRequest
):
    """
    更新用户偏好设置
    """
    for username, user in mock_users.items():
        if user["id"] == user_id:
            # 更新偏好设置
            if preferences.theme is not None:
                user["preferences"]["theme"] = preferences.theme
            if preferences.auto_theme is not None:
                user["preferences"]["auto_theme"] = preferences.auto_theme
            if preferences.language is not None:
                user["preferences"]["language"] = preferences.language
            if preferences.notifications is not None:
                user["preferences"]["notifications"] = preferences.notifications
            
            return BaseResponse(
                success=True,
                message="Preferences updated successfully"
            )
    
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/user/{user_id}/preferences")
async def get_user_preferences(user_id: int):
    """
    获取用户偏好设置
    """
    for user in mock_users.values():
        if user["id"] == user_id:
            return user["preferences"]
    
    raise HTTPException(status_code=404, detail="User not found")

# Export the authentication dependency for use in other modules
__all__ = ["router", "get_current_user_id"]
