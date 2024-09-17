from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    String,
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
from app.schemas.tasks import ReadTaskSchema
from app.utils.enums import (
    Complexity,
    Status,
)


class Task(
    IdIntPkMixin,
    UpdateCreateDateTimeMixin,
    BaseModel,
):
    title: Mapped[str] = mapped_column(
        "Title",
        String(255),
    )
    description: Mapped[str] = mapped_column("Description")
    complexity: Mapped[Complexity] = mapped_column(
        "Complexity",
        Enum(Complexity),
    )
    status: Mapped[Status] = mapped_column(
        "Status",
        Enum(Status),
        default=Status.OPEN,
    )
    deadline: Mapped[datetime | None] = mapped_column(
        "Deadline",
        DateTime,
        nullable=True,
    )
    employed_user_id: Mapped[int] = mapped_column(
        "Employed user",
        ForeignKey("employedusers.id"),
    )
    unemployed_user_id: Mapped[int] = mapped_column(
        "Unemployed user",
        ForeignKey("unemployedusers.id"),
        nullable=True,
    )
    employed_user = relationship("EmployedUser", back_populates="tasks")
    unemployed_user = relationship("UnemployedUser", back_populates="tasks")

    def to_read_model(self) -> ReadTaskSchema:
        return ReadTaskSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            complexity=self.complexity,
            status=self.status,
            created_at=self.created_at,
            deadline=self.deadline,
            updated_at=self.updated_at,
            employed_user_id=self.employed_user_id,
            unemployed_user_id=self.unemployed_user_id,
        )

    def __repr__(self):
        return f"<Task-{self.id}, title={self.title}, status={self.status}>"
