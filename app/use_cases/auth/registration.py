from dataclasses import dataclass

from app.schemas.users import (
    CreateUserSchema,
    ReadUserSchema,
    RegisterUserSchema,
)
from app.services.auth import BaseAuthService
from app.services.tokens import AbstractJWTTokenService
from app.services.users import (
    EmployedUserService,
    UnemployedUserService,
)
from app.use_cases.exceptions import InvalidUserRoleException
from app.utils.unitofwork import IUnitOfWork


@dataclass
class RegisterUserUseCase:
    auth_service: BaseAuthService
    employed_user_service: EmployedUserService
    unemployed_user_service: UnemployedUserService
    token_service: AbstractJWTTokenService

    async def __register_user(
        self,
        user_in: RegisterUserSchema,
        uow: IUnitOfWork,
    ) -> ReadUserSchema:
        user_auth_in = CreateUserSchema(
            **user_in.model_dump(exclude={"password"}),
            hashed_password=await self.token_service.hash_password(user_in.password),
        )
        return await self.auth_service.register(
            uow,
            user_auth_in,
        )

    async def __register_user_role(
        self,
        user: ReadUserSchema,
        uow: IUnitOfWork,
    ) -> None:

        attr = getattr(self, f"{user.role.value}_user_service", None)

        if attr is None:
            raise InvalidUserRoleException(f"Unsupported role: {user.role.value}")

        await attr.register(
            user_id=user.id,
            uow=uow,
        )

    async def execute(
        self,
        user_in: RegisterUserSchema,
        uow: IUnitOfWork,
    ) -> ReadUserSchema:
        async with uow:
            user = await self.__register_user(user_in=user_in, uow=uow)
            await self.__register_user_role(user=user, uow=uow)
            return user
