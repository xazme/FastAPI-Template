from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body, Path, status

from app.api.auth.rbac import RequiredRoleForEveryone

from .user_dtos import ResponseUserDTO, UpdateUserDTO
from .user_service import UserService

router = APIRouter()


@router.get(
    path="/all",
    response_model=list[ResponseUserDTO],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all(
    user_service: FromDishka[UserService],
):
    return await user_service.get_all()


@router.get(
    path="/me",
    response_model=ResponseUserDTO,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_me(
    user: RequiredRoleForEveryone,
    user_service: FromDishka[UserService],
):
    return await user_service.get_one(id=user.id)


@router.get(
    path="/{user_id}",
    response_model=ResponseUserDTO,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_one(
    user_id: Annotated[UUID, Path(...)],
    user_service: FromDishka[UserService],
):
    return ResponseUserDTO.model_validate(
        await user_service.get_one(id=user_id),
    )


@router.patch(
    path="/{user_id}",
    response_model=ResponseUserDTO,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
@inject
async def update(
    user_id: Annotated[UUID, Path(...)],
    payload: Annotated[UpdateUserDTO, Body(...)],
    user_service: FromDishka[UserService],
):
    return ResponseUserDTO.model_validate(
        await user_service.update_by_id(
            id=user_id,
            payload=payload.model_dump(exclude_unset=True),
        )
    )


@router.delete(
    path="/{user_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete(
    user_id: Annotated[UUID, Path(...)],
    user_service: FromDishka[UserService],
):
    await user_service.delete_by_id(id=user_id)
