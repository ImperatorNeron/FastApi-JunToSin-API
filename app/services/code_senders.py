from abc import (
    ABC,
    abstractmethod,
)

from pydantic import EmailStr


class BaseCodeSenderService(ABC):

    @abstractmethod
    async def send_code(self, email: EmailStr, code: str) -> bool: ...


class EmailSenderService(BaseCodeSenderService):

    async def send_code(self, email: EmailStr, code: str) -> bool:
        # do it with real email
        print(f"User: {email}, code: {code}")
        return True
