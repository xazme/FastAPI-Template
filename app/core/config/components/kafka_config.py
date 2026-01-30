from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..constans import ENV_FILE_PATH


class KafkaConfig(BaseSettings):
    kafka_bootstrap_servers: str = Field(default="111")
    kafka_acks: str | int = Field(default="all")
    kafka_retries: int = Field(default=10000)
    kafka_request_timeout_ms: int = Field(default=111)
    kafka_linger_ms: int = Field(default=111)
    kafka_enable_idempotence: bool = Field(default=True)
    kafka_max_in_flight_requests_per_connection: int = Field(default=5)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )
