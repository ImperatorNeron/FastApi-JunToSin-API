from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Form,
)
from fastapi.security import OAuth2PasswordBearer

from punq import Container

from app.api.v1.dependencies import UOWDep
from app.schemas.api_response import ApiResponseSchema
from app.schemas.auth_users import (
    LoginUserSchema,
    ReadUserSchema,
    RegisterUserSchema,
)
from app.schemas.tokens import TokenInfoSchema
from app.settings.containers import get_container
from app.use_cases.login import LoginUserUseCase
from app.use_cases.registration import RegisterUserUseCase
from app.use_cases.user_profile import GetUserProfileUseCase


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)

router = APIRouter(prefix="/auth", tags=["Users"])


@router.post(
    "/login",
    response_model=TokenInfoSchema,
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


@router.get("users/me")
async def auth_user_check(
    container: Annotated[Container, Depends(get_container)],
    uow: UOWDep,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    use_case: GetUserProfileUseCase = container.resolve(GetUserProfileUseCase)
    return await use_case.execute(token=token, uow=uow)
