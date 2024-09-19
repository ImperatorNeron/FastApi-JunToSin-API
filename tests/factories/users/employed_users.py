from datetime import datetime

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.db.db import test_database_helper
from app.models.users import EmployedUser


class EmployedUsersModelFactory(SQLAlchemyModelFactory):

    id = factory.Sequence(lambda n: n)  # noqa
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    hashed_password = factory.Faker("password", length=50)
    phone_number = factory.Sequence(lambda n: "38096%07d" % n)
    description = factory.Faker("text")
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)

    class Meta:
        model = EmployedUser
        sqlalchemy_session_factory = test_database_helper.session_factory
