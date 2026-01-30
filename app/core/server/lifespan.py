import logging
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infastructure import init_db, init_kafka

logger = logging.getLogger(__name__)


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    db_helper = await init_db(app)
    broker = await init_kafka(app)

    # await db_helper.create_tables()
    await broker.start()
    yield
    # await db_helper.drop_tables()
    await broker.stop()
    # await db_helper.dispose()
