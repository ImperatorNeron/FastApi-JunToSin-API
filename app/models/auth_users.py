from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum,
    LargeBinary,
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
from app.schemas.auth_users import ReadUserWithPasswordSchema
from app.utils.enums import UserRole


if TYPE_CHECKING:
    from app.models.roled_users import (
        AdminUser,
        EmployedUser,
        UnemployedUser,
    )


class User(
    IdIntPkMixin,
    UpdateCreateDateTimeMixin,
    BaseModel,
):

    email: Mapped[str] = mapped_column(
        String(length=320),
        unique=True,
        index=True,
    )
    hashed_password: Mapped[bytes] = mapped_column(
        LargeBinary,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )
    phone_number: Mapped[str] = mapped_column(
        String(12),
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

    def to_read_model(self) -> ReadUserWithPasswordSchema:
        return ReadUserWithPasswordSchema(
            id=self.id,
            email=self.email,
            username=self.username,
            phone_number=self.phone_number,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            is_verified=self.is_verified,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.updated_at,
            hashed_password=self.hashed_password,
        )

    def __repr__(self):
        return f"<User-{self.id}, username={self.username}, role={self.role}>"
