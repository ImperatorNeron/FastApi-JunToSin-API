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
    async def get_user_with_profile(
        self,
        uow: IUnitOfWork,
        username: str,
        role: str,
    ) -> BaseModel: ...

    @abstractmethod
    async def get_user_tasks(
        self,
        uow: IUnitOfWork,
        username: str,
    ) -> list[BaseModel]: ...


class BaseRoledUserService(ABC):

    @abstractmethod
    async def register(
        self,
        user_id: int,
        uow: IUnitOfWork,
    ) -> None: ...


class UserService(BaseUserService):

    async def get_user_with_profile(
        self,
        uow: IUnitOfWork,
        username: str,
        role: str,
    ) -> BaseModel:
        return await uow.auth_users.get_user_with_profile(
            username=username,
            role=role,
        )

    async def get_user_tasks(
        self,
        uow: IUnitOfWork,
        username: str,
    ) -> list[BaseModel]:
        async with uow:
            user = await uow.auth_users.fetch_by_attribute("username", username)
            # TODO: do normal error
            if user is None:
                raise ValueError("User wasn`t found")
            if user.role.value == "unemployed":
                return await uow.auth_users.get_tasks_for_unemployed_user(user.id)
            if user.role.value == "employed":
                return await uow.auth_users.get_tasks_for_employed_user(user.id)


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
