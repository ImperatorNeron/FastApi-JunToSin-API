from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

def create_app() -> FastAPI:
    application = FastAPI(
        title="JunToSin API",
        docs_url="/api/docs",
        description="PetProject using FastApi/Docker/SqlAlchemy/Alembic",
        default_response_class=ORJSONResponse,
        debug=True,
    )

    return application