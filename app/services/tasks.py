from app.schemas.tasks import (
    CreateTaskSchema,
    UpdateTaskSchema,
)
from app.utils.unitofwork import IUnitOfWork


class TaskService:

    async def get_all(self, uow: IUnitOfWork):
        async with uow:
            return await uow.tasks.get_all()

    async def add_task(self, task_in: CreateTaskSchema, uow: IUnitOfWork):
        async with uow:
            return await uow.tasks.add_one(task_in)

    async def get_task(self, task_id: int, uow: IUnitOfWork):
        async with uow:
            return await uow.tasks.get_one(item_id=task_id)

    async def update_task(
        self,
        task_id: int,
        task_in: UpdateTaskSchema,
        uow: IUnitOfWork,
    ):
        async with uow:
            return await uow.tasks.update_one(item_id=task_id, item_in=task_in)
