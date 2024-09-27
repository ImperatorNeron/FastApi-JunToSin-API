from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

from fastapi_users import (
    BaseUserManager,
    exceptions,
    schemas,
)
from fastapi_users.router.common import ErrorCode

from app.auth.dependencies.backend import authentication_backend
from app.auth.dependencies.fastapi_users_routers import fastapi_users_routers
from app.auth.dependencies.user_manager import get_user_manager
from app.schemas.auth_users import (
    UserCreate,
    UserRead,
)
from app.utils.unitofwork import (
    IUnitOfWork,
    UnitOfWork,
)


router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(
    router=fastapi_users_routers.get_auth_router(
        authentication_backend,
    ),
)

router.include_router(
    router=fastapi_users_routers.get_verify_router(
        UserRead,
    ),
)
router.include_router(
    router=fastapi_users_routers.get_reset_password_router(),
)


@router.post("/register", response_model=UserRead)
async def register(
    request: Request,
    user_create: UserCreate,
    user_manager: Annotated[BaseUserManager, Depends(get_user_manager)],
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork)],
):
    try:
        created_user = await user_manager.create(
            user_create,
            safe=True,
            request=request,
            uow=uow,
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )

    return schemas.model_validate(UserRead, created_user)
