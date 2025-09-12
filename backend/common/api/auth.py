from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from ..schemas.auth import LoginRequest, AuthResponse, UserResponse, UpdatePreferencesRequest
from ..schemas.common import BaseResponse

router = APIRouter()

# Mock user database (in production, use real database)
mock_users = {
    "admin": {
        "id": 1,
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

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """
    用户登录接口
    支持快速登录和完整登录
    """
    try:
        # 模拟用户验证
        if request.username in mock_users:
            user_data = mock_users[request.username]
            
            # 模拟生成token
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
        else:
            # 创建新用户（快速登录）
            new_user_id = len(mock_users) + 1
            new_user = {
                "id": new_user_id,
                "username": request.username,
                "email": request.email or f"{request.username}@example.com",
                "password": request.password or "default123",
                "user_type": "client",
                "preferences": {
                    "theme": "auto",
                    "auto_theme": True,
                    "language": "zh",
                    "notifications": True
                },
                "created_at": "2024-01-15T10:30:00Z",
                "last_login": "2024-01-15T10:30:00Z"
            }
            
            mock_users[request.username] = new_user
            
            token = f"mock_token_{new_user_id}_{request.module}"
            
            user_response = UserResponse(
                id=new_user["id"],
                username=new_user["username"],
                email=new_user["email"],
                module=request.module,
                user_type=new_user["user_type"],
                preferences=new_user["preferences"],
                created_at=new_user["created_at"],
                last_login=new_user["last_login"]
            )
            
            return AuthResponse(
                success=True,
                user=user_response,
                token=token
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
