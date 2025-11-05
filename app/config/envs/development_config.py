from pydantic import Field
from .base_config import BaseConfig


class DevelopmentConfig(BaseConfig):
    env: str = Field(default="development")
    reload: bool = Field(default=True)
    workers: int = Field(default=1)
    docs_url: str = Field(default="/docs")
    redoc_url: str = Field(default="/redoc")

    # CORS
    cors_origins: list[str] = Field(default=["*"])
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: list[str] = Field(default=["*"])
    cors_allow_headers: list[str] = Field(default=["*"])
