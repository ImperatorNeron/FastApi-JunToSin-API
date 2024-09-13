import enum
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


class Complexity(enum.Enum):
    VERY_EASY = 'Effortless'
    EASY = 'Easy'
    MODERATE = 'Moderate'
    CHALLENGING = 'Challenging'
    DIFFICULT = 'Difficult'
    VERY_DIFFICULT = 'Complicated'


class Status(enum.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In progress'
    COMPLETED = 'Completed'


class Task(IdIntPkMixin, BaseModel):
    title: Mapped[str] = mapped_column("Title", String(255))
    description: Mapped[str] = mapped_column("Description")
    complexity: Mapped[Complexity] = mapped_column("Complexity", Enum(Complexity))
    status: Mapped[Status] = mapped_column("Status", Enum(Status), default=Status.OPEN)
    created_at: Mapped[datetime] = mapped_column("Created at", DateTime, default=datetime.now(timezone.utc))
    deadline: Mapped[datetime | None] = mapped_column("Deadline", DateTime, nullable=True)

    def __repr__(self):
        return f"<Task-{self.id}, title={self.title}, status={self.status}>"
