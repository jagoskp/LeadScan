from typing import Any

from fastapi import HTTPException, status


def validate_credentials_format(creds: dict[str, Any]) -> None:
    """Ensure integration authentication credentials contain required keys."""
    if "encrypted_token" not in creds or not creds["encrypted_token"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing token credentials details",
        )
