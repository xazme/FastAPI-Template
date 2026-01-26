from typing import TypeVar
from fastapi import status
from app.core.exceptions import DomainBaseException
from .base import Base

T = TypeVar(name="T", bound=Base)


class ObjectNotFoundException(DomainBaseException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(
        self,
        message: str = f"{T.__name__} not found",
        details: str | None = None,
    ) -> None:
        super().__init__(message, details)


class ObjectAlreadyExistsException(DomainBaseException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(
        self,
        message: str = f"{T.__name__} already exists",
        details: str | None = None,
    ) -> None:
        super().__init__(message, details)
