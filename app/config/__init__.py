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
    """
    Factory function to retrieve the appropriate settings instance based on the environment.

    This function reads the 'ENV' environment variable to determine which configuration
    to load. By default, it returns DevelopmentSettings if the ENV variable is not set.
    Supported environments are 'development' and 'production'. Raises a ValueError for
    any unknown environment value.

    Returns:
        Union[ProductionSettings, DevelopmentSettings]: An instance of the settings class
        corresponding to the current environment.

    Environment Variables:
        ENV (str): Specifies the current environment. Valid values are:
            - "development" (default): Loads DevelopmentSettings.
            - "production": Loads ProductionSettings.

    Example:
        >>> settings = get_settings()
        >>> print(settings.env)
        'development'

    Note:
        The function prints the current environment value for debugging purposes.
        Ensure that the appropriate settings classes (DevelopmentSettings, ProductionSettings)
        are defined and inherit from BaseConfig or a similar settings base.
    """
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
