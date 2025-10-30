from typing import TypeVar, Generic, Any, Optional, Sequence, Mapping
from sqlalchemy.sql import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base

from .base_repository import BaseRepository

T = TypeVar(name="T", bound=Base)


class BaseService(Generic[T]):
    def __init__(
        self,
        repository: BaseRepository[T],
        session: AsyncSession,
    ) -> None:
        self.repository: BaseRepository[T] = repository
        self.session: AsyncSession = session

    async def get(self, id: Any) -> Optional[T]:
        return await self.repository.get(id=id)

    async def get_one(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Optional[T]:
        return await self.repository.get_one(*where, **where_by)

    async def get_one_or_none(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Optional[T]:
        return await self.repository.get_one_or_none(*where, **where_by)

    async def get_all(self) -> Sequence[T]:
        return await self.repository.get_all()

    async def get_all_filtered(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Sequence[T]:
        return await self.repository.get_all_filtered(*where, **where_by)

    async def exists(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> bool:
        return await self.repository.exists(*where, **where_by)

    async def count(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> int:
        return await self.repository.count(*where, **where_by)

    async def create(
        self,
        payload: Mapping[str, Any],
    ) -> Optional[T]:
        obj = await self.repository.create(payload)
        await self._safe_commit()
        return obj

    async def update(
        self,
        payload: Mapping[str, Any],
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Optional[T]:
        obj = await self.repository.update(payload, *where, **where_by)
        await self._safe_commit()
        return obj

    async def update_by_id(
        self,
        _id: Any,
        payload: Mapping[str, Any],
    ) -> Optional[T]:
        obj = await self.repository.update(payload=payload, id=_id)
        await self._safe_commit()
        return obj

    async def delete(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> int:
        obj = await self.repository.delete(*where, **where_by)
        await self._safe_commit()
        return obj

    async def delete_by_id(self, _id: Any) -> int:
        obj = await self.repository.delete(id=_id)
        await self._safe_commit()
        return obj

    async def _safe_commit(self):
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
