from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Cookie, Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.api.user import User

from .auth_exceptions import EmptyTokenProvidedException, NotAuthenticatedException
from .auth_service import AuthService

http_bearer = HTTPBearer(auto_error=False)


@inject
def get_access_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
) -> str:
    if not credentials:
        raise NotAuthenticatedException()
    token = credentials.credentials
    if not token:
        raise EmptyTokenProvidedException()
    return token


@inject
async def get_current_user(
    auth_service: FromDishka[AuthService],
    access_token: Annotated[str, Depends(get_access_token)],
) -> User:
    return await auth_service.get_user_from_access_token(access_token=access_token)


async def get_refresh_token(refresh_token: Annotated[str | None, Cookie()]) -> str:
    if not refresh_token:
        raise EmptyTokenProvidedException()
    return refresh_token


RefreshTokenDep = Annotated[str, Depends(get_refresh_token)]
