from datetime import datetime

from sqlalchemy import (
    DateTime,
    func,
    Integer,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class IdIntPkMixin:
    id: Mapped[int] = mapped_column(  # noqa
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )


class UpdateCreateDateTimeMixin:
    created_at: Mapped[datetime] = mapped_column(
        "Created at",
        DateTime,
        default=func.now(),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        "Updated at",
        DateTime,
        onupdate=func.now(),
        default=func.now(),
        server_default=func.now(),
    )
