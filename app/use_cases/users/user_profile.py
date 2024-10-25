from dataclasses import dataclass

from jwt import InvalidTokenError
from pydantic import BaseModel

from app.services.tokens import AbstractJWTTokenService
from app.services.users import BaseUserService
from app.use_cases.exceptions import InvalidTokenException
from app.utils.unitofwork import IUnitOfWork


@dataclass
class GetCurrentUserProfileUseCase:

    auth_user_service: BaseUserService
    token_service: AbstractJWTTokenService

    async def execute(self, token: str, uow: IUnitOfWork) -> BaseModel:
        try:
            payload = await self.token_service.decode_jwt(token=token)
        except InvalidTokenError as e:
            raise InvalidTokenException(detail=f"Invalid token error: {e}")

        username = payload.get("sub")
        role = payload.get("role")

        async with uow:
            return await self.auth_user_service.fetch_current_user_profile(
                username=username,
                role=role,
                uow=uow,
            )
