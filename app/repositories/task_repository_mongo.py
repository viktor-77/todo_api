from datetime import datetime, UTC
from typing import Optional, List, Literal

from bson import ObjectId, errors as bson_errors
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING, ReturnDocument
from pymongo.errors import PyMongoError, DuplicateKeyError

from app.models.task_model import TaskModel
from app.repositories.errors import RepositoryError, UniqueViolationError, \
    NotFoundError, InvalidIdError
from app.repositories.task_repository import TaskRepository, TaskId, \
    TaskPatchData, TaskListFilters

COLLECTION_NAME = "tasks"


class TaskRepositoryImpl(TaskRepository):
    """
    MongoDB implementation of TaskRepository.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.get_collection(COLLECTION_NAME)

    async def create(self, task: TaskModel) -> TaskModel:
        payload = task.model_dump(by_alias=True, exclude={"id"})
        try:
            res = await self._collection.insert_one(payload)
        except DuplicateKeyError:
            # Likely title uniqueness per owner
            raise UniqueViolationError("title must be unique per owner")
        except PyMongoError:
            raise RepositoryError()
        return task.model_copy(update={"id": str(res.inserted_id)})

    async def get(self, task_id: TaskId, owner_id: str) -> TaskModel:
        oid = self._to_oid(task_id)
        try:
            doc = await self._collection.find_one(
                {"_id": oid, "owner_id": owner_id}
            )
        except PyMongoError:
            raise RepositoryError()
        if doc is None:
            raise NotFoundError("task not found")
        doc["_id"] = str(doc["_id"])
        return TaskModel.model_validate(doc)

    async def delete(self, task_id: TaskId, owner_id: str) -> None:
        oid = self._to_oid(task_id)
        try:
            res = await self._collection.delete_one(
                {"_id": oid, "owner_id": owner_id}
            )
        except PyMongoError:
            raise RepositoryError()
        if res.deleted_count == 0:
            raise NotFoundError("task not found")

    async def list(
        self,
        limit: int,
        skip: int,
        sort: Literal["created_at", "updated_at"],
        sort_dir: Literal["asc", "desc"],
        filters: Optional[TaskListFilters],
    ) -> List[TaskModel]:
        query: dict = {}
        if filters:
            if "owner_id" in filters:
                query["owner_id"] = filters["owner_id"]
            if "status" in filters:
                query["status"] = filters["status"]
            if "priority" in filters:
                query["priority"] = filters["priority"]

        sort_order = DESCENDING if sort_dir == "desc" else ASCENDING

        try:
            cursor = self._collection.find(query).sort(sort, sort_order).skip(
                skip
            ).limit(limit)
            items: List[TaskModel] = []
            async for doc in cursor:
                doc["_id"] = str(doc["_id"])
                items.append(TaskModel.model_validate(doc))
            return items
        except PyMongoError:
            raise RepositoryError()

    async def count(self, filters: Optional[TaskListFilters]) -> int:
        query: dict = {}
        if filters:
            if "owner_id" in filters:
                query["owner_id"] = filters["owner_id"]
            if "status" in filters:
                query["status"] = filters["status"]
            if "priority" in filters:
                query["priority"] = filters["priority"]
        try:
            return await self._collection.count_documents(query)
        except PyMongoError:
            raise RepositoryError()

    async def replace(self, task_id: TaskId, owner_id: str,
                      task: TaskModel) -> TaskModel:
        oid = self._to_oid(task_id)
        payload = task.model_dump(by_alias=True, exclude={"id"})
        try:
            doc = await self._collection.find_one_and_replace(
                {"_id": oid, "owner_id": owner_id},
                payload,
                return_document=ReturnDocument.AFTER,
            )
        except DuplicateKeyError:
            raise UniqueViolationError("title must be unique per owner")
        except PyMongoError:
            raise RepositoryError()
        if doc is None:
            raise NotFoundError("task not found")
        doc["_id"] = str(doc["_id"])
        return TaskModel.model_validate(doc)

    async def patch(self, task_id: TaskId, owner_id: str,
                    update_data: TaskPatchData) -> TaskModel:
        oid = self._to_oid(task_id)
        update_doc = {
            "$set": dict(update_data) | {"updated_at": datetime.now(UTC)}}
        try:
            doc = await self._collection.find_one_and_update(
                {"_id": oid, "owner_id": owner_id},
                update_doc,
                return_document=ReturnDocument.AFTER,
            )
        except DuplicateKeyError:
            raise UniqueViolationError("title must be unique per owner")
        except PyMongoError:
            raise RepositoryError()
        if doc is None:
            raise NotFoundError("task not found")
        doc["_id"] = str(doc["_id"])
        return TaskModel.model_validate(doc)

    @staticmethod
    def _to_oid(task_id: str) -> ObjectId:
        try:
            return ObjectId(task_id)
        except bson_errors.InvalidId:
            raise InvalidIdError()
