from datetime import datetime
from pydantic import EmailStr, Field

from .base import RequestBaseModel, ResponseBaseModel


class UserCreate(RequestBaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserPublic(ResponseBaseModel):
    id: str = Field(alias="_id")
    username: str
    email: EmailStr
    created_at: datetime


class Token(ResponseBaseModel):
    access_token: str
    token_type: str = "bearer"
