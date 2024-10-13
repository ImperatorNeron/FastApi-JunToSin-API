from random import SystemRandom

import factory

from app.schemas.auth_users import RegisterUserSchema
from app.utils.enums import UserRole


class AuthUserPayloadFactory(factory.Factory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    phone_number = factory.Sequence(lambda n: "38096%07d" % n)
    password = factory.Faker("password", length=20)
    role = factory.LazyAttribute(
        lambda _: SystemRandom().choice(
            [
                UserRole.EMPLOYED.value,
                UserRole.UNEMPLOYED.value,
            ],
        ),
    )

    class Meta:
        model = RegisterUserSchema
