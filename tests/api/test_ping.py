import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_get_tasks_empty_list(async_client: AsyncClient):
    response = await async_client.get("/api/ping")
    assert response.json()["result"]
