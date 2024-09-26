from datetime import datetime
from typing import (
    Optional,
    TYPE_CHECKING,
)

from sqlalchemy import (
    DateTime,
    ForeignKey,
    func,
    Integer,
)
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)


if TYPE_CHECKING:
    from app.models.roled_users import User


class IdIntPkMixin:
    id: Mapped[int] = mapped_column(  # noqa
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )


class UpdateCreateDateTimeMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        onupdate=func.now(),
        default=func.now(),
        server_default=func.now(),
    )


class UserRelationMixin:
    _back_populates: Optional[str] = None

    @declared_attr
    def user_id(self) -> Mapped[int]:
        return mapped_column(
            ForeignKey("users.id"),
            primary_key=True,
        )

    @declared_attr
    def user(self) -> Mapped["User"]:
        return relationship(
            "User",
            back_populates=self._back_populates,
        )
