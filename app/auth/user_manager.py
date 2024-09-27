from typing import TYPE_CHECKING

from fastapi import Depends

from fastapi_users import BaseUserManager

from app.schemas.auth_users import UserCreate
from app.services.roled_users import (
    EmployedUserService,
    UnemployedUserService,
)
from app.settings.settings import settings
from app.utils.unitofwork import (
    IUnitOfWork,
    UnitOfWork,
)


if TYPE_CHECKING:
    from fastapi import Request

    from app.models.auth_users import User


class UserManager(BaseUserManager["User", int]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    def parse_id(self, user_id: str) -> int:
        return int(user_id)

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Request | None = None,
        uow: IUnitOfWork = Depends(UnitOfWork),
    ) -> "User":
        created_user = await super().create(user_create, safe, request)
        match created_user.role.value:
            case "employed":
                await EmployedUserService().register(uow=uow, user_id=created_user.id)
            case "unemployed":
                await UnemployedUserService().register(uow=uow, user_id=created_user.id)
        return created_user
