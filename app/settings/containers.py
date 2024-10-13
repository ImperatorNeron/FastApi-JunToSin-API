from functools import lru_cache

import punq

from app.services.auth_users import (
    AuthUserService,
    BaseAuthUserService,
)
from app.services.code_senders import (
    BaseCodeSenderService,
    EmailSenderService,
)
from app.services.codes import (
    BaseCodeService,
    RedisCacheCodeService,
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
from app.use_cases.send_varification_code import SendVerificationCodeUseCase
from app.use_cases.user_profile import GetUserProfileUseCase
from app.use_cases.verify import VerifyUseCase


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
    container.register(BaseCodeService, RedisCacheCodeService)
    container.register(BaseCodeSenderService, EmailSenderService)

    # Use cases
    container.register(RegisterUserUseCase)
    container.register(LoginUserUseCase)
    container.register(GetUserProfileUseCase)
    container.register(SendVerificationCodeUseCase)
    container.register(VerifyUseCase)

    return container
