import re
from services.api.src.assets.exceptions import AssetException

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "application/pdf",
}


def validate_asset_upload(file_name: str, mime_type: str, file_bytes: bytes) -> tuple[str, str]:
    """Validate asset file upload inputs."""
    if not file_name or len(file_name.strip()) == 0:
        raise AssetException("Asset file name cannot be empty.")
    
    if mime_type.lower() not in ALLOWED_MIME_TYPES:
        raise AssetException(f"Unsupported MIME type '{mime_type}'. Supported types: {', '.join(ALLOWED_MIME_TYPES)}")

    if len(file_bytes) == 0:
        raise AssetException("Uploaded file payload is empty (0 bytes).")

    return file_name.strip(), mime_type.lower()
