from fastapi import HTTPException, status


class AIUnderstandingException(HTTPException):
    """Base exception for all AI understanding module errors."""
    pass


class UnderstandingJobNotFoundException(AIUnderstandingException):
    """Exception raised when an AI understanding job is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI understanding job not found",
        )


class EntityNotFoundException(AIUnderstandingException):
    """Exception raised when a requested semantic entity is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detected entity not found",
        )


class InvalidDocumentTypeException(AIUnderstandingException):
    """Exception raised when a document type is invalid."""

    def __init__(self, doc_type: str = "document type") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or unsupported document classification: '{doc_type}'",
        )


class AIProviderException(AIUnderstandingException):
    """Exception raised when an AI / LLM provider fails."""

    def __init__(
        self, provider: str = "AI Provider", detail: str = "Unknown error"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI understanding execution via {provider} failed: {detail}",
        )
