from pydantic import Field
from .base_config import BaseConfig


class DevelopmentConfig(BaseConfig):
    """
    Configuration class for development environment settings.

    This class extends BaseConfig with settings tailored for local development.
    It enables features such as auto-reload, single-worker mode, and full CORS
    permissions to facilitate a smooth and flexible development experience.

    Attributes:
        env (str): Environment identifier, set to "development".
        reload (bool): Enables auto-reloading of the server when code changes are detected.
        workers (int): Number of Uvicorn worker processes; set to 1 for development.
        docs_url (str): Path to expose Swagger UI documentation. Enabled by default at "/docs".
        redoc_url (str): Path to expose ReDoc documentation. Enabled by default at "/redoc".

    CORS Settings:
        cors_origins (list[str]): List of allowed origins for cross-origin requests. Defaults to ["*"].
        cors_allow_credentials (bool): Allows credentials (e.g., cookies) in CORS requests.
        cors_allow_methods (list[str]): HTTP methods allowed in CORS requests. Defaults to ["*"].
        cors_allow_headers (list[str]): Headers allowed in CORS requests. Defaults to ["*"].

    Example:
        >>> settings = DevelopmentConfig()
        >>> print(settings.env)
        'development'
        >>> print(settings.reload)
        True

    Note:
        Wildcard CORS settings are used for convenience during development but should
        never be used in production environments due to security risks.
    """

    env: str = Field(
        default="development",
    )
    reload: bool = Field(
        default=True,
    )
    workers: int = Field(
        default=1,
    )
    docs_url: str = Field(
        default="/docs",
    )
    redoc_url: str = Field(
        default="/redoc",
    )

    # CORS
    cors_origins: list[str] = Field(
        default=["*"],
    )
    cors_allow_credentials: bool = Field(
        default=True,
    )
    cors_allow_methods: list[str] = Field(
        default=["*"],
    )
    cors_allow_headers: list[str] = Field(
        default=["*"],
    )
