from abc import (
    ABC,
    abstractmethod,
)

from pydantic import BaseModel

from app.schemas.roled_users import (
    CreateEmployedUserSchema,
    CreateUnemployedUserSchema,
)
from app.utils.unitofwork import IUnitOfWork


class BaseUserService(ABC):

    @abstractmethod
    async def fetch_current_user_profile(
        self,
        uow: IUnitOfWork,
        username: str,
        role: str,
    ) -> BaseModel: ...

    @abstractmethod
    async def fetch_user_profile(
        self,
        uow: IUnitOfWork,
        username: str,
    ) -> BaseModel: ...

    @abstractmethod
    async def fetch_user_tasks(
        self,
        uow: IUnitOfWork,
        username: str,
    ) -> list[BaseModel]: ...


class UserService(BaseUserService):

    async def fetch_current_user_profile(
        self,
        uow: IUnitOfWork,
        username: str,
        role: str,
    ) -> BaseModel:
        return await uow.users.fetch_user_profile(
            username=username,
            role=role,
        )

    async def fetch_user_profile(
        self,
        uow: IUnitOfWork,
        username: str,
    ):
        async with uow:
            user = await uow.users.fetch_one_by_attributes(username=username)
            return await self.fetch_current_user_profile(
                uow=uow,
                username=user.username,
                role=user.role.value,
            )

    async def fetch_user_tasks(
        self,
        uow: IUnitOfWork,
        username: str,
    ) -> list[BaseModel]:
        async with uow:
            user = await uow.users.fetch_one_by_attributes(username=username)
            # TODO: do normal error
            if user is None:
                raise ValueError("User wasn`t found")
            if user.role.value == "unemployed":
                return await uow.tasks.fetch_by_attributes(unemployed_user_id=user.id)
            if user.role.value == "employed":
                return await uow.tasks.fetch_by_attributes(employed_user_id=user.id)


class BaseRoledUserService(ABC):

    @abstractmethod
    async def register(
        self,
        user_id: int,
        uow: IUnitOfWork,
    ) -> None: ...


class EmployedUserService(BaseRoledUserService):

    async def register(
        self,
        user_id: int,
        uow: IUnitOfWork,
    ) -> None:
        user_in = CreateEmployedUserSchema(user_id=user_id)
        await uow.employed_users.create(item_in=user_in)


class UnemployedUserService(BaseRoledUserService):

    async def register(
        self,
        user_id: int,
        uow: IUnitOfWork,
    ) -> None:
        user_in = CreateUnemployedUserSchema(user_id=user_id)
        await uow.unemployed_users.create(item_in=user_in)
