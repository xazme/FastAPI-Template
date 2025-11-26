from .db_config import DataBaseConfig
from .redis_config import RedisConfig
from .jwt_config import JWTConfig


class ComponentsConfig(DataBaseConfig, RedisConfig, JWTConfig): ...


__all__ = ["ComponentsConfig"]
