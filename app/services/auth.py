from abc import (
    ABC,
    abstractmethod,
)

from pydantic import (
    BaseModel,
    EmailStr,
)

from app.schemas.users import (
    CreateUserSchema,
    ReadUserSchema,
)
from app.utils.unitofwork import IUnitOfWork


class BaseAuthService(ABC):

    @abstractmethod
    async def register(
        self,
        uow: IUnitOfWork,
        user_in: CreateUserSchema,
    ) -> BaseModel: ...

    @abstractmethod
    async def get_user_by_username(
        self,
        uow: IUnitOfWork,
        username: str,
    ) -> BaseModel: ...

    @abstractmethod
    async def is_unverified_user_by_email(
        self,
        uow: IUnitOfWork,
        email: EmailStr,
    ) -> bool: ...

    @abstractmethod
    async def update_user_by_email(
        self,
        uow: IUnitOfWork,
        email: EmailStr,
        update_data: BaseModel,
    ) -> BaseModel: ...


class AuthService(BaseAuthService):

    async def register(
        self,
        uow: IUnitOfWork,
        user_in: CreateUserSchema,
    ) -> ReadUserSchema:
        return await uow.users.create(item_in=user_in)

    async def get_user_by_username(
        self,
        uow: IUnitOfWork,
        username: str,
    ) -> ReadUserSchema:
        return await uow.users.fetch_one_by_attributes(username=username)

    async def is_unverified_user_by_email(
        self,
        uow: IUnitOfWork,
        email: EmailStr,
    ) -> bool:
        user = await uow.users.fetch_one_by_attributes(email=email)
        return user is not None and not user.is_verified

    async def update_user_by_email(
        self,
        uow: IUnitOfWork,
        email: EmailStr,
        update_data: BaseModel,
    ) -> ReadUserSchema:
        return await uow.users.update_by_attributes(
            item_in=update_data,
            email=email,
        )
