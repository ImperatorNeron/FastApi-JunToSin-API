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


class BaseAuthService(ABC):

    @abstractmethod
    async def register(): ...

    @abstractmethod
    async def get_user_by_username(): ...

    @abstractmethod
    async def is_unverified_user_by_email(): ...

    @abstractmethod
    async def update_user_by_email(): ...


class AuthService(BaseAuthService):

    async def register(
        self,
        uow: IUnitOfWork,
        user_in: CreateUserSchema,
    ) -> ReadUserSchema:
        return await uow.auth_users.create(item_in=user_in)

    async def get_user_by_username(
        self,
        uow: IUnitOfWork,
        username: str,
    ):
        return await uow.auth_users.fetch_by_attribute(
            "username",
            username,
        )

    async def is_unverified_user_by_email(
        self,
        uow: IUnitOfWork,
        email: EmailStr,
    ):
        user = await uow.auth_users.fetch_by_attribute("email", email)
        return user is not None and not user.is_verified

    async def update_user_by_email(
        self,
        uow: IUnitOfWork,
        email: EmailStr,
        update_data: BaseModel,
    ):
        return await uow.auth_users.update_by_field(
            name="email",
            value=email,
            item_in=update_data,
        )
