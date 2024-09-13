from app.utils.unitofwork import IUnitOfWork


class TaskService:

    async def get_all(self, uow: IUnitOfWork):
        async with uow:
            return await uow.tasks.get_all()
