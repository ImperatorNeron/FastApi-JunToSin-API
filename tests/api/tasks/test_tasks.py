import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_get_tasks_empty_list(async_client: AsyncClient):
    response = await async_client.get("/api/v1/tasks/")
    assert len(response.json()["data"]["tasks"]) == 0
