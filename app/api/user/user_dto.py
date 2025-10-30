import uuid
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class CreateUserDTO(BaseModel):
    name: Annotated[str, Field(default=...)]
    email: Annotated[EmailStr, Field(default=...)]
    password: Annotated[str, Field(default=...)]


class UpdateUserDTO(CreateUserDTO): ...


class ResponseUserDTO(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    name: str
    email: EmailStr
    password: str

    model_config = ConfigDict(
        from_attributes=True,
    )
