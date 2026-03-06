from .components import ComponentsConfig
from .config import Config


class ApplicationSettings(Config, ComponentsConfig): ...


settings = ApplicationSettings()

__all__ = [
    "settings",
]
