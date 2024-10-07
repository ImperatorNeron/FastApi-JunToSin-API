from dataclasses import dataclass

from jwt import InvalidTokenError

from app.services.auth_users import BaseAuthUserService
from app.services.tokens import AbstractJWTTokenService
from app.use_cases.exceptions import InvalidTokenException
from app.utils.unitofwork import IUnitOfWork


@dataclass
class GetUserProfileUseCase:

    auth_user_service: BaseAuthUserService
    token_service: AbstractJWTTokenService

    async def execute(self, token: str, uow: IUnitOfWork) -> dict:
        try:
            payload = await self.token_service.decode_jwt(token=token)
        except InvalidTokenError as e:
            raise InvalidTokenException(detail=f"Invalid token error: {e}")

        username = payload.get("sub")
        role = payload.get("role")

        async with uow:
            return await self.auth_user_service.get_user_with_profile(
                username=username,
                role=role,
                uow=uow,
            )
