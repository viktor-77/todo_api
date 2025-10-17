from typing import Optional
from bson import ObjectId, errors as bson_errors
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError, DuplicateKeyError

from app.models.user_model import UserModel
from app.repositories.errors import RepositoryError, UniqueViolationError, \
    NotFoundError, InvalidIdError
from app.repositories.user_repository import UserRepository, UserId

COLLECTION_NAME = "users"


class UserRepositoryImpl(UserRepository):
    """
    MongoDB implementation of UserRepository.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.get_collection(COLLECTION_NAME)

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        try:
            doc = await self._collection.find_one({"username": username})
        except PyMongoError:
            raise RepositoryError()
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return UserModel.model_validate(doc)

    async def get_by_id(self, user_id: UserId) -> UserModel:
        try:
            oid = ObjectId(user_id)
        except bson_errors.InvalidId:
            raise InvalidIdError("invalid user id format")
        try:
            doc = await self._collection.find_one({"_id": oid})
        except PyMongoError:
            raise RepositoryError()
        if doc is None:
            raise NotFoundError("user not found")
        doc["_id"] = str(doc["_id"])
        return UserModel.model_validate(doc)

    async def create(self, user: UserModel) -> UserModel:
        payload = user.model_dump(by_alias=True, exclude={"id"})
        try:
            res = await self._collection.insert_one(payload)
        except DuplicateKeyError as e:
            raise UniqueViolationError(
                "username or email already exists"
            ) from e
        except PyMongoError as e:
            raise RepositoryError() from e
        return user.model_copy(update={"id": str(res.inserted_id)})
