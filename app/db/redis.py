import redis.asyncio as redis

from app.settings.settings import settings


class RedisHelper:

    def __init__(
        self,
        url: str,
    ) -> None:
        self.url = url

    async def get_redis_client(self):
        return await redis.from_url(url=self.url)


redis_helper = RedisHelper(settings.redis.url)
test_redis_helper = RedisHelper(settings.test_redis.url)
