import os
from dotenv import load_dotenv
from typing import Union
from .components import ComponentsConfig
from .envs import DevelopmentConfig, ProductionConfig
from .constans import APP_DIR, ROOT_DIR, ENV_FILE_PATH

load_dotenv()


class ProductionSettings(ProductionConfig, ComponentsConfig): ...


class DevelopmentSettings(DevelopmentConfig, ComponentsConfig): ...


def get_settings() -> Union[ProductionSettings, DevelopmentSettings]:
    env = os.getenv("ENV", "development")
    if env == "development":
        return DevelopmentSettings()
    elif env == "production":
        return ProductionSettings()
    else:
        raise ValueError(f"Unknown environment: {env}")


settings: Union[ProductionSettings, DevelopmentSettings] = get_settings()
__all__ = ["settings", "APP_DIR", "ROOT_DIR", "ENV_FILE_PATH"]
