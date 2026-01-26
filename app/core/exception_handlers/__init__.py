from fastapi import FastAPI
from app.core.exceptions import DomainBaseException
from .domain_exception_handler import domain_exceptions_handler


def init_domain_exception_handler(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=DomainBaseException,
        handler=domain_exceptions_handler,  # type: ignore
    )


def init_exception_handlers(app: FastAPI) -> None:
    init_domain_exception_handler(app=app)


__all__ = ["init_exception_handlers"]
