from dataclasses import dataclass

from pydantic import EmailStr

from app.services.auth import BaseAuthService
from app.services.code_senders import BaseCodeSenderService
from app.services.codes import BaseCodeService
from app.use_cases.exceptions import UserAlreadyExistsError
from app.utils.unitofwork import IUnitOfWork


@dataclass
class SendVerificationCodeUseCase:

    auth_user_service: BaseAuthService
    code_service: BaseCodeService
    sender_service: BaseCodeSenderService

    async def execute(self, email: EmailStr, uow: IUnitOfWork):
        async with uow:
            is_user = await self.auth_user_service.is_unverified_user_by_email(
                uow=uow,
                email=email,
            )
            if is_user:
                code = await self.code_service.generate_code(uow=uow, email=email)
            else:
                raise UserAlreadyExistsError()
            return await self.sender_service.send_code(
                email=email,
                code=code,
            )
