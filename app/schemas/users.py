from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class BaseUserSchema(BaseModel):
    username: str = Field(max_length=255)
    email: str = Field(max_length=255)
    hashed_password: str


class UserSchema(BaseUserSchema):
    phone_number: Optional[str] = Field(max_length=12, default=None)
    description: Optional[str] = Field(default=None)


class ReadEmployedUserSchema(UserSchema):
    id: int  # noqa
    created_at: datetime
    updated_at: datetime


class ReadEmployedUserListSchema(BaseModel):
    users: list[ReadEmployedUserSchema]


class CreateEmployedUserSchema(UserSchema):
    pass
