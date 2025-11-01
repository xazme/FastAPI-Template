from typing import AsyncGenerator
from contextlib import asynccontextmanager
from pydantic import ValidationError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import db_helper
from app.error_handlers import (
    not_found_handler,
    already_exists_handler,
    validation_error_handler,
)
from app.shared import ObjectNotFoundError, ObjectAlreadyExistsError


def _init_router(_app: FastAPI) -> None:
    from app.api import router

    _app.include_router(router=router)


def _init_middleware(_app: FastAPI) -> None:
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )


def _init_exception_handler(_app: FastAPI) -> None:
    _app.add_exception_handler(ObjectNotFoundError, not_found_handler)
    _app.add_exception_handler(ObjectAlreadyExistsError, already_exists_handler)
    _app.add_exception_handler(ValidationError, validation_error_handler)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        # await db_helper.create_tables()
        yield
        # await db_helper.drop_tables()
        await db_helper.dispose()
    except Exception:
        raise


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
    )
    _init_middleware(_app)
    _init_router(_app)
    _init_exception_handler(_app)
    return _app


app = create_app()
