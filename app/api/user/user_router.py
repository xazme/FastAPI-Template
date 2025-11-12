from uuid import UUID
from fastapi import APIRouter, Depends, Path, Body, status
from typing import Annotated
from .user_dto import CreateUserDTO, UpdateUserDTO, ResponseUserDTO
from .user_service import UserService
from .user_dependencies import get_user_service

router = APIRouter()


@router.get(
    path="/all",
    response_model=list[ResponseUserDTO],
    status_code=status.HTTP_200_OK,
)
async def get_all(
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_all()


@router.post(
    path="/create",
    response_model=ResponseUserDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    payload: Annotated[CreateUserDTO, Body(...)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return ResponseUserDTO.model_validate(
        await user_service.create(
            payload=payload.model_dump(),
        ),
    )


@router.get(
    path="/{user_id}",
    response_model=ResponseUserDTO,
    status_code=status.HTTP_200_OK,
)
async def get_one(
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
    status_code=status.HTTP_200_OK,
)
async def update(
    user_id: Annotated[UUID, Path(...)],
    payload: Annotated[UpdateUserDTO, Body(...)],
    user_service: Annotated[UserService, Depends(get_user_service)],
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
async def delete(
    user_id: Annotated[UUID, Path(...)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    await user_service.delete_by_id(id=user_id)
