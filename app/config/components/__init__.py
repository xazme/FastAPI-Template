from .db_config import DataBaseConfig
from .redis_config import RedisConfig


class ComponentsConfig(DataBaseConfig, RedisConfig): ...


__all__ = ["ComponentsConfig"]
