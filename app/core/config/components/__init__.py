from .db_config import DataBaseConfig
from .jwt_config import JWTConfig
from .kafka_config import KafkaConfig


class ComponentsConfig(DataBaseConfig, JWTConfig, KafkaConfig): ...


__all__ = ["ComponentsConfig"]
