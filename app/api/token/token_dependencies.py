from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import db_helper
from .token_repository import TokenRepository
from .token_service import TokenService


def get_token_service(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
):
    repository = TokenRepository(session=session)
    return TokenService(
        repository=repository,
        session=session,
    )


TokenServiceDep = Annotated[TokenService, Depends(get_token_service)]
