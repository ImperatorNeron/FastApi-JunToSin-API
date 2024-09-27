from fastapi_users.authentication import AuthenticationBackend

from app.auth.dependencies.strategy import get_database_strategy
from app.auth.transport import bearer_transport


authentication_backend = AuthenticationBackend(
    name="access-token-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)