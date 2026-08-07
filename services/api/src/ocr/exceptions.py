from fastapi import HTTPException, status


class OCRModuleException(HTTPException):
    """Base exception for all OCR processing module errors."""

    pass


class OCRJobNotFoundException(OCRModuleException):
    """Raised when a requested OCR job does not exist."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OCR job not found",
        )


class InvalidOCRStatusTransitionException(OCRModuleException):
    """Raised when an invalid status transition is requested."""

    def __init__(self, detail: str = "Invalid OCR status transition") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class OCRJobNotCancellableException(OCRModuleException):
    """Raised when trying to cancel a job that is already done/failed/cancelled."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "OCR job is not in a cancellable state "
                "(must be PENDING, QUEUED, or RUNNING)"
            ),
        )


class OCRJobNotRetriableException(OCRModuleException):
    """Raised when trying to retry a job that is not failed or cancelled."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OCR job is not in a retriable state (must be FAILED or CANCELLED)",
        )
