from dataclasses import dataclass

from pydantic import EmailStr

from app.schemas.users import UpdateUserVerificationSchema
from app.services.auth import BaseAuthService
from app.services.codes import BaseCodeService
from app.utils.unitofwork import IUnitOfWork


@dataclass
class VerifyUseCase:

    auth_service: BaseAuthService
    code_service: BaseCodeService

    async def execute(
        self,
        email: EmailStr,
        code: str,
        uow: IUnitOfWork,
    ):
        async with uow:
            is_valid = await self.code_service.validate_code(
                code=code,
                email=email,
                uow=uow,
            )
            if is_valid:
                await self.auth_service.update_user_by_email(
                    uow=uow,
                    email=email,
                    update_data=UpdateUserVerificationSchema(is_verified=True),
                )
                # TODO: Зробити нормальні повернення
                return {"is_varified": True}
