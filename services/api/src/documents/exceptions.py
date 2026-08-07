from fastapi import HTTPException, status


class DocumentModuleException(HTTPException):
    """Base exception for all Document management module errors."""

    pass


class DocumentNotFoundException(DocumentModuleException):
    """Raised when a requested document does not exist."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )


class DocumentAlreadyArchivedException(DocumentModuleException):
    """Raised when trying to archive an already archived document."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document is already archived",
        )


class DocumentNotArchivedException(DocumentModuleException):
    """Raised when trying to restore a document that is not archived."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document is not archived",
        )
