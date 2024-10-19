from fastapi import status


success_login_response = {
    status.HTTP_200_OK: {
        "description": "Successful login, returns a JWT token",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "your_token_here",
                    "token_type": "Bearer",
                },
            },
        },
    },
}

invalid_credentials_response = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Invalid credentials",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid username or password"},
            },
        },
    },
}

server_error_response = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {"detail": "An unexpected error occurred."},
            },
        },
    },
}

login_responses = {
    **success_login_response,
    **invalid_credentials_response,
    **server_error_response,
}
