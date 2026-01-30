from typing import Annotated
from fastapi import Depends
from app.infastructure.database import SessionDep
from .token_repository import TokenRepository
from .token_service import TokenService


def get_token_service(
    session: SessionDep,
):
    repository = TokenRepository(session=session)
    return TokenService(
        repository=repository,
        session=session,
    )


TokenServiceDep = Annotated[TokenService, Depends(get_token_service)]
