from fastapi import (
    APIRouter,
    status,
)

from app.api.v1.dependencies import UOWDep
from app.schemas.api_response import ApiResponseSchema
from app.schemas.users import (
    CreateEmployedUserSchema,
    ReadEmployedUserListSchema,
    ReadEmployedUserSchema,
)
from app.services.users import EmployedUserService


router = APIRouter(prefix="/employed-users", tags=["Employed users"])


@router.get(
    "/",
    response_model=ApiResponseSchema[ReadEmployedUserListSchema],
)
async def get_employed_users(
    uow: UOWDep,
):
    users = await EmployedUserService().get_all(uow=uow)
    return ApiResponseSchema(
        data=ReadEmployedUserListSchema(
            users=users,
        ),
    )


@router.post(
    "/",
    response_model=ApiResponseSchema[ReadEmployedUserSchema],
)
async def create_employed_user(
    user_in: CreateEmployedUserSchema,
    uow: UOWDep,
):
    user = await EmployedUserService().add_user(user_in=user_in, uow=uow)
    return ApiResponseSchema(data=user)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employed_user(
    used_id: int,
    uow: UOWDep,
):
    await EmployedUserService().delete_user(
        user_id=used_id,
        uow=uow,
    )
