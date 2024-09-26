from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import (
    Enum,
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
from app.utils.enums import UserRole


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.models.roled_users import (
        AdminUser,
        EmployedUser,
        UnemployedUser,
    )
    from app.models.tokens import AccessToken


class User(
    SQLAlchemyBaseUserTable[int],
    IdIntPkMixin,
    UpdateCreateDateTimeMixin,
    BaseModel,
):

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )
    phone_number: Mapped[str] = mapped_column(
        String(12),
        nullable=True,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.UNEMPLOYED,
    )

    admin_user: Mapped["AdminUser"] = relationship(
        "AdminUser",
        back_populates="user",
    )
    unemployed_user: Mapped["UnemployedUser"] = relationship(
        "UnemployedUser",
        back_populates="user",
    )

    employed_user: Mapped["EmployedUser"] = relationship(
        "EmployedUser",
        back_populates="user",
    )

    access_token: Mapped["AccessToken"] = relationship(
        "AccessToken",
        back_populates="user",
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
