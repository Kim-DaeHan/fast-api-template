from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.token import Token
from app.models.user import UserCreate, UserResponse
from app.repositories.user_repository import create_user, get_user_by_email
from app.security.jwt import create_access_token
from app.security.password import verify_password
from config import settings

router = APIRouter(prefix="/auth", tags=["인증"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user: UserCreate):
    """새로운 사용자를 등록하는 엔드포인트"""
    # 이메일 중복 검사
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 등록된 이메일입니다"
        )

    # 사용자 생성
    new_user = await create_user(user)

    # UserResponse 형태로 변환하여 반환
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        is_active=new_user.is_active,
        role=new_user.role,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
    )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """사용자 로그인을 처리하는 엔드포인트 (이메일로 로그인)

    username 필드에 이메일 주소를 입력해주세요.
    """
    # 이메일로 사용자 조회 (username 필드에 이메일 입력)
    user = await get_user_by_email(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 이메일 또는 비밀번호입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 비밀번호 검증
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 이메일 또는 비밀번호입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 비활성화된 사용자 검사
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="비활성화된 사용자입니다"
        )

    # 액세스 토큰 생성
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token)
