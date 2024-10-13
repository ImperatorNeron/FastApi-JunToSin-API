import hmac
import random
from abc import (
    ABC,
    abstractmethod,
)

from pydantic import EmailStr

from app.settings.settings import settings
from app.utils.unitofwork import IUnitOfWork


class BaseCodeService(ABC):

    @abstractmethod
    async def generate_code(
        self,
        email: EmailStr,
        uow: IUnitOfWork,
    ) -> str: ...

    @abstractmethod
    async def validate_code(
        self,
        code: str,
        email: EmailStr,
        uow: IUnitOfWork,
    ) -> bool: ...


class RedisCacheCodeService(BaseCodeService):

    async def generate_code(self, email: EmailStr, uow: IUnitOfWork) -> str:
        secure_random = random.SystemRandom()
        code: str = str(secure_random.randint(100000, 999999))
        await uow.code_cache.set(
            name=email,
            value=code,
            expire=settings.code.expire_time,
        )
        return code

    async def validate_code(
        self,
        code: str,
        email: EmailStr,
        uow: IUnitOfWork,
    ) -> bool:
        cache_code = await uow.code_cache.get(email)
        if cache_code is None:
            return False
        return hmac.compare_digest(code, cache_code)
