from typing import (
    Annotated,
    TYPE_CHECKING,
)

from fastapi import Depends

from fastapi_users.authentication.strategy.db import DatabaseStrategy

from app.auth.dependencies.access_tokens import get_access_token_db
from app.settings.settings import settings


if TYPE_CHECKING:
    from fastapi_users.authentication.strategy.db import AccessTokenDatabase

    from app.models.tokens import AccessToken


def get_database_strategy(
    access_token_db: Annotated[
        "AccessTokenDatabase[AccessToken]",
        Depends(get_access_token_db),
    ],
) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=settings.access_token.lifetime_seconds,
    )