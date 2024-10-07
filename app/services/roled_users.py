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


class EmployedUserService(BaseRoledUserService):

    async def register(
        self,
        user_id: int,
        uow: IUnitOfWork,
    ) -> None:
        user_in = CreateEmployedUserSchema(user_id=user_id)
        await uow.employed_users.add_one(item_in=user_in)


class UnemployedUserService(BaseRoledUserService):

    async def register(
        self,
        user_id: int,
        uow: IUnitOfWork,
    ) -> None:
        user_in = CreateUnemployedUserSchema(user_id=user_id)
        await uow.unemployed_users.add_one(item_in=user_in)
