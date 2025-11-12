from fastapi import FastAPI
from pydantic import ValidationError
from app.database import ObjectNotFoundError, ObjectAlreadyExistsError
from .pydantic_exception_handlers import pydantic_validation_exception_handler
from .db_exception_handlers import (
    not_found_handler,
    already_exists_handler,
)


def init_db_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=ObjectNotFoundError,
        handler=not_found_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=ObjectAlreadyExistsError,
        handler=already_exists_handler,
    )


def init_pydantic_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=ValidationError,
        handler=pydantic_validation_exception_handler,
    )


def init_exception_handlers(app: FastAPI) -> None:
    init_db_exception_handlers(app=app)
    init_pydantic_exception_handlers(app=app)


__all__ = ["init_exception_handlers"]
