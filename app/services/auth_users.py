from abc import (
    ABC,
    abstractmethod,
)

from pydantic import (
    BaseModel,
    EmailStr,
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
    async def is_unverified_user_by_email(): ...

    @abstractmethod
    async def get_user_with_profile(): ...

    @abstractmethod
    async def update_user_by_email(): ...


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

    async def is_unverified_user_by_email(
        self,
        uow: IUnitOfWork,
        email: EmailStr,
    ):
        user = await uow.auth_users.get_one_by_field("email", email)
        return user is not None and not user.is_verified

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

    async def update_user_by_email(
        self, uow: IUnitOfWork, email: EmailStr, update_data: BaseModel,
    ):
        return await uow.auth_users.update_one_by_field(
            field_name="email",
            field_value=email,
            item_in=update_data,
        )
