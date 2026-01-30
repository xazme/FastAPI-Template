import logging
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from faststream.kafka import KafkaBroker
from app.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    db_helper = DataBaseHelper(
        db_url=settings.postgres_connection,
        echo=True,
    )

    broker = KafkaBroker(bootstrap_servers=settings)

    await db_helper.create_tables()
    app.state.pro
    yield
    # await db_helper.drop_tables()
    await db_helper.dispose()
