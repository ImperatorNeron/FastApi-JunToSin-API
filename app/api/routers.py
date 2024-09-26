from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer

from app.api.v1.routers import router as v1_router
from app.schemas.ping import PingResponseSchema


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/api",
    dependencies=[Depends(http_bearer)],
)
router.include_router(router=v1_router)


@router.get(
    "/ping",
    response_model=PingResponseSchema,
    tags=["Ping"],
)
async def ping():
    return PingResponseSchema(result=True)
