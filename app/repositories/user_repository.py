from typing import Optional, Protocol, runtime_checkable

from app.models.user_model import UserModel

UserId = str


@runtime_checkable
class UserRepository(Protocol):
    """
    Repository contract for User entity.
    """

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        ...

    async def get_by_id(self, user_id: UserId) -> UserModel:
        ...

    async def create(self, user: UserModel) -> UserModel:
        ...
