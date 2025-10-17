from datetime import datetime, UTC
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(StrEnum):
    NEW = "new"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskModel(BaseModel):
    """
    Domain model for Task.
    """
    id: Optional[str] = Field(default=None, alias="_id")
    owner_id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.NEW
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)
