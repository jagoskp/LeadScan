import os

from services.api.src.config.base import BaseAppSettings
from services.api.src.config.development import DevelopmentSettings
from services.api.src.config.production import ProductionSettings
from services.api.src.config.staging import StagingSettings
from services.api.src.config.testing import TestingSettings


def get_settings() -> BaseAppSettings:
    """Resolve and instantiate settings matching active APP_ENV."""
    env = os.environ.get("APP_ENV", "development").lower()

    config_classes = {
        "development": DevelopmentSettings,
        "testing": TestingSettings,
        "staging": StagingSettings,
        "production": ProductionSettings,
    }

    settings_class = config_classes.get(env, DevelopmentSettings)

    # Determine env file targets (.env.development, .env.testing, etc.)
    env_file = f".env.{env}"
    if not os.path.exists(env_file):
        # Fallback to root .env config file
        env_file = ".env"

    return settings_class(
        _env_file=env_file,
        _env_file_encoding="utf-8",
    )  # type: ignore[call-arg]
