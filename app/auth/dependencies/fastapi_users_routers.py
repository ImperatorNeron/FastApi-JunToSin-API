from typing import TYPE_CHECKING

from fastapi_users import FastAPIUsers

from app.auth.dependencies.backend import authentication_backend
from app.auth.dependencies.user_manager import get_user_manager


if TYPE_CHECKING:
    pass


fastapi_users_routers = FastAPIUsers["User", int](
    get_user_manager,
    [authentication_backend],
)

current_active_user = fastapi_users_routers.current_user(active=True)
current_active_super_user = fastapi_users_routers.current_user(
    active=True,
    superuser=True,
)
