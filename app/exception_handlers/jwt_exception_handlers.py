from fastapi import Request, status
from fastapi.responses import JSONResponse


def jwt_expired_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Token expired"},
        headers={"WWW-Authenticate": "Bearer"},
    )


def jwt_invalid_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid token"},
        headers={"WWW-Authenticate": "Bearer"},
    )
