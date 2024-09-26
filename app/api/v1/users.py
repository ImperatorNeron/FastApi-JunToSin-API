from fastapi import APIRouter

from app.auth.dependencies.fastapi_users_routers import fastapi_users_routers
from app.schemas.auth_users import (
    UserRead,
    UserUpdate,
)


router = APIRouter(prefix="/users", tags=["Users"])

router.include_router(
    router=fastapi_users_routers.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
