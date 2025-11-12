from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import db_helper
from app.api import init_routers
from app.middlewares import init_middlewares
from app.exception_handlers import init_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        # await db_helper.create_tables()
        yield
        # await db_helper.drop_tables()
        await db_helper.dispose()
    except Exception:
        raise


def create_app() -> FastAPI:
    app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
    )
    init_middlewares(app=app)
    init_routers(app=app)
    init_exception_handlers(app=app)
    return app


app = create_app()
