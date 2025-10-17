from datetime import datetime, UTC
from typing import Tuple, List

from app.models.task_model import TaskModel
from app.repositories.task_repository import TaskRepository, TaskId, \
    TaskPatchData, TaskListFilters
from app.schemas.task_schema import TaskCreate, TaskPutUpdate, TaskQueryParams


class TaskService:
    """
    Task business logic.
    """

    @staticmethod
    async def create_task(owner_id: str, task_data: TaskCreate,
                          repository: TaskRepository) -> TaskModel:
        task = TaskModel(owner_id=owner_id, **task_data.model_dump())
        return await repository.create(task)

    @staticmethod
    async def get_task(task_id: TaskId, owner_id: str,
                       repository: TaskRepository) -> TaskModel:
        return await repository.get(task_id, owner_id)

    @staticmethod
    async def delete_task(task_id: TaskId, owner_id: str,
                          repository: TaskRepository) -> None:
        return await repository.delete(task_id, owner_id)

    @staticmethod
    async def list_tasks(owner_id: str, params: TaskQueryParams,
                         repository: TaskRepository) -> Tuple[
        List[TaskModel], int]:
        filters: TaskListFilters = {"owner_id": owner_id}
        if params.status is not None:
            filters["status"] = params.status
        if params.priority is not None:
            filters["priority"] = params.priority

        items = await repository.list(
            limit=params.limit,
            skip=params.skip,
            sort=params.sort,
            sort_dir=params.sort_dir,
            filters=filters,
        )
        total = await repository.count(filters=filters)
        return items, total

    @staticmethod
    async def replace_task(task_id: TaskId, owner_id: str, data: TaskPutUpdate,
                           repository: TaskRepository) -> TaskModel:
        existing = await repository.get(task_id, owner_id)
        new_model = TaskModel(
            id=existing.id,
            owner_id=owner_id,
            title=data.title,
            description=data.description,
            status=data.status,
            priority=data.priority,
            created_at=existing.created_at,
            updated_at=datetime.now(UTC),
        )
        return await repository.replace(task_id, owner_id, new_model)

    @staticmethod
    async def patch_task(task_id: TaskId, owner_id: str, data: TaskPatchData,
                         repository: TaskRepository) -> TaskModel:
        return await repository.patch(task_id, owner_id, data)
