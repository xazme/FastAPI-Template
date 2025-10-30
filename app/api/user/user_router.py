from uuid import UUID
from fastapi import APIRouter, Depends, Path, Body
from typing import Annotated
from .user_dto import CreateUserDTO, UpdateUserDTO, ResponseUserDTO
from .user_service import UserService
from .user_dependencies import get_user_service

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    path="/all",
    response_model=list[ResponseUserDTO],
)
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_all()


@router.post(
    path="/create",
    response_model=ResponseUserDTO,
    status_code=201,
)
async def create_user(
    payload: Annotated[CreateUserDTO, Body(...)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return ResponseUserDTO.model_validate(
        await user_service.create(payload.model_dump()),
    )


@router.get(
    path="/{user_id}",
    response_model=ResponseUserDTO,
)
async def get_user(
    user_id: Annotated[UUID, Path(...)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return ResponseUserDTO.model_validate(
        await user_service.get_one(id=user_id),
    )


@router.patch(
    path="/{user_id}",
    response_model=ResponseUserDTO,
    response_model_exclude_unset=True,
)
async def update_user(
    user_id: Annotated[UUID, Path(...)],
    payload: Annotated[UpdateUserDTO, Body(...)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return ResponseUserDTO.model_validate(
        await user_service.update_by_id(user_id, payload.model_dump(exclude_unset=True))
    )


@router.delete(
    path="/{user_id}",
    response_model=int,
)
async def delete_user(
    user_id: Annotated[UUID, Path(...)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return ResponseUserDTO.model_validate(
        await user_service.delete_by_id(user_id),
    )
