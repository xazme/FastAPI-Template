from typing import Annotated
from fastapi import Depends
from app.infastructure.database import SessionDep
from .user_service import UserService
from .user_repository import UserRepository


def get_user_service(
    session: SessionDep,
) -> UserService:
    repository = UserRepository(session=session)
    return UserService(
        repository=repository,
        session=session,
    )


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
