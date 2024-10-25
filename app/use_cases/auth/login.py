from dataclasses import dataclass

from app.schemas.tokens import TokenInfoSchema
from app.schemas.users import (
    LoginUserSchema,
    ReadUserWithPasswordSchema,
)
from app.services.auth import BaseAuthService
from app.services.tokens import AbstractJWTTokenService
from app.use_cases.exceptions import InvalidCredentialsException
from app.utils.unitofwork import IUnitOfWork


@dataclass
class LoginUserUseCase:

    auth_service: BaseAuthService
    token_service: AbstractJWTTokenService

    async def __fetch_user_by_username(
        self,
        uow: IUnitOfWork,
        username: str,
    ) -> ReadUserWithPasswordSchema:
        user: ReadUserWithPasswordSchema = await self.auth_service.get_user_by_username(
            uow=uow,
            username=username,
        )

        if not user:
            raise InvalidCredentialsException()

        return user

    def __is_valid_password(
        self,
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return self.token_service.validate_password(
            password=password,
            hashed_password=hashed_password,
        )

    async def __generate_token(self, username: str, role: str) -> TokenInfoSchema:
        payload = {"sub": username, "role": role}
        token = await self.token_service.encode_jwt(payload=payload)

        return TokenInfoSchema(
            access_token=token,
            token_type="Bearer",
        )

    async def execute(
        self,
        uow: IUnitOfWork,
        user_in: LoginUserSchema,
    ):
        async with uow:
            user = await self.__fetch_user_by_username(
                uow=uow,
                username=user_in.username,
            )

            if not self.__is_valid_password(
                user_in.password,
                user.hashed_password,
            ):
                raise InvalidCredentialsException()

            return await self.__generate_token(user_in.username, user.role.value)
