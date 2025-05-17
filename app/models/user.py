from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """사용자 역할을 정의하는 열거형"""
    ADMIN = "admin"
    USER = "user"

class UserBase(BaseModel):
    """사용자 기본 모델"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    is_active: bool = True
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    """사용자 생성 모델"""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """사용자 수정 모델"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None
    password: Optional[str] = Field(None, min_length=8)

class UserInDB(UserBase):
    """데이터베이스에 저장되는 사용자 모델"""
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

class UserResponse(UserBase):
    """API 응답용 사용자 모델"""
    id: str
    created_at: datetime
    updated_at: datetime 