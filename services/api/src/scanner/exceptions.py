from fastapi import HTTPException, status


class ScannerModuleException(HTTPException):
    """Base exception for all Scanner module errors."""
    pass


class ScanJobNotFoundException(ScannerModuleException):
    """Exception raised when a requested scan job cannot be found in the database."""
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan job not found",
        )


class ScanResultNotFoundException(ScannerModuleException):
    """Exception raised when the scan result cannot be found."""
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan result not found",
        )


class DetectedFieldNotFoundException(ScannerModuleException):
    """Exception raised when a specific detected metadata field is not found."""
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detected field not found",
        )


class InvalidScanSourceException(ScannerModuleException):
    """Exception raised when an unsupported or invalid scan source type is supplied."""
    def __init__(self, detail: str = "Invalid scan source type provided") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class ManualReviewValidationException(ScannerModuleException):
    """Exception raised when manual review actions fail constraints.

    For example, invalid bounding box coordinates.
    """
    def __init__(
        self, detail: str = "Validation failed for manual review action"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
