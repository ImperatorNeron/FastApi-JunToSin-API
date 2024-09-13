from datetime import (
    datetime,
    timezone,
)

from sqlalchemy import (
    DateTime,
    Enum,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import BaseModel
from app.models.mixins import IdIntPkMixin
from app.schemas.tasks import ReadTaskSchema
from app.utils.enums import (
    Complexity,
    Status,
)


class Task(IdIntPkMixin, BaseModel):
    title: Mapped[str] = mapped_column("Title", String(255))
    description: Mapped[str] = mapped_column("Description")
    complexity: Mapped[Complexity] = mapped_column("Complexity", Enum(Complexity))
    status: Mapped[Status] = mapped_column("Status", Enum(Status), default=Status.OPEN)
    created_at: Mapped[datetime] = mapped_column("Created at", DateTime, default=datetime.now(timezone.utc))
    deadline: Mapped[datetime | None] = mapped_column("Deadline", DateTime, nullable=True)

    def to_read_model(self) -> ReadTaskSchema:
        return ReadTaskSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            complexity=self.complexity,
            status=self.status,
            created_at=self.created_at,
            deadline=self.deadline,
        )

    def __repr__(self):
        return f"<Task-{self.id}, title={self.title}, status={self.status}>"
