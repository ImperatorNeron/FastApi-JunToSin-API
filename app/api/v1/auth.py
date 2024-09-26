from fastapi import APIRouter

from app.auth.dependencies.backend import authentication_backend
from app.auth.dependencies.fastapi_users_routers import fastapi_users_routers
from app.schemas.auth_users import (
    UserCreate,
    UserRead,
)


router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(
    router=fastapi_users_routers.get_auth_router(authentication_backend),
)

router.include_router(
    router=fastapi_users_routers.get_register_router(UserRead, UserCreate),
)

router.include_router(router=fastapi_users_routers.get_verify_router(UserRead))

router.include_router(router=fastapi_users_routers.get_reset_password_router())
