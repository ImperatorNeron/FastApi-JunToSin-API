from fastapi import (
    APIRouter,
    status,
)

from app.api.v1.dependencies import UOWDep
from app.schemas.api_response import ApiResponseSchema
from app.schemas.tasks import (
    CreateTaskSchema,
    ReadListTaskSchema,
    ReadTaskSchema,
    UpdateTaskSchema,
)
from app.services.tasks import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get(
    "/",
    response_model=ApiResponseSchema[ReadListTaskSchema],
)
async def get_tasks(
    uow: UOWDep,
):
    return ApiResponseSchema(
        data=ReadListTaskSchema(tasks=await TaskService().fetch_all(uow=uow)),
    )


@router.post(
    "/",
    response_model=ApiResponseSchema[ReadTaskSchema],
)
async def add_task(
    task_in: CreateTaskSchema,
    uow: UOWDep,
):
    return ApiResponseSchema(
        data=await TaskService().create(
            task_in=task_in,
            uow=uow,
        ),
    )


@router.get(
    "/{task_id}",
    response_model=ApiResponseSchema[ReadTaskSchema],
)
async def get_task(
    task_id: int,
    uow: UOWDep,
):
    return ApiResponseSchema(
        data=await TaskService().fetch_by_id(
            task_id=task_id,
            uow=uow,
        ),
    )


@router.patch(
    "/{task_id}",
    response_model=ApiResponseSchema[ReadTaskSchema],
)
async def update_task(
    task_id: int,
    task_in: UpdateTaskSchema,
    uow: UOWDep,
):
    return ApiResponseSchema(
        data=await TaskService().update_by_id(
            task_id=task_id,
            task_in=task_in,
            uow=uow,
        ),
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    uow: UOWDep,
):
    await TaskService().remove_by_id(
        task_id=task_id,
        uow=uow,
    )
