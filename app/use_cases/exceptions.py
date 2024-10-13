from typing import (
    Any,
    Dict,
)

from fastapi import (
    HTTPException,
    status,
)


class InvalidCredentialsException(HTTPException):

    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Invalid credentials",
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class InvalidTokenException(HTTPException):

    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Invalid token",
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class InvalidUserRoleException(Exception):

    def __init__(self, message: str = "Invalid user role") -> None:
        self.message = message
        super().__init__(message)


class UserAlreadyExistsError(Exception):

    def __init__(self, message="User already exists or verified."):
        self.message = message
        super().__init__(self.message)
