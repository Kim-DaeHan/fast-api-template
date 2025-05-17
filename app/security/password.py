from passlib.context import CryptContext

# 비밀번호 해싱 컨텍스트 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """비밀번호를 해싱하는 함수"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호를 검증하는 함수"""
    return pwd_context.verify(plain_password, hashed_password) 