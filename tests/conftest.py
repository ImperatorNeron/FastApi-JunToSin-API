import asyncio

import pytest
import pytest_asyncio
from httpx import (
    ASGITransport,
    AsyncClient,
)

from app.db.db import test_database_helper
from app.main import create_app
from app.models.base import BaseModel
from app.utils.unitofwork import (
    TestUnitOfWork,
    UnitOfWork,
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    async with test_database_helper.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with test_database_helper.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest_asyncio.fixture()
async def async_client():
    app = create_app()
    app.dependency_overrides[UnitOfWork] = TestUnitOfWork
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
