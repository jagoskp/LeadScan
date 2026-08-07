from datetime import UTC, datetime

from fastapi import HTTPException, status

from services.api.src.secret_vault.enums import SecretStatus


def validate_secret_not_expired(
    status_value: str, expires_at: datetime | None
) -> None:
    """Raise 410 if the secret is expired or in a non-active status."""
    if status_value == SecretStatus.EXPIRED:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Secret has expired",
        )
    if expires_at and expires_at < datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Secret TTL has passed — it is expired",
        )


def validate_policy_config(
    rotation_interval_days: int, max_versions: int
) -> None:
    """Validate rotation interval and version retention bounds."""
    if rotation_interval_days < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rotation interval must be at least 1 day",
        )
    if max_versions < 1 or max_versions > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Max versions must be between 1 and 100",
        )
