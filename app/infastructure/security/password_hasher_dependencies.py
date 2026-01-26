from typing import Annotated
from functools import lru_cache
from fastapi import Depends
from .password_hasher import PasswordHasher


@lru_cache  # We can use LRU in this case
def get_password_hasher():
    return PasswordHasher()


PasswordHasherDep = Annotated[PasswordHasher, Depends(get_password_hasher)]
