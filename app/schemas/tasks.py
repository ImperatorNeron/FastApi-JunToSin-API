from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)

from app.utils.enums import (
    Complexity,
    Status,
)


class BaseTaskSchema(BaseModel):
    title: str = Field(max_length=255)
    description: str
    complexity: Complexity
    status: Status = Status.OPEN
    deadline: Optional[datetime] = Field(None, examples=["2024-08-04T15:02:36.351052"])


class ReadTaskSchema(BaseTaskSchema):
    id: int = Field(ge=0)  # noqa
    created_at: datetime


class ReadListTaskSchema(BaseModel):
    tasks: list[ReadTaskSchema]


class CreateTaskSchema(BaseTaskSchema):
    pass


class UpdateTaskSchema(BaseTaskSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    complexity: Optional[Complexity] = None
    status: Optional[Status] = None
    deadline: Optional[datetime] = None
