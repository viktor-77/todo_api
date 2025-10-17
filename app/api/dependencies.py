from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings
from app.core.database import get_database
from app.core.security import decode_token
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.repositories.user_repository_mongo import UserRepositoryImpl
from app.repositories.task_repository import TaskRepository
from app.repositories.task_repository_mongo import TaskRepositoryImpl
from app.repositories.errors import NotFoundError


def get_task_repository(
    db: AsyncIOMotorDatabase = Depends(get_database)) -> TaskRepository:
    return TaskRepositoryImpl(db)


def get_user_repository(
    db: AsyncIOMotorDatabase = Depends(get_database)) -> UserRepository:
    return UserRepositoryImpl(db)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: UserRepository = Depends(get_user_repository),
) -> UserModel:
    """
    Decode JWT and fetch the current user. Return 401 on any issue.
    """
    try:
        payload = decode_token(
            token=token,
            secret=settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
        )
        user_id = str(payload.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    try:
        return await repo.get_by_id(user_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
