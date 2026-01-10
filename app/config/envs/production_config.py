from pydantic import Field
from .base_config import BaseConfig


class ProductionConfig(BaseConfig):
    """
    Configuration class for production environment settings.

    This class extends BaseConfig with settings optimized for a secure and efficient
    production deployment. It disables development features like auto-reload and
    documentation endpoints, uses multiple workers, and restricts CORS to trusted domains.

    Attributes:
        env (str): Environment identifier, set to "production".
        reload (bool): Disables auto-reload for stability in production.
        workers (int): Number of Uvicorn worker processes; defaults to 8 for better performance.
        docs_url (str | None): Disables Swagger UI documentation by setting the path to None.
        redoc_url (str | None): Disables ReDoc documentation by setting the path to None.

    CORS Settings:
        cors_origins (list[str]): List of allowed origins for cross-origin requests.
            Defaults to ["https://example.com"] — should be updated to actual frontend domains.
        cors_allow_credentials (bool): Allows credentials (e.g., cookies) in CORS requests.
        cors_allow_methods (list[str]): HTTP methods permitted in CORS requests.
            Restricts to common safe methods: GET, POST, PUT, DELETE.
        cors_allow_headers (list[str]): Headers allowed in CORS requests. Supports any header by default.

    Example:
        >>> settings = ProductionConfig()
        >>> print(settings.env)
        'production'
        >>> print(settings.docs_url)
        None

    Note:
        The documentation UI (docs_url, redoc_url) is disabled in production for security.
        CORS settings should be strictly configured to trusted origins in real deployments.
    """

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
