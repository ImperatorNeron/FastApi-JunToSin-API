from app.models.users import EmployedUser
from app.utils.repositories import SQLAlchemyRepository


class EmployedUserRepository(SQLAlchemyRepository):
    model = EmployedUser
