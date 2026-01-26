from .db_config import DataBaseConfig
from .jwt_config import JWTConfig


class ComponentsConfig(DataBaseConfig, JWTConfig): ...


__all__ = ["ComponentsConfig"]
