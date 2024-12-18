from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.users import User
from app.repositories.exceptions import UnhandledRoleError
from app.schemas.profiles import (
    EmployedUserProfileSchema,
    UnemployedUserProfileSchema,
)
from app.utils.sql_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):

    model = User

    async def __generate_profile_schema(self, user_profile: User) -> BaseModel:

        basic_profile = user_profile.to_read_model().model_dump(
            exclude=["hashed_password"],
        )

        profile_map = {
            "employed": EmployedUserProfileSchema,
            "unemployed": UnemployedUserProfileSchema,
        }

        role = user_profile.role.value
        if role not in profile_map:
            raise UnhandledRoleError(role)

        return profile_map[role](
            **basic_profile,
            **getattr(user_profile, f"{role}_user")
            .to_read_model()
            .model_dump(
                exclude=["user_id"],
            ),
        )

    async def __fetch_user_with_profile(
        self,
        role: str,
        username: str,
    ) -> User:
        result = await self.session.execute(
            select(self.model)
            .options(
                joinedload(getattr(self.model, f"{role}_user")),
            )
            .where(self.model.username == username),
        )
        return result.scalars().first()

    async def fetch_user_profile(self, username: str, role: str) -> BaseModel:
        user_profile = await self.__fetch_user_with_profile(role, username)
        return await self.__generate_profile_schema(user_profile)
