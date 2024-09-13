from typing import List

from fastapi import APIRouter

from app.api.v1.dependencies import UOWDep
from app.schemas.tasks import ReadTaskSchema
from app.services.tasks import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[ReadTaskSchema])
async def get_tasks(
        uow: UOWDep,
):
    return await TaskService().get_all(uow=uow)
