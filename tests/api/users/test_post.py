import pytest
from httpx import AsyncClient
from tests.factories.users.employed_users import EmployedUsersModelFactory

from app.models.users import EmployedUser


@pytest.mark.asyncio(loop_scope="session")
async def test_post_employed_user(async_client: AsyncClient):
    employed_user: EmployedUser = EmployedUsersModelFactory.create()
    employed_user_schema_data = employed_user.to_read_model()
    response = await async_client.post(
        "/api/v1/employed-users/",
        json=employed_user_schema_data.model_dump(mode='json'),
    )
    assert response.status_code == 200
    assert response.json()["data"]["username"] == employed_user.username
