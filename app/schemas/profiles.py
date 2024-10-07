from app.schemas.auth_users import ReadUserSchema
from app.schemas.roled_users import (
    BaseEmployedUserSchema,
    BaseUnemployedUserSchema,
)


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
