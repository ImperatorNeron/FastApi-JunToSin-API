from sqlalchemy import (
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import BaseModel
from app.models.mixins import (
    IdIntPkMixin,
    UpdateCreateDateTimeMixin,
)


class BaseUser(
    IdIntPkMixin,
    UpdateCreateDateTimeMixin,
    BaseModel,
):

    __abstract__ = True

    username: Mapped[str] = mapped_column(
        "Username",
        String(255),
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        "Email",
        String(255),
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        "Hashed password",
        Text,
    )


class User(BaseUser):

    __abstract__ = True

    phone_number: Mapped[str] = mapped_column(
        "Phone number",
        String(12),
        nullable=True,
    )
    description: Mapped[str] = mapped_column(
        "Description",
        Text,
        nullable=True,
    )


class AdminUser(BaseUser):
    pass


class UnemployedUser(User):
    linkedin_url: Mapped[str] = mapped_column(
        "LinkedIn",
        String,
        nullable=True,
    )
    achivements: Mapped[str] = mapped_column(
        "Achivements",
        Text,
        nullable=True,
    )
    tasks = relationship(
        "Task",
        back_populates="unemployed_user",
    )


class EmployedUser(User):
    tasks = relationship(
        "Task",
        back_populates="employed_user",
    )
