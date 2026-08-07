from typing import Any

from fastapi import HTTPException, status


def validate_connection_config(config: dict[str, Any]) -> None:
    """Ensure connector studio configuration contains valid keys."""
    if "api_endpoint" in config and not config["api_endpoint"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Configuration endpoint path is invalid",
        )
