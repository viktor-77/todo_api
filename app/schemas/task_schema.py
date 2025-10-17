from datetime import datetime
from enum import StrEnum
from typing import Optional, List, Literal

from pydantic import Field, ConfigDict, model_validator

from app.models.task_model import TaskStatus, TaskPriority
from .base import RequestBaseModel, ResponseBaseModel


class TaskBase(RequestBaseModel):
    title: str = Field(min_length=5, max_length=100, description="Task title")
    description: Optional[str] = Field(
        default=None, min_length=10, max_length=1000,
        description="Detailed task description"
    )
    status: TaskStatus = TaskStatus.NEW
    priority: TaskPriority = TaskPriority.MEDIUM


# --- Requests ---
class TaskCreate(TaskBase):
    pass


class TaskPutUpdate(TaskBase):
    pass


class TaskPatchUpdate(RequestBaseModel):
    title: Optional[str] = Field(default=None, min_length=5, max_length=100)
    description: Optional[str] = Field(
        default=None, min_length=10, max_length=1000
    )
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        if any(
            v is not None for v in
            (self.title, self.description, self.status, self.priority)
        ):
            return self
        raise ValueError("At least one field must be provided")


# --- Responses ---
class TaskResponse(ResponseBaseModel):
    id: str = Field(alias="_id")
    owner_id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime] = None


class PageMeta(ResponseBaseModel):
    total: int
    limit: int
    skip: int
    sort: Literal["created_at", "updated_at"]
    sort_dir: Literal["asc", "desc"]


class TaskList(ResponseBaseModel):
    items: List[TaskResponse]
    meta: PageMeta


# --- Query params ---
class TaskQueryParams(RequestBaseModel):
    limit: int = Field(
        50, ge=1, le=100, description="Max number of tasks to return"
    )
    skip: int = Field(
        0, ge=0, description="Number of tasks to skip from the beginning"
    )
    sort: Literal["created_at", "updated_at"] = Field(
        default="created_at", description="Sort field"
    )
    sort_dir: Literal["asc", "desc"] = Field(
        default="desc", description="Sort direction"
    )
    status: Optional[TaskStatus] = Field(
        default=None, description="Filter by status"
    )
    priority: Optional[TaskPriority] = Field(
        default=None, description="Filter by priority"
    )

    model_config = ConfigDict(str_strip_whitespace=True)
