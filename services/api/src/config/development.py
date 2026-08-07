from services.api.src.config.base import BaseAppSettings


class DevelopmentSettings(BaseAppSettings):
    """Configuration overrides for the local development environment."""

    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
