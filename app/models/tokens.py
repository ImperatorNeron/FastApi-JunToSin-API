from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)

from app.models.base import BaseModel
from app.models.mixins import UserRelationMixin


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class AccessToken(BaseModel, SQLAlchemyBaseAccessTokenTable[int], UserRelationMixin):

    _back_populates = "access_token"

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyAccessTokenDatabase(session, cls)
