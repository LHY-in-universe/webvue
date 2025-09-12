from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserType(str, Enum):
    CLIENT = "client"
    SERVER = "server"
    NODE = "node"
    ADMIN = "admin"

class ModuleType(str, Enum):
    P2PAI = "p2pai"
    EDGEAI = "edgeai"
    BLOCKCHAIN = "blockchain"
    CRYPTO = "crypto"

class LoginRequest(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    module: ModuleType

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    module: ModuleType
    user_type: UserType
    preferences: dict
    created_at: str
    last_login: str

class AuthResponse(BaseModel):
    success: bool
    user: Optional[UserResponse] = None
    token: Optional[str] = None
    error: Optional[str] = None

class UserPreferences(BaseModel):
    theme: str = "auto"
    auto_theme: bool = True
    language: str = "zh"
    notifications: bool = True

class UpdatePreferencesRequest(BaseModel):
    theme: Optional[str] = None
    auto_theme: Optional[bool] = None
    language: Optional[str] = None
    notifications: Optional[bool] = None
