from typing import Optional

from pydantic import BaseModel


class BaseEmployedUserSchema(BaseModel):
    description: Optional[str] = None


class ReadEmployedUserSchema(BaseEmployedUserSchema):
    user_id: int


class CreateEmployedUserSchema(ReadEmployedUserSchema):
    pass


class UpdateEmployedUserSchema(BaseEmployedUserSchema):
    pass


class BaseUnemployedUserSchema(BaseModel):
    linkedin_url: Optional[str] = None
    achivements: Optional[str] = None


class ReadUnemployedUserSchema(BaseUnemployedUserSchema):
    user_id: int


class CreateUnemployedUserSchema(ReadUnemployedUserSchema):
    pass


class UpdateUnemployedUserSchema(BaseUnemployedUserSchema):
    pass
