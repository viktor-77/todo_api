from app.core.config import settings
from app.core.security import get_password_hash, verify_password, \
    create_access_token
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserCreate


class AuthService:
    """
    Authentication and user management business logic.
    """

    @staticmethod
    async def register_user(data: UserCreate,
                            repo: UserRepository) -> UserModel:
        hashed = get_password_hash(data.password)
        user = UserModel(
            username=data.username, email=data.email, hashed_password=hashed
        )
        return await repo.create(user)

    @staticmethod
    async def authenticate_user(username: str, password: str,
                                repo: UserRepository) -> UserModel | None:
        user = await repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def mint_access_token(user_id: str) -> str:
        return create_access_token(
            subject=user_id,
            minutes=settings.access_token_expire_minutes,
            secret=settings.jwt_secret_key.get_secret_value(),
            algorithm=settings.jwt_algorithm,
        )
