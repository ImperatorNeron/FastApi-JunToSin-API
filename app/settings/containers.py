from functools import lru_cache

import punq

from app.services.auth_users import (
    AuthUserService,
    BaseAuthUserService,
)
from app.services.roled_users import (
    EmployedUserService,
    UnemployedUserService,
)
from app.services.tokens import (
    AbstractJWTTokenService,
    JWTTokenService,
)
from app.use_cases.login import LoginUserUseCase
from app.use_cases.registration import RegisterUserUseCase
from app.use_cases.user_profile import GetUserProfileUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # Services
    container.register(EmployedUserService)
    container.register(AbstractJWTTokenService, JWTTokenService)
    container.register(UnemployedUserService)
    container.register(BaseAuthUserService, AuthUserService)

    # Use cases
    container.register(RegisterUserUseCase)
    container.register(LoginUserUseCase)
    container.register(GetUserProfileUseCase)

    return container
