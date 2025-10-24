from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from .base import Base


class DataBaseHelper:
    def __init__(
        self,
        db_url: str,
        echo: bool = False,
        autoflush: bool = False,
        expire_on_commit: bool = False,
    ) -> None:
        self.db_url: str = db_url
        self.echo: bool = echo
        self.autoflush: bool = autoflush
        self.expire_on_commit: bool = expire_on_commit
        self.__engine: AsyncEngine = create_async_engine(
            url=self.db_url,
            echo=self.echo,
        )
        self.__session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            class_=AsyncSession,
            bind=self.__engine,
            autoflush=self.autoflush,
            expire_on_commit=self.expire_on_commit,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.__session_factory() as session:
            yield session

    async def create_tables(self) -> None:
        async with self.__engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        async with self.__engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
