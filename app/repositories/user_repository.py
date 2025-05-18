from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from app.database import db
from app.models.user import UserCreate, UserInDB, UserRole, UserUpdate
from app.security.password import hash_password


async def create_user(user: UserCreate) -> UserInDB:
    """새로운 사용자를 생성하는 함수"""
    now = datetime.utcnow()

    # ObjectId 생성
    user_id = str(ObjectId())

    # 사용자 데이터 생성
    user_data = {
        "_id": ObjectId(user_id),
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "role": user.role,
        "hashed_password": hash_password(user.password),
        "created_at": now,
        "updated_at": now,
    }

    # 데이터베이스에 저장
    await db.get_db()["users"].insert_one(user_data)

    # UserInDB 객체로 변환하여 반환
    return UserInDB(
        id=user_id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        role=user.role,
        hashed_password=user_data["hashed_password"],
        created_at=now,
        updated_at=now,
    )


async def get_user_by_email(email: str) -> Optional[UserInDB]:
    """이메일로 사용자를 조회하는 함수"""
    user_data = await db.get_db()["users"].find_one({"email": email})

    if user_data:
        return UserInDB(
            id=str(user_data["_id"]),
            username=user_data["username"],
            email=user_data["email"],
            is_active=user_data["is_active"],
            role=UserRole(user_data["role"]),
            hashed_password=user_data["hashed_password"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"],
        )

    return None


async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    """ID로 사용자를 조회하는 함수"""
    try:
        user_data = await db.get_db()["users"].find_one({"_id": ObjectId(user_id)})

        if user_data:
            return UserInDB(
                id=str(user_data["_id"]),
                username=user_data["username"],
                email=user_data["email"],
                is_active=user_data["is_active"],
                role=UserRole(user_data["role"]),
                hashed_password=user_data["hashed_password"],
                created_at=user_data["created_at"],
                updated_at=user_data["updated_at"],
            )

    except Exception:
        return None

    return None


async def get_users(skip: int = 0, limit: int = 100) -> List[UserInDB]:
    """모든 사용자를 조회하는 함수"""
    users = []
    cursor = db.get_db()["users"].find().skip(skip).limit(limit)

    async for user_data in cursor:
        users.append(
            UserInDB(
                id=str(user_data["_id"]),
                username=user_data["username"],
                email=user_data["email"],
                is_active=user_data["is_active"],
                role=UserRole(user_data["role"]),
                hashed_password=user_data["hashed_password"],
                created_at=user_data["created_at"],
                updated_at=user_data["updated_at"],
            )
        )

    return users


async def update_user(user_id: str, user_update: UserUpdate) -> Optional[UserInDB]:
    """사용자 정보를 업데이트하는 함수"""
    try:
        # 현재 사용자 데이터 가져오기
        current_user = await get_user_by_id(user_id)

        if not current_user:
            return None

        # 업데이트 데이터 준비
        update_data = {}

        if user_update.username is not None:
            update_data["username"] = user_update.username

        if user_update.email is not None:
            update_data["email"] = user_update.email

        if user_update.is_active is not None:
            update_data["is_active"] = user_update.is_active

        if user_update.role is not None:
            update_data["role"] = user_update.role

        if user_update.password is not None:
            update_data["hashed_password"] = hash_password(user_update.password)

        # 업데이트 시간 갱신
        update_data["updated_at"] = datetime.utcnow()

        # 데이터베이스 업데이트
        await db.get_db()["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )

        # 업데이트된 사용자 정보 반환
        return await get_user_by_id(user_id)

    except Exception:
        return None


async def delete_user(user_id: str) -> bool:
    """사용자를 삭제하는 함수"""
    try:
        result = await db.get_db()["users"].delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except Exception:
        return False
