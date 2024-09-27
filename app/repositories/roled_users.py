from app.models.roled_users import (
    EmployedUser,
    UnemployedUser,
)
from app.utils.repositories import SQLAlchemyRepository


class EmployedUserRepository(SQLAlchemyRepository):

    model = EmployedUser


class UnemployedUserRepository(SQLAlchemyRepository):

    model = UnemployedUser
