from fastapi import APIRouter, Body, status, Response
from typing import Annotated
from .auth_dto import (
    LoginDTO,
    RegisterDTO,
    LogOutDTO,
    ResponseAuthTokensDTO,
    RefreshTokenDTO,
)
from .auth_dependencies import AuthServiceDep, RefreshTokenDep
from .rbac import RequiredRoleForEveryone

router = APIRouter()


@router.post(
    path="/login",
    response_model=ResponseAuthTokensDTO,
    response_model_exclude={"refresh_token"},
    status_code=status.HTTP_200_OK,
)
async def login(
    response: Response,
    payload: Annotated[LoginDTO, Body(...)],
    auth_service: AuthServiceDep,
):
    tokensDTO = await auth_service.login(payload=payload)
    response.set_cookie(
        key="refresh_token",
        value=tokensDTO.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )
    return tokensDTO


@router.post(
    path="/register",
    response_model=ResponseAuthTokensDTO,
    response_model_exclude={"refresh_token"},
    status_code=status.HTTP_201_CREATED,
)
async def register(
    response: Response,
    payload: Annotated[RegisterDTO, Body(...)],
    auth_service: AuthServiceDep,
):
    tokensDTO = await auth_service.register(payload=payload)
    response.set_cookie(
        key="refresh_token",
        value=tokensDTO.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )
    return tokensDTO


@router.delete(
    path="/logout",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    response: Response,
    user: RequiredRoleForEveryone,
    auth_service: AuthServiceDep,
):
    await auth_service.logout(payload=LogOutDTO(user_id=user.id))
    response.delete_cookie(key="refresh_token")


@router.post(
    path="/refresh",
    response_model=ResponseAuthTokensDTO,
    status_code=status.HTTP_200_OK,
)
async def refresh(
    response: Response,
    refresh_token: RefreshTokenDep,
    auth_service: AuthServiceDep,
):
    tokensDTO = await auth_service.refresh_token(
        payload=RefreshTokenDTO(refresh_token=refresh_token)
    )
    response.set_cookie(
        key="refresh_token",
        value=tokensDTO.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )
    return tokensDTO
