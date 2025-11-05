import os
from dotenv import load_dotenv
from typing import Union
from .components import ComponentsConfig
from .envs import DevelopmentConfig, ProductionConfig
from .constans import ENV_FILE_PATH

load_dotenv()


class ProductionSettings(ProductionConfig, ComponentsConfig): ...


class DevelopmentSettings(DevelopmentConfig, ComponentsConfig): ...


def get_settings() -> Union[ProductionSettings, DevelopmentSettings]:
    env = os.getenv("ENV", "development")  # using dev settings as default settings
    print(env)
    if env == "development":
        return DevelopmentSettings()
    elif env == "production":
        return ProductionSettings()
    else:
        raise ValueError(f"Unknown environment: {env}")


settings: Union[ProductionSettings, DevelopmentSettings] = get_settings()
__all__ = ["settings", "ENV_FILE_PATH"]
