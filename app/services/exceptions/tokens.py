class JWTExpiredError(Exception):

    def __init__(self, message: str = "Token has expired") -> None:
        self.message = message
        super().__init__(message)


class JWTInvalidError(Exception):

    def __init__(self, message: str = "Invalid token") -> None:
        self.message = message
        super().__init__(message)
