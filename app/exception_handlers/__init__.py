from fastapi import FastAPI
from pydantic import ValidationError
from app.database.db_exceptions import ObjectNotFoundError, ObjectAlreadyExistsError
from app.api.auth.auth_exceptions import (
    PasswordIsIncorrectException,
    AccountAlreadyExists,
    RefreshTokenCompromisedException,
    NotAuthenticatedException,
    EmptyTokenProvidedException,
    NotEnoughtPermissionsException,
)
from app.api.auth.jwt.jwt_exceptions import JWTExpiredError, JWTInvalidError
from .pydantic_exception_handlers import pydantic_validation_exception_handler
from .db_exception_handlers import (
    not_found_handler,
    already_exists_handler,
)
from .auth_exception_handlers import (
    password_incorrect_handler,
    account_already_exists_handler,
    refresh_token_compromised_handler,
    not_authenticated_handler,
    empty_token_provided_handler,
    not_enough_permissions_handler,
)
from .jwt_exception_handlers import jwt_expired_handler, jwt_invalid_handler


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


def init_auth_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=PasswordIsIncorrectException,
        handler=password_incorrect_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=AccountAlreadyExists,
        handler=account_already_exists_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=RefreshTokenCompromisedException,
        handler=refresh_token_compromised_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=NotAuthenticatedException,
        handler=not_authenticated_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=EmptyTokenProvidedException,
        handler=empty_token_provided_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=NotEnoughtPermissionsException,
        handler=not_enough_permissions_handler,
    )


def init_jwt_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(JWTExpiredError, jwt_expired_handler)
    app.add_exception_handler(JWTInvalidError, jwt_invalid_handler)


def init_exception_handlers(app: FastAPI) -> None:
    init_db_exception_handlers(app=app)
    init_pydantic_exception_handlers(app=app)
    init_auth_exception_handlers(app=app)
    init_jwt_exception_handlers(app=app)


__all__ = ["init_exception_handlers"]
