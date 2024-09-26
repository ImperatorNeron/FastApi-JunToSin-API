from typing import Optional

from fastapi_users import schemas
from pydantic import (
    BaseModel,
    Field,
)

from app.utils.enums import UserRole


class BaseUserSchema(BaseModel):
    username: str = Field(max_length=50)
    phone_number: Optional[str] = Field(max_length=12, default=None)
    role: UserRole = Field(default=UserRole.UNEMPLOYED)


class UserRead(schemas.BaseUser[int], BaseUserSchema):
    pass


class UserCreate(schemas.BaseUserCreate, BaseUserSchema):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    phone_number: Optional[str] = None
