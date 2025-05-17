import os
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

# 환경 변수 로드
load_dotenv()

class Settings(BaseModel):
    """애플리케이션 설정을 관리하는 클래스"""
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "fastapi")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 전역 설정 인스턴스
settings = Settings() 