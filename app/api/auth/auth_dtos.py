from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class LoginDTO(BaseModel):
    email: Annotated[
        EmailStr,
        Field(..., description="User email"),
    ]
    password: Annotated[
        str,
        Field(..., description="User password"),
    ]


class RegisterDTO(LoginDTO):
    name: Annotated[
        str,
        Field(..., description="User name"),
    ]


class LogOutDTO(BaseModel):
    user_id: Annotated[
        UUID,
        Field(..., description="User name"),
    ]


class ResponseAuthTokensDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshTokenDTO(BaseModel):
    refresh_token: Annotated[
        str,
        Field(..., description="User password"),
    ]
