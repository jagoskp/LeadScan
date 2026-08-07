from services.api.src.config.base import BaseAppSettings


class StagingSettings(BaseAppSettings):
    """Configuration overrides for pre-release staging environments."""

    APP_ENV: str = "staging"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
