from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Optional,
)

import redis.asyncio as redis


class AbstractCacheRepository(ABC):

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int) -> None: ...  # noqa

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...


class RedisCacheRepository(AbstractCacheRepository):

    def __init__(self, client: redis.Redis) -> None:
        self.client = client

    async def set(self, name: str, value: Any, expire: int) -> None:  # noqa
        await self.client.set(name=name, value=value, ex=expire)

    async def get(self, name: str) -> Optional[Any]:
        value = await self.client.get(name=name)
        if value:
            return value.decode("utf-8")

    async def delete(self, name: str) -> None:
        return await self.client.delete(name=name)
