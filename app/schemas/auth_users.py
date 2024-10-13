from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from app.utils.enums import UserRole


class BaseUserSchema(BaseModel):
    email: EmailStr
    username: str = Field(max_length=50)
    phone_number: Optional[str] = Field(max_length=12, default=None)
    role: UserRole = Field(default=UserRole.UNEMPLOYED)


class LoginUserSchema(BaseModel):
    username: str = Field(max_length=50)
    password: str


class RegisterUserSchema(BaseUserSchema):
    password: str


class CreateUserSchema(BaseUserSchema):
    hashed_password: bytes


class ReadUserSchema(BaseUserSchema):
    id: int  # noqa
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime


class ReadUserWithPasswordSchema(ReadUserSchema):
    hashed_password: bytes


class UpdateUserVerificationSchema(BaseModel):
    is_verified: bool
