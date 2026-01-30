from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..constans import ENV_FILE_PATH


class KafkaConfig(BaseSettings):
    kafka_bootstrap_servers: str = Field(...)
    kafka_acks: str | int = Field(...)
    kafka_retries: int = Field(...)
    kafka_delivery_timeout_ms: int = Field(...)
    kafka_request_timeout_ms: int = Field(...)
    kafka_linger_ms: int = Field(...)
    kafka_enable_idempotence: bool = Field(...)
    kafka_max_in_flight_requests_per_connection: int = Field(...)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )
