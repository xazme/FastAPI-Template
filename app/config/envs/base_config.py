from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..constans import ENV_FILE_PATH


class BaseConfig(BaseSettings):
    app_host: str = Field(default="0.0.0.0", description="Host for the app")
    app_port: int = Field(default=8000, description="Port for the app")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )
