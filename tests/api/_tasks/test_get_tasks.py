import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_get_tasks_empty(async_client: AsyncClient):
    response = await async_client.get(url="/api/v1/tasks/")
    assert response.status_code == 200
    assert len(response.json()["data"]["tasks"]) == 0
