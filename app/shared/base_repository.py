from typing import Mapping, Sequence, TypeVar, Generic, Any, Optional
from sqlalchemy import delete, insert, select, func, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base
from .exceptions import ObjectNotFoundError, ObjectAlreadyExistsError

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    РЕПОЗИТОРИЙ НЕ КОММИТИТ. КОММИТ ВЫПОЛНЯЕТСЯ В СЕРВИСЕ
    """

    def __init__(
        self,
        model: type[T],
        session: AsyncSession,
    ) -> None:
        self.model: type[T] = model
        self.session: AsyncSession = session

    async def get(
        self,
        id: Any,
    ) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == id)
        orm_obj = await self.session.execute(statement=stmt)
        return orm_obj.scalar_one_or_none()

    async def get_one(
        self,
        /,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Optional[T]:
        stmt = select(self.model)
        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)
        try:
            res = await self.session.execute(statement=stmt)
            orm_obj = res.scalar_one()
            return orm_obj
        except NoResultFound:
            raise ObjectNotFoundError(f"{self.model.__name__} not found")

    async def get_one_or_none(
        self,
        /,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Optional[T]:
        stmt = select(self.model)
        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)
        res = await self.session.execute(statement=stmt)
        return res.scalar_one_or_none()

    async def get_all(self) -> Sequence[T]:
        stmt = select(self.model)
        res = await self.session.execute(statement=stmt)
        return res.scalars().all()

    async def get_all_filtered(
        self,
        /,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Sequence[T]:
        stmt = select(self.model)
        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)
        res = await self.session.execute(statement=stmt)
        return res.scalars().all()

    async def exists(
        self,
        /,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> bool:
        stmt = select(func.count()).select_from(self.model)
        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)
        res = await self.session.execute(statement=stmt)
        return bool(res.scalar_one())

    async def count(
        self,
        /,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> int:
        stmt = select(func.count()).select_from(self.model)
        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)
        res = await self.session.execute(statement=stmt)
        return res.scalar_one()

    async def create(
        self,
        payload: Mapping[str, Any],
    ) -> Optional[T]:
        stmt = insert(self.model).values(**dict(payload)).returning(self.model)
        try:
            res = await self.session.execute(statement=stmt)
            return res.scalar_one()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ObjectAlreadyExistsError(
                f"Integrity constraint failed on {self.model.__name__}: {exc.orig}"
            )

    async def update(
        self,
        /,
        payload: Mapping[str, Any],
        *where: ColumnElement[bool],
        **where_by: Any,
    ):
        stmt = update(self.model).values(**dict(payload)).returning(self.model)
        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)
        try:
            res = await self.session.execute(statement=stmt)
            obj = res.scalar_one_or_none()
            if obj is None:
                raise ObjectNotFoundError(f"{self.model.__name__} not found for update")
            return obj
        except IntegrityError as exc:
            await self.session.rollback()
            raise ObjectAlreadyExistsError(
                f"Integrity constraint failed on {self.model.__name__}: {exc.orig}"
            )

    async def delete(
        self,
        /,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> int:
        stmt = delete(self.model).returning(self.model.id)
        if not where and not where_by:
            raise ValueError("Delete without filter is not allowed")
        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)
        res = await self.session.execute(statement=stmt)
        deleted_ids = res.scalars().all()
        if not deleted_ids:
            raise ObjectNotFoundError(f"{self.model.__name__} not found for delete")
        return len(deleted_ids)
