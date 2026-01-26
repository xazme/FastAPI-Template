import logging
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infastructure.database import db_helper
from app.core.config import get_current_env

logger = logging.getLogger(__name__)


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Using %s enviroment", get_current_env())
    """
    Manage the lifespan of the FastAPI application with asynchronous startup and shutdown events.

    This async context manager is used to handle setup and teardown logic for the FastAPI
    application lifecycle. Currently, it supports shutdown operations such as safely
    disposing of the database connection pool. Startup logic can be added as needed.

    The function yields control back to the application during its runtime. On shutdown,
    it ensures that the database helper disposes of any active connections or resources.

    Args:
        app (FastAPI): The FastAPI application instance to which this lifespan is attached.

    Yields:
        AsyncGenerator[None, None]: A generator that yields control during app runtime.

    Example:
        app = FastAPI(lifespan=app_lifespan)

    Note:
        Lines for creating and dropping tables are commented out and can be enabled
        for development or testing if needed.
    """

    await db_helper.create_tables()
    yield
    # await db_helper.drop_tables()
    await db_helper.dispose()
