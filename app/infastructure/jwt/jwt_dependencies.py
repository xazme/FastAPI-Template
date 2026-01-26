from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from app.core.config import settings
from .jwt_helper import JWTHelper


@lru_cache  # We can use LRU in this case
def get_jwt_helper():
    jwt_helper = JWTHelper(
        alogrithm=settings.algorithm,
        expire_days=settings.expire_days,
        expire_minutes=settings.expire_minutes,
        access_private_key=settings.access_private_key,
        access_public_key=settings.access_public_key,
        refresh_private_key=settings.refresh_private_key,
        refresh_public_key=settings.refresh_public_key,
    )
    return jwt_helper


JWTHelperDep = Annotated[JWTHelper, Depends(get_jwt_helper)]
