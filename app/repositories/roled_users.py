from app.models.roled_users import (
    EmployedUser,
    UnemployedUser,
)
from app.utils.sql_repository import SQLAlchemyRepository


class EmployedUserRepository(SQLAlchemyRepository):

    model = EmployedUser


class UnemployedUserRepository(SQLAlchemyRepository):

    model = UnemployedUser
