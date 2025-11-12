from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import db_helper


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        # await db_helper.create_tables()
        yield
        # await db_helper.drop_tables()
        await db_helper.dispose()
    except Exception:
        raise
