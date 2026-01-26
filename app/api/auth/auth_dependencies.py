from typing import Annotated, TYPE_CHECKING
from fastapi import Depends, Cookie
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from app.api.token import TokenServiceDep
from app.api.user import UserServiceDep
from app.infastructure.jwt import JWTHelperDep
from app.infastructure.security import PasswordHasherDep
from .auth_service import AuthService
from .auth_exceptions import NotAuthenticatedException, EmptyTokenProvidedException

if TYPE_CHECKING:
    from app.api.user import User

http_bearer = HTTPBearer(auto_error=False)


def get_access_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
) -> str:
    if not credentials:
        raise NotAuthenticatedException()
    token = credentials.credentials
    if not token:
        raise EmptyTokenProvidedException()
    return token


def get_auth_service(
    token_service: TokenServiceDep,
    user_service: UserServiceDep,
    jwt_helper: JWTHelperDep,
    password_hasher: PasswordHasherDep,
):
    return AuthService(
        jwt_helper=jwt_helper,
        password_hasher=password_hasher,
        token_service=token_service,
        user_service=user_service,
    )


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(
    auth_service: AuthServiceDep,
    access_token: Annotated[str, Depends(get_access_token)],
) -> "User":
    return await auth_service.get_user_from_access_token(access_token=access_token)


async def get_refresh_token(refresh_token: Annotated[str | None, Cookie()]) -> str:
    if not refresh_token:
        raise EmptyTokenProvidedException()
    return refresh_token


RefreshTokenDep = Annotated[str, Depends(get_refresh_token)]
