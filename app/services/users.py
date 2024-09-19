from app.schemas.users import CreateEmployedUserSchema
from app.utils.unitofwork import IUnitOfWork


class EmployedUserService:

    async def get_all(self, uow: IUnitOfWork):
        async with uow:
            return await uow.employed_users.get_all()

    async def add_user(self, user_in: CreateEmployedUserSchema, uow: IUnitOfWork):
        async with uow:
            return await uow.employed_users.add_one(user_in)

    async def delete_user(self, user_id, uow: IUnitOfWork):
        async with uow:
            return await uow.employed_users.delete_one(user_id)
