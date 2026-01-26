import os
import logging
from typing import Type
from .config import Config
from .components import ComponentsConfig

logger = logging.getLogger(__name__)


class DevelopmentSettings(Config, ComponentsConfig):
    pass


class ProductionSettings(Config, ComponentsConfig):
    pass


class TestingSettings(Config, ComponentsConfig):
    pass


ENV = os.getenv("ENV", "dev")


class SettingsFactory:
    @staticmethod
    def get_settings():
        mapping: dict[
            str,
            Type[DevelopmentSettings]
            | Type[ProductionSettings]
            | Type[TestingSettings],
        ] = {
            "dev": DevelopmentSettings,
            "prod": ProductionSettings,
            "test": TestingSettings,
        }
        config_class = mapping.get(ENV, DevelopmentSettings)
        return config_class()


def get_current_env() -> str:
    return ENV


settings = SettingsFactory().get_settings()
