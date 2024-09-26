from typing import (
    Annotated,
    TYPE_CHECKING,
)

from fastapi import Depends

from app.db.db import database_helper
from app.models.auth_users import User


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(
    session: Annotated[
        "AsyncSession",
        Depends(database_helper.session_getter),
    ],
):
    yield User.get_db(session)
