from fastapi import HTTPException, status


class AIModuleException(HTTPException):
    """Base exception for all AI analysis module errors."""

    pass


class AIJobNotFoundException(AIModuleException):
    """Raised when a requested AI job does not exist."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI job not found",
        )


class AIJobNotCancellableException(AIModuleException):
    """Raised when trying to cancel a job that is already completed or cancelled."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "AI job is not in a cancellable state "
                "(must be PENDING, QUEUED, or RUNNING)"
            ),
        )


class AIJobNotRetriableException(AIModuleException):
    """Raised when trying to retry a job that is not failed or cancelled."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "AI job is not in a retriable state " "(must be FAILED or CANCELLED)"
            ),
        )


class OCRResultNotFoundException(AIModuleException):
    """Raised when an associated OCR result does not exist."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated OCR result not found",
        )
