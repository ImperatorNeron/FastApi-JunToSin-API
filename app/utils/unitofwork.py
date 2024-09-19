from abc import (
    ABC,
    abstractmethod,
)
from typing import Type

from app.db.db import (
    database_helper,
    test_database_helper,
)
from app.repositories.tasks import TaskRepository
from app.repositories.users import EmployedUserRepository


class IUnitOfWork(ABC):
    tasks: Type[TaskRepository]
    employed_users: Type[EmployedUserRepository]

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(IUnitOfWork):

    async def __aenter__(self):
        self.session = database_helper.session_factory()
        self.tasks = TaskRepository(self.session)
        self.employed_users = EmployedUserRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class TestUnitOfWork(IUnitOfWork):

    async def __aenter__(self):
        self.session = test_database_helper.session_factory()
        self.tasks = TaskRepository(self.session)
        self.employed_users = EmployedUserRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
