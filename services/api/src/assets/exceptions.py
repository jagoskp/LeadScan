class AssetException(Exception):
    """Base exception for Enterprise Digital Asset Management errors."""

    def __init__(self, message: str, code: str = "ASSET_ERROR", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class AssetNotFoundException(AssetException):
    """Raised when an Asset record or file is not found."""

    def __init__(self, asset_id: str):
        super().__init__(f"Asset '{asset_id}' not found", code="ASSET_NOT_FOUND", status_code=404)


class ImmutableAssetModificationException(AssetException):
    """Raised when an attempt is made to overwrite or modify an immutable original asset."""

    def __init__(self, asset_id: str):
        super().__init__(
            f"Asset '{asset_id}' is immutable (Original Scan Image) and cannot be modified or overwritten",
            code="IMMUTABLE_ASSET_MODIFICATION_FORBIDDEN",
            status_code=422,
        )


class AssetIntegrityException(AssetException):
    """Raised when asset checksum validation fails or file is corrupted."""

    def __init__(self, asset_id: str, detail: str):
        super().__init__(
            f"Integrity check failed for asset '{asset_id}': {detail}",
            code="ASSET_INTEGRITY_FAILURE",
            status_code=422,
        )
