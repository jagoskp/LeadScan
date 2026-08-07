from services.api.src.config.base import BaseAppSettings


class TestingSettings(BaseAppSettings):
    """Configuration overrides for testing environments, using separated DBs."""

    APP_ENV: str = "testing"
    DEBUG: bool = True
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/leadscan_test"
    )
    LOG_LEVEL: str = "WARNING"
