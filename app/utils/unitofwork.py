from abc import (
    ABC,
    abstractmethod,
)
from typing import Type

from app.db.db import (
    database_helper,
    test_database_helper,
)
from app.db.redis import (
    redis_helper,
    test_redis_helper,
)
from app.repositories.auth_user import AuthUserRepository
from app.repositories.roled_users import (
    EmployedUserRepository,
    UnemployedUserRepository,
)
from app.repositories.tasks import TaskRepository
from app.utils.redis_repository import RedisCacheRepository


class IUnitOfWork(ABC):
    tasks: Type[TaskRepository]
    auth_users: Type[AuthUserRepository]
    employed_users: Type[EmployedUserRepository]
    unemployed_users: Type[UnemployedUserRepository]
    code_cache: Type[RedisCacheRepository]

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
        self.redis_client = await redis_helper.get_redis_client()
        self.tasks = TaskRepository(self.session)
        self.auth_users = AuthUserRepository(self.session)
        self.employed_users = EmployedUserRepository(self.session)
        self.unemployed_users = UnemployedUserRepository(self.session)
        self.code_cache = RedisCacheRepository(self.redis_client)

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
        self.redis_client = await test_redis_helper.get_redis_client()
        self.tasks = TaskRepository(self.session)
        self.auth_users = AuthUserRepository(self.session)
        self.employed_users = EmployedUserRepository(self.session)
        self.unemployed_users = UnemployedUserRepository(self.session)
        self.code_cache = RedisCacheRepository(self.redis_client)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
