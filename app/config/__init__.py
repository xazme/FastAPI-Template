from typing import Union
from .components import ComponentsConfig
from .envs import DevelopmentConfig, ProductionConfig


class ProductionSettings(ProductionConfig, ComponentsConfig): ...


class DevelopmentSettings(DevelopmentConfig, ComponentsConfig): ...


def get_settings() -> Union[ProductionSettings, DevelopmentSettings]:
    env = ComponentsConfig().env
    print(env)
    if env == "development":
        return DevelopmentSettings()
    elif env == "production":
        return ProductionSettings()
    else:
        raise ValueError(f"Unknown environment: {env}")


settings: Union[ProductionSettings, DevelopmentSettings] = get_settings()

__all__ = ["settings"]
