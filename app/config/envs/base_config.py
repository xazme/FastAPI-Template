from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..constans import ENV_FILE_PATH


class BaseConfig(BaseSettings):
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
    app_host: str = Field(
        default="0.0.0.0",
        description="Host for the app",
    )
    app_port: int = Field(
        default=8000,
        description="Port for the app",
    )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )
