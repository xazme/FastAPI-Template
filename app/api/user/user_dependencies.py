from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import db_helper
from .user_service import UserService
from .user_repository import UserRepository


def get_user_service(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> UserService:
    repository = UserRepository(session=session)
    return UserService(repository=repository, session=session)
