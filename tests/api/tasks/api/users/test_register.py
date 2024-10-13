import pytest
from httpx import AsyncClient

from app.schemas.auth_users import RegisterUserSchema
from app.utils.unitofwork import IUnitOfWork


# TODO: Add some validations tests

@pytest.mark.asyncio(loop_scope="session")
async def test_register(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
):
    response = await async_client.post(
        url="/api/v1/auth/register",
        json=auth_user_payload.model_dump(mode="json"),
    )
    assert response.status_code == 200
    assert response.json()["data"]["username"] == auth_user_payload.username


@pytest.mark.asyncio(loop_scope="session")
async def test_is_registered(
    async_client: AsyncClient,
    uow: IUnitOfWork,
    auth_user_payload: RegisterUserSchema,
):
    response = await async_client.post(
        url="/api/v1/auth/register",
        json=auth_user_payload.model_dump(mode="json"),
    )
    assert response.status_code == 200
    user_in_db = await uow.auth_users.get_one_by_field(
        "username",
        auth_user_payload.username,
    )
    assert response.json()["data"]["username"] == user_in_db.username
