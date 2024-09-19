import pytest
from httpx import AsyncClient
from tests.api.common import post_items
from tests.factories.users.employed_users import EmployedUsersModelFactory


@pytest.mark.asyncio(loop_scope="session")
async def test_get_employed_users_empty_list(async_client: AsyncClient):
    response = await async_client.get("/api/v1/employed-users/")
    assert len(response.json()["data"]["users"]) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_get_employed_users(async_client: AsyncClient):
    expected_count = 5
    await post_items(
        async_client,
        "/api/v1/employed-users/",
        EmployedUsersModelFactory,
        expected_count,
    )
    get_response = await async_client.get("/api/v1/employed-users/")
    assert len(get_response.json()["data"]["users"]) == expected_count
