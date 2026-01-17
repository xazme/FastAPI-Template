import os
from typing import Type
from .config import Config
from .components import ComponentsConfig

ENV = os.getenv("ENV", "development")


class DevelopmentSettings(Config, ComponentsConfig):
    pass


class ProductionSettings(Config, ComponentsConfig):
    pass


class SettingsFactory:
    @staticmethod
    def get_settings():
        mapping: dict[str, Type[DevelopmentSettings] | Type[ProductionSettings]] = {
            "development": DevelopmentSettings,
            "production": ProductionSettings,
        }
        config_class = mapping.get(ENV, DevelopmentSettings)
        return config_class()


settings = SettingsFactory().get_settings()
