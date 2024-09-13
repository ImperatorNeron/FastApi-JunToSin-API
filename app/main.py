from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.routers import router as api_router


def create_app() -> FastAPI:
    application = FastAPI(
        title="JunToSin API",
        docs_url="/api/docs",
        description="PetProject using FastApi/Docker/SqlAlchemy/Alembic",
        default_response_class=ORJSONResponse,
        debug=True,
    )
    application.include_router(router=api_router)
    return application
