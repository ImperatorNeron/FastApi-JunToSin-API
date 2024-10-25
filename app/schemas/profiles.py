from app.schemas.roled_users import (
    BaseEmployedUserSchema,
    BaseUnemployedUserSchema,
)
from app.schemas.users import ReadUserSchema


class UnemployedUserProfileSchema(
    ReadUserSchema,
    BaseUnemployedUserSchema,
):
    pass


class EmployedUserProfileSchema(
    ReadUserSchema,
    BaseEmployedUserSchema,
):
    pass
