from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from punq import Container

from app.api.v1.dependencies import (
    oauth2_scheme,
    UOWDep,
)
from app.services.users import BaseUserService
from app.settings.containers import get_container
from app.use_cases.users.user_profile import GetCurrentUserProfileUseCase


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_authenticated_user_profile(
    container: Annotated[Container, Depends(get_container)],
    uow: UOWDep,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    use_case: GetCurrentUserProfileUseCase = container.resolve(
        GetCurrentUserProfileUseCase,
    )
    return await use_case.execute(token=token, uow=uow)


@router.get("/{username}/profile")
async def get_user_profile(
    username: str,
    container: Annotated[Container, Depends(get_container)],
    uow: UOWDep,
):
    service: BaseUserService = container.resolve(BaseUserService)
    return await service.fetch_user_profile(uow=uow, username=username)


@router.get("/{username}/tasks")
async def get_current_tasks_for_user(
    username: str,
    container: Annotated[Container, Depends(get_container)],
    uow: UOWDep,
):
    service: BaseUserService = container.resolve(BaseUserService)
    return await service.fetch_user_tasks(uow=uow, username=username)
