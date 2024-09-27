from abc import (
    ABC,
    abstractmethod,
)

from app.schemas.roled_users import (
    CreateEmployedUserSchema,
    CreateUnemployedUserSchema,
)
from app.utils.unitofwork import IUnitOfWork


class BaseRoledUserService(ABC):

    @abstractmethod
    async def register(self, user_id: int, uow: IUnitOfWork) -> None: ...


class EmployedUserService:

    async def register(
        self,
        user_id: int,
        uow: IUnitOfWork,
    ):
        async with uow:
            user_in = CreateEmployedUserSchema(user_id=user_id)
            await uow.employed_users.add_one(item_in=user_in)


class UnemployedUserService:

    async def register(
        self,
        user_id: int,
        uow: IUnitOfWork,
    ):
        async with uow:
            user_in = CreateUnemployedUserSchema(user_id=user_id)
            await uow.unemployed_users.add_one(item_in=user_in)
