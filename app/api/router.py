from fastapi import APIRouter

from app.api.endpoints import auth, users

# API 라우터 생성
api_router = APIRouter(prefix="/api")

# 엔드포인트 라우터 등록
api_router.include_router(auth.router)
api_router.include_router(users.router) 