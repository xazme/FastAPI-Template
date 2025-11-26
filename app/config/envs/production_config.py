from pydantic import Field
from .base_config import BaseConfig


class ProductionConfig(BaseConfig):
    env: str = Field(
        default="production",
    )
    reload: bool = Field(
        default=False,
    )
    workers: int = Field(
        default=8,
    )
    docs_url: str | None = Field(
        default=None,
    )
    redoc_url: str | None = Field(
        default=None,
    )

    # CORS
    cors_origins: list[str] = Field(
        default=["https://example.com"],
    )
    cors_allow_credentials: bool = Field(
        default=True,
    )
    cors_allow_methods: list[str] = Field(
        default=["GET", "POST", "PUT", "DELETE"],
    )
    cors_allow_headers: list[str] = Field(
        default=["*"],
    )
