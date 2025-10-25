from .base_config import BaseConfig
from .db_config import DataBaseConfig
from .redis_config import RedisConfig


class ComponentsConfig(BaseConfig, DataBaseConfig, RedisConfig): ...
