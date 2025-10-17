from typing import List, Optional, Protocol, runtime_checkable, Literal, \
    TypedDict

from app.models.task_model import TaskModel, TaskStatus, TaskPriority

TaskId = str


class TaskListFilters(TypedDict, total=False):
    owner_id: str
    status: TaskStatus
    priority: TaskPriority


class TaskPatchData(TypedDict, total=False):
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority


@runtime_checkable
class TaskRepository(Protocol):
    """
    Repository contract for Task entity.
    """

    async def list(
        self,
        limit: int,
        skip: int,
        sort: Literal["created_at", "updated_at"],
        sort_dir: Literal["asc", "desc"],
        filters: Optional[TaskListFilters],
    ) -> List[TaskModel]:
        ...

    async def count(self, filters: Optional[TaskListFilters]) -> int:
        ...

    async def get(self, task_id: TaskId, owner_id: str) -> TaskModel:
        ...

    async def create(self, task: TaskModel) -> TaskModel:
        ...

    async def replace(self, task_id: TaskId, owner_id: str,
                      task: TaskModel) -> TaskModel:
        ...

    async def patch(self, task_id: TaskId, owner_id: str,
                    update_data: TaskPatchData) -> TaskModel:
        ...

    async def delete(self, task_id: TaskId, owner_id: str) -> None:
        ...
