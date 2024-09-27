from typing import (
    List,
    TYPE_CHECKING,
)

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
from app.models.mixins import UserRelationMixin
from app.schemas.roled_users import (
    ReadEmployedUserSchema,
    ReadUnemployedUserSchema,
)


if TYPE_CHECKING:
    from app.models.tasks import Task


class EmployedUser(BaseModel, UserRelationMixin):

    _back_populates = "employed_user"

    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="employed_user",
    )

    def to_read_model(self) -> ReadEmployedUserSchema:
        return ReadEmployedUserSchema(
            user_id=self.user_id,
            description=self.description,
        )


class UnemployedUser(BaseModel, UserRelationMixin):

    _back_populates = "unemployed_user"

    linkedin_url: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    achivements: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="unemployed_user",
    )

    def to_read_model(self) -> ReadUnemployedUserSchema:
        return ReadUnemployedUserSchema(
            user_id=self.user_id,
            linkedin_url=self.linkedin_url,
            achivements=self.achivements,
        )


class AdminUser(BaseModel, UserRelationMixin):

    _back_populates = "admin_user"
