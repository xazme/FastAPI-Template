from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.config import settings
from .base import Base
from .db_decorators import db_exception_handler


class DataBaseHelper:
    """
    A helper class for managing asynchronous database connections and operations using SQLAlchemy 2.x with AsyncIO.

    This class encapsulates the creation of an async engine, session factory, and provides
    convenient methods to manage database tables (create/drop) and retrieve async database sessions.
    It supports configurable behavior such as echo, autoflush, and expire-on-commit settings.

    Args:
        db_url (str): The database connection URL (e.g., 'postgresql+asyncpg://...').
        echo (bool): If True, SQL statements will be logged. Default is False.
        autoflush (bool): If True, the session will automatically flush changes before queries. Default is False.
        expire_on_commit (bool): If True, all instances are expired after commit. Default is False.

    Attributes:
        __engine (AsyncEngine): The SQLAlchemy async engine used for database connection.
        __session_factory (async_sessionmaker[AsyncSession]): A factory for creating new async sessions.

    Example:
        >>> db_helper = DataBaseHelper(db_url="postgresql+asyncpg://...", echo=True)
        >>> async for session in db_helper.get_session():
        ...     user = await session.get(User, 1)
    """

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

    # @db_exception_handler FIXME ГЕНЕРАТОР
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
<<<<<<< HEAD
=======
        """
        Provide an asynchronous database session generator.

        This method yields a new async session from the session factory and ensures
        proper closure of the session after use. It is intended to be used with
        'async with' or in FastAPI dependencies.

        Yields:
            AsyncGenerator[AsyncSession, None]: An asynchronous generator that yields a single AsyncSession.

        Note:
            The session is automatically closed once the context exits.
            The @db_exception_handler decorator is currently commented out (FIXME)
            because it may not be compatible with generators.
        """
>>>>>>> dev
        async with self.__session_factory() as session:
            yield session

    @db_exception_handler
    async def create_tables(self) -> None:
<<<<<<< HEAD
=======
        """
        Create all database tables defined in the Base metadata.

        This method uses the engine to connect to the database and synchronously runs
        the table creation process within an asynchronous context using run_sync.

        It is typically used during development or testing to set up the schema.

        Raises:
            Exception: If table creation fails and @db_exception_handler is active,
                       the exception will be handled accordingly.
        """
>>>>>>> dev
        async with self.__engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    @db_exception_handler
    async def drop_tables(self) -> None:
<<<<<<< HEAD
=======
        """
        Drop all database tables defined in the Base metadata.

        This method connects to the database and synchronously removes all tables
        using SQLAlchemy's metadata.drop_all method within an async context.

        Use with caution — this will result in complete data loss.

        Raises:
            Exception: If table dropping fails and @db_exception_handler is active,
                       the exception will be handled accordingly.
        """
>>>>>>> dev
        async with self.__engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

    @db_exception_handler
    async def dispose(self) -> None:
<<<<<<< HEAD
=======
        """
        Dispose of the async engine and close all associated connections.

        This method should be called during application shutdown to cleanly
        release all database resources and avoid connection leaks.

        Raises:
            Exception: If engine disposal fails and @db_exception_handler is active,
                       the exception will be handled accordingly.
        """
>>>>>>> dev
        await self.__engine.dispose()


db_helper = DataBaseHelper(
    db_url=settings.postgres_connection,
    echo=True,
)
