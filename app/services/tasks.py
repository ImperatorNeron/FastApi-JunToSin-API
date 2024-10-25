from app.schemas.tasks import (
    CreateTaskSchema,
    UpdateTaskSchema,
)
from app.utils.unitofwork import IUnitOfWork


class TaskService:

    async def fetch_all(self, uow: IUnitOfWork):
        async with uow:
            return await uow.tasks.fetch_all()

    async def create(self, task_in: CreateTaskSchema, uow: IUnitOfWork):
        async with uow:
            return await uow.tasks.create(task_in)

    async def fetch_by_id(self, task_id: int, uow: IUnitOfWork):
        async with uow:
            return await uow.tasks.fetch_by_id(item_id=task_id)

    async def fetch_by_username(self, username: str, uow: IUnitOfWork):
        async with uow:
            return await uow.tasks.fetch_by_attributes(username=username)

    async def update_by_id(
        self,
        task_id: int,
        task_in: UpdateTaskSchema,
        uow: IUnitOfWork,
    ):
        async with uow:
            return await uow.tasks.update_by_id(item_id=task_id, item_in=task_in)

    async def remove_by_id(
        self,
        task_id: int,
        uow: IUnitOfWork,
    ):
        async with uow:
            await uow.tasks.remove_by_id(item_id=task_id)
