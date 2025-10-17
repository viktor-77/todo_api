from datetime import datetime, UTC
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserModel(BaseModel):
    """
    Domain model for User (internal, includes hashed_password).
    """
    id: Optional[str] = Field(default=None, alias="_id")
    username: str
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)
