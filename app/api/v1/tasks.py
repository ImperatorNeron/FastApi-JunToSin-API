from typing import List

from fastapi import APIRouter

from app.api.v1.dependencies import UOWDep
from app.schemas.tasks import (
    CreateTaskSchema,
    ReadTaskSchema,
    UpdateTaskSchema,
)
from app.services.tasks import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[ReadTaskSchema])
async def get_tasks(
    uow: UOWDep,
):
    return await TaskService().get_all(uow=uow)


@router.post("/")
async def add_task(
    task_in: CreateTaskSchema,
    uow: UOWDep,
):
    return await TaskService().add_task(
        task_in=task_in,
        uow=uow,
    )


@router.get("/{task_id}", response_model=ReadTaskSchema)
async def get_task(
    task_id: int,
    uow: UOWDep,
):
    return await TaskService().get_task(
        task_id=task_id,
        uow=uow,
    )


@router.patch("/{task_id}", response_model=ReadTaskSchema)
async def update_task(
    task_id: int,
    task_in: UpdateTaskSchema,
    uow: UOWDep,
):
    return await TaskService().update_task(
        task_id=task_id,
        task_in=task_in,
        uow=uow,
    )
