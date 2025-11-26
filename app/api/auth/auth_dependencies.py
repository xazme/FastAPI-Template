from typing import Annotated, TYPE_CHECKING
from functools import lru_cache
from fastapi import Depends, Cookie
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from app.api.token import TokenServiceDep
from app.api.user import UserServiceDep
from app.config import settings
from .jwt import JWTHelper
from .utils import PasswordHasher
from .auth_service import AuthService
from .auth_exceptions import NotAuthenticatedException, EmptyTokenProvidedException

if TYPE_CHECKING:
    from app.api.user import User

http_bearer = HTTPBearer(auto_error=False)


def get_access_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
) -> str:
    if not credentials:
        raise NotAuthenticatedException(details="Not authenticated")
    token = credentials.credentials
    if not token:
        raise EmptyTokenProvidedException(details="Empty token provided")
    return token


@lru_cache  # We can use LRU in this case
def get_jwt_helper():
    jwt_helper = JWTHelper(
        alogrithm=settings.algorithm,
        expire_days=settings.expire_days,
        expire_minutes=settings.expire_minutes,
        access_private_key=settings.access_private_key,
        access_public_key=settings.access_public_key,
        refresh_private_key=settings.refresh_private_key,
        refresh_public_key=settings.refresh_public_key,
    )
    return jwt_helper


@lru_cache  # We can use LRU in this case
def get_password_hasher():
    return PasswordHasher()


JWTHelperDep = Annotated[JWTHelper, Depends(get_jwt_helper)]
PasswordHasherDep = Annotated[PasswordHasher, Depends(get_password_hasher)]


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
        raise EmptyTokenProvidedException(details="Refresh Token is empty")
    return refresh_token


RefreshTokenDep = Annotated[str, Depends(get_refresh_token)]
