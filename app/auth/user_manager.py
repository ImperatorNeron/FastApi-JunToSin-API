from typing import (
    Optional,
    TYPE_CHECKING,
)

from fastapi_users import BaseUserManager

from app.settings.settings import settings


if TYPE_CHECKING:
    from fastapi import Request

    from app.models.auth_users import User


class UserManager(BaseUserManager["User", int]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    def parse_id(self, user_id: str) -> int:
        return int(user_id)

    async def on_after_register(
        self,
        user: "User",
        request: Optional["Request"] = None,
    ):
        match user.role.value:
            case "employed":
                print("Employed user has registered.")
            case "unemployed":
                print("Unemployed user has registered.")
            case "admin":
                print("Admin user has registered.")

        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self,
        user: "User",
        token: str,
        request: Optional["Request"] = None,
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self,
        user: "User",
        token: str,
        request: Optional["Request"] = None,
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
