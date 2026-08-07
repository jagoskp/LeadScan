from fastapi import HTTPException, status


class StorageModuleException(HTTPException):
    """Base exception for all Storage Management modules."""

    pass


class ProviderNotFoundException(StorageModuleException):
    """Raised when a specified storage provider cannot be found."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Storage provider not found",
        )


class FileNotFoundException(StorageModuleException):
    """Raised when a specific file metadata record cannot be found."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File metadata not found",
        )


class QuotaExceededException(StorageModuleException):
    """Raised when file registration violates the organization quota limit."""

    def __init__(self, detail: str = "Storage quota limit exceeded") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class QuotaNotFoundException(StorageModuleException):
    """Raised when an organization quota profile cannot be found."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Storage quota profile not found",
        )
