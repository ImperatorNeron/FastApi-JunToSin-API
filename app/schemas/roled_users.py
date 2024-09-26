from typing import Optional

from pydantic import BaseModel


class BaseEmployedUserSchema(BaseModel):
    description: Optional[str] = None


class ReadEmployedUserSchema(BaseEmployedUserSchema):
    user_id: int


class CreateEmployedUserSchema(BaseEmployedUserSchema):
    pass


class UpdateEmployedUserSchema(BaseEmployedUserSchema):
    pass
