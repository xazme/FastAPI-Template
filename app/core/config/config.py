import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from .constans import ENV_FILE_PATH

ENV = os.getenv("ENV", "dev")


class Config(BaseSettings):
    """
    Configuration class for base application settings using Pydantic's BaseSettings.

    This class defines common settings required for the application to run, such as
    host and port. It loads values from environment variables if available, falling
    back to defaults defined in the fields. The configuration supports external
    `.env` file loading with UTF-8 encoding.

    Attributes:
        app_host (str): The host IP address on which the FastAPI application will run.
            Defaults to "0.0.0.0" to allow external connections.
        app_port (int): The port number on which the application will be exposed.
            Defaults to 8000.

    Settings Configuration:
        - env_file: Path to the environment file (defined by ENV_FILE_PATH).
        - env_file_encoding: File encoding, set to UTF-8.

    Example:
        >>> settings = BaseConfig()
        >>> print(settings.app_host)
        '0.0.0.0'

    Note:
        This class is typically used as a base or directly instantiated to manage
        runtime configuration with strong typing and validation.
    """

    reload: bool = Field(default=False)
    workers: int = Field(default=8)
    docs_url: str | None = Field(default=None)
    redoc_url: str | None = Field(default=None)

    cors_origins: list[str] = Field(default=["https://givemeajobplz.com"])
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: list[str] = Field(default=["GET", "POST", "PUT", "DELETE"])
    cors_allow_headers: list[str] = Field(default=["*"])

    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )
