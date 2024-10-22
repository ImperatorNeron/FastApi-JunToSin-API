import pytest
from httpx import AsyncClient

from app.schemas.auth_users import RegisterUserSchema


@pytest.mark.asyncio(loop_scope="session")
async def test_send_verification_code(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
):

    user_response = await async_client.post(
        url="/api/v1/auth/register",
        json=auth_user_payload.model_dump(mode="json"),
    )
    assert user_response.status_code == 200

    response = await async_client.post(
        url="/api/v1/auth/send-verification-code",
        params={"email": user_response.json()["data"]["email"]},
    )
    print(response.json())
    assert response.status_code == 200
