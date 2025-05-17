from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import UserResponse, UserUpdate
from app.repositories.user_repository import get_users, get_user_by_id, update_user, delete_user
from app.security.jwt import get_current_active_user, get_admin_user

router = APIRouter(prefix="/users", tags=["사용자"])

@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user = Depends(get_current_active_user)):
    """현재 로그인한 사용자 정보를 조회하는 엔드포인트"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.get("", response_model=List[UserResponse])
async def read_users(
    skip: int = 0, 
    limit: int = 100,
    current_user = Depends(get_admin_user)
):
    """모든 사용자 목록을 조회하는 엔드포인트 (관리자 전용)"""
    users = await get_users(skip, limit)
    
    # UserResponse 형태로 변환하여 반환
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        for user in users
    ]

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: str,
    current_user = Depends(get_current_active_user)
):
    """특정 사용자 정보를 조회하는 엔드포인트"""
    # 관리자가 아니고, 자신의 정보가 아닌 경우 접근 제한
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="해당 작업에 대한 권한이 없습니다"
        )
        
    user = await get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
        
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_info(
    user_id: str,
    user_update: UserUpdate,
    current_user = Depends(get_current_active_user)
):
    """사용자 정보를 업데이트하는 엔드포인트"""
    # 관리자가 아니고, 자신의 정보가 아닌 경우 접근 제한
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="해당 작업에 대한 권한이 없습니다"
        )
    
    # 관리자가 아닌 경우, 역할 변경 제한
    if current_user.role != "admin" and user_update.role is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="역할 변경은 관리자만 가능합니다"
        )
    
    updated_user = await update_user(user_id, user_update)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
        
    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        is_active=updated_user.is_active,
        role=updated_user.role,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_info(
    user_id: str,
    current_user = Depends(get_admin_user)
):
    """사용자를 삭제하는 엔드포인트 (관리자 전용)"""
    # 관리자 본인 삭제 방지
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자신의 계정은 삭제할 수 없습니다"
        )
        
    deleted = await delete_user(user_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        ) 