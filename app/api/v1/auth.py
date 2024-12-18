from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Form,
)

from punq import Container
from pydantic import EmailStr

from app.api.responses import login_responses
from app.api.v1.dependencies import UOWDep
from app.schemas.api_response import ApiResponseSchema
from app.schemas.tokens import TokenInfoSchema
from app.schemas.users import (
    LoginUserSchema,
    ReadUserSchema,
    RegisterUserSchema,
)
from app.settings.containers import get_container
from app.use_cases.auth.login import LoginUserUseCase
from app.use_cases.auth.registration import RegisterUserUseCase
from app.use_cases.auth.send_varification_code import SendVerificationCodeUseCase
from app.use_cases.auth.verify import VerifyUseCase


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=TokenInfoSchema,
    responses=login_responses,
)
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    container: Annotated[Container, Depends(get_container)],
    uow: UOWDep,
):
    use_case: LoginUserUseCase = container.resolve(LoginUserUseCase)
    user_in = LoginUserSchema(username=username, password=password)
    return await use_case.execute(uow=uow, user_in=user_in)


@router.post(
    "/register",
    response_model=ApiResponseSchema[ReadUserSchema],
)
async def register(
    user_in: RegisterUserSchema,
    container: Annotated[Container, Depends(get_container)],
    uow: UOWDep,
):
    use_case: RegisterUserUseCase = container.resolve(RegisterUserUseCase)
    result = await use_case.execute(user_in=user_in, uow=uow)
    return ApiResponseSchema(data=result)


# TODO: do email from json
@router.post("/send-verification-code")
async def send_verification_code(
    email: EmailStr,
    container: Annotated[Container, Depends(get_container)],
    uow: UOWDep,
):
    # TODO: додати нормальні response model
    use_case: SendVerificationCodeUseCase = container.resolve(
        SendVerificationCodeUseCase,
    )
    return await use_case.execute(email=email, uow=uow)


@router.post("/verify")
async def verify(
    email: EmailStr,
    code: str,
    container: Annotated[Container, Depends(get_container)],
    uow: UOWDep,
):
    use_case: VerifyUseCase = container.resolve(VerifyUseCase)
    return await use_case.execute(email=email, code=code, uow=uow)
