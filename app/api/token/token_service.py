from sqlalchemy.ext.asyncio import AsyncSession

from app.infastructure.database import BaseService

from .token_dtos import UpsertTokenDTO
from .token_model import Token
from .token_repository import TokenRepository


class TokenService(BaseService[Token]):
    def __init__(
        self,
        repository: TokenRepository,
        session: AsyncSession,
    ) -> None:
        super().__init__(
            repository=repository,
            session=session,
        )
        self.token_repository = repository

    async def upsert(
        self,
        payload: UpsertTokenDTO,
    ) -> None:
        await self.token_repository.upsert(
            payload=payload.model_dump(),
        )
        await self._safe_commit()
