import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.database import db

# FastAPI 앱 생성
app = FastAPI(
    title="사용자 관리 API",
    description="FastAPI와 MongoDB를 사용한 사용자 관리 API",
    version="0.1.0",
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 환경에서는 실제 도메인으로 제한해야 함
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router)


@app.on_event("startup")
async def startup_db_client():
    """앱 시작 시 데이터베이스 연결"""
    await db.connect_db()


@app.on_event("shutdown")
async def shutdown_db_client():
    """앱 종료 시 데이터베이스 연결 종료"""
    await db.close_db()


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "사용자 관리 API에 오신 것을 환영합니다",
        "documentation": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
