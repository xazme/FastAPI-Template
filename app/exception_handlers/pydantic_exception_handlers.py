from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError


def pydantic_validation_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, ValidationError)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": str(exc) or "Invalid input"},
    )
