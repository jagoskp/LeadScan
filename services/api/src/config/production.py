from pydantic import model_validator

from services.api.src.config.base import BaseAppSettings
from services.api.src.config.validators import validate_jwt_secret_strength


class ProductionSettings(BaseAppSettings):
    """Configuration settings for production, enforcing strict secrets validation."""

    APP_ENV: str = "production"
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "ProductionSettings":
        """Enforce strict validations over secrets in production."""
        validate_jwt_secret_strength(self.JWT_SECRET_KEY, self.APP_ENV)
        return self
