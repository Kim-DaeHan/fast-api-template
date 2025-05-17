from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.token import TokenData
from app.repositories.user_repository import get_user_by_id
from config import settings
from app.models.user import UserRole

# OAuth2 스키마 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """액세스 토큰을 생성하는 함수"""
    to_encode = data.copy()
    
    # 만료 시간 설정
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    # JWT 토큰 생성
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """현재 인증된 사용자를 반환하는 함수"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 유효하지 않습니다",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 토큰 디코딩
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # 필요한 데이터 추출
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        role: str = payload.get("role")
        
        if user_id is None:
            raise credentials_exception
            
        token_data = TokenData(
            user_id=user_id, 
            username=username, 
            role=UserRole(role)
        )
        
    except JWTError:
        raise credentials_exception
        
    # 사용자 정보 조회
    user = await get_user_by_id(token_data.user_id)
    
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    """현재 활성화된 사용자를 반환하는 함수"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 사용자입니다"
        )
        
    return current_user

async def get_admin_user(current_user = Depends(get_current_active_user)):
    """관리자 권한이 있는 사용자를 반환하는 함수"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="해당 작업에 대한 권한이 없습니다"
        )
        
    return current_user 