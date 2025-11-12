from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.database import ObjectNotFoundError, ObjectAlreadyExistsError


def not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, ObjectNotFoundError)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc) or "Object not found"},
    )


def already_exists_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, ObjectAlreadyExistsError)
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc) or "Object already exists"},
    )
