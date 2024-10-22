from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.auth_users import User
from app.models.tasks import Task
from app.repositories.exceptions import UnhandledRoleError
from app.schemas.profiles import (
    EmployedUserProfileSchema,
    UnemployedUserProfileSchema,
)
from app.utils.sql_repository import SQLAlchemyRepository


class AuthUserRepository(SQLAlchemyRepository):

    model = User

    async def _return_valid_profile_schema(self, user_profile: User) -> BaseModel:

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

    async def _get_user_with_profile_result(
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

    async def get_user_with_profile(self, username: str, role: str) -> BaseModel:
        user_profile = await self._get_user_with_profile_result(role, username)
        return await self._return_valid_profile_schema(user_profile)

    async def get_tasks_for_employed_user(self, user_id: int) -> list[BaseModel]:
        result = await self.session.execute(
            select(Task).where(Task.employed_user_id == user_id),
        )
        return [task.to_read_model() for task in result.scalars().all()]

    async def get_tasks_for_unemployed_user(self, user_id: int) -> list[BaseModel]:
        result = await self.session.execute(
            select(Task).where(Task.unemployed_user_id == user_id),
        )
        return [task.to_read_model() for task in result.scalars().all()]
