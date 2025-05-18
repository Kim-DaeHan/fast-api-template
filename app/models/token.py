from typing import Optional

from pydantic import BaseModel

from app.models.user import UserRole


class Token(BaseModel):
    """JWT 토큰 응답 모델"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """토큰에서 추출된 데이터 모델"""

    user_id: str
    email: Optional[str] = None
    role: UserRole
