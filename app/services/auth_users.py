from abc import (
    ABC,
    abstractmethod,
)

from app.schemas.auth_users import (
    CreateUserSchema,
    ReadUserSchema,
)
from app.utils.unitofwork import IUnitOfWork


class BaseAuthUserService(ABC):

    @abstractmethod
    async def register(): ...

    @abstractmethod
    async def get_user_by_username(): ...

    @abstractmethod
    async def get_user_with_profile(): ...


class AuthUserService(BaseAuthUserService):

    async def register(
        self,
        uow: IUnitOfWork,
        user_in: CreateUserSchema,
    ) -> ReadUserSchema:
        return await uow.auth_users.add_one(item_in=user_in)

    async def get_user_by_username(
        self,
        uow: IUnitOfWork,
        username: str,
    ):
        return await uow.auth_users.get_one_by_field(
            "username",
            username,
        )

    async def get_user_with_profile(
        self,
        uow: IUnitOfWork,
        username: str,
        role: str,
    ):
        return await uow.auth_users.get_user_with_profile(
            username=username,
            role=role,
        )
