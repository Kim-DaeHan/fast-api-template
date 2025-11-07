# FastAPI를 이용한 사용자 관리 API

MongoDB를 데이터베이스로 사용하여 구현한 사용자 관리 API입니다.

## 주요 기능

- 사용자 모델(id, username, email, is_active 필드)
- 사용자 CRUD 기능
- JWT 토큰 기반 인증
- 보호된 엔드포인트
- 입력 데이터 검증
- 오류 처리
- 역할 기반 접근 제어(관리자/일반 사용자)

## 설치 및 실행

### 필수 요구사항

- Python 3.11 이상
- MongoDB
- [uv](https://docs.astral.sh/uv/) (Python 패키지 관리 도구)

### 설치 과정

1. 저장소 클론

```bash
git clone <repository-url>
cd fast-api-template
```

2. uv 설치 (설치되어 있지 않은 경우)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. 의존성 설치

```bash
uv sync
```

4. 환경 변수 설정

`.env.example` 파일을 참고하여 `.env` 파일을 생성하세요.

```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=user_management
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 실행

**개발 환경 (권장):**
```bash
uv run poe dev
```

**또는 직접 실행:**
```bash
# Python 모듈로 실행
uv run python -m app.main

# uvicorn CLI로 실행
uv run uvicorn app.main:app --reload
```

## API 문서

API 문서는 다음 URL에서 확인할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API 엔드포인트

### 인증

- `POST /api/auth/register` - 사용자 등록
- `POST /api/auth/login` - 사용자 로그인

### 사용자 관리

- `GET /api/users/me` - 현재 로그인한 사용자 정보 조회
- `GET /api/users` - 모든 사용자 목록 조회 (관리자 전용)
- `GET /api/users/{user_id}` - 특정 사용자 정보 조회
- `PUT /api/users/{user_id}` - 사용자 정보 업데이트
- `DELETE /api/users/{user_id}` - 사용자 삭제 (관리자 전용)
