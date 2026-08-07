from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from services.api.src.config.validators import (
    validate_database_url,
    validate_redis_url,
)


class BaseAppSettings(BaseSettings):
    """Parent application configuration containing base defaults."""

    APP_NAME: str = "LeadScan AI"
    APP_ENV: str = "development"
    DEBUG: bool = False

    # Database Configuration
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/leadscan_db"
    )
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery background workers broker and backend configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # JWT Authentication settings
    JWT_SECRET_KEY: str = "change_me_in_production_secret_key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Feature Flags
    ENABLE_OCR: bool = True
    ENABLE_AI_EXTRACTION: bool = True
    ENABLE_NOTIFICATIONS: bool = True
    ENABLE_AUDIT: bool = True

    @field_validator("DATABASE_URL")
    @classmethod
    def check_db_url(cls, v: str) -> str:
        """Validate database connection format."""
        return validate_database_url(v)

    @field_validator("REDIS_URL", "CELERY_BROKER_URL", "CELERY_RESULT_BACKEND")
    @classmethod
    def check_redis_url(cls, v: str) -> str:
        """Validate redis connections formats."""
        return validate_redis_url(v)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class SettingsConfigHelper:
    pass
