import pytest
from httpx import AsyncClient

from app.schemas.auth_users import (
    LoginUserSchema,
    RegisterUserSchema,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_authenticated_user_profile(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
):
    register_response = await async_client.post(
        url="/api/v1/auth/register",
        json=auth_user_payload.model_dump(mode="json"),
    )

    assert register_response.status_code == 200

    login_credentials = LoginUserSchema(
        username=auth_user_payload.username,
        password=auth_user_payload.password,
    )

    login_response = await async_client.post(
        url="/api/v1/auth/login",
        data=login_credentials.model_dump(mode="json"),
    )

    token = login_response.json()["access_token"]

    assert login_response.status_code == 200
    assert token is not None

    response = await async_client.get(
        url="/api/v1/auth/users/me", headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == login_credentials.username
