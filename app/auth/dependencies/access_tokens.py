from typing import (
    Annotated,
    TYPE_CHECKING,
)

from fastapi import Depends

from app.db.db import database_helper
from app.models.tokens import AccessToken


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: Annotated[
        "AsyncSession",
        Depends(database_helper.session_getter),
    ],
):
    yield AccessToken.get_db(session)
