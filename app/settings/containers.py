from functools import lru_cache

import punq

from app.services.auth import (
    AuthService,
    BaseAuthService,
)
from app.services.code_senders import (
    BaseCodeSenderService,
    EmailSenderService,
)
from app.services.codes import (
    BaseCodeService,
    RedisCacheCodeService,
)
from app.services.tokens import (
    AbstractJWTTokenService,
    JWTTokenService,
)
from app.services.users import (
    BaseUserService,
    EmployedUserService,
    UnemployedUserService,
    UserService,
)
from app.use_cases.auth.login import LoginUserUseCase
from app.use_cases.auth.registration import RegisterUserUseCase
from app.use_cases.auth.send_varification_code import SendVerificationCodeUseCase
from app.use_cases.auth.verify import VerifyUseCase
from app.use_cases.users.user_profile import GetCurrentUserProfileUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # Services
    container.register(EmployedUserService)
    container.register(AbstractJWTTokenService, JWTTokenService)
    container.register(UnemployedUserService)
    container.register(BaseUserService, UserService)
    container.register(BaseAuthService, AuthService)
    container.register(BaseCodeService, RedisCacheCodeService)
    container.register(BaseCodeSenderService, EmailSenderService)

    # Use cases
    container.register(RegisterUserUseCase)
    container.register(LoginUserUseCase)
    container.register(GetCurrentUserProfileUseCase)
    container.register(SendVerificationCodeUseCase)
    container.register(VerifyUseCase)

    return container
