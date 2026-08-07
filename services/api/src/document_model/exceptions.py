from fastapi import HTTPException, status


class DOMEngineException(HTTPException):
    """Base exception for all DOM engine errors."""
    pass


class DocumentNotFoundException(DOMEngineException):
    """Exception raised when a DOM Document is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DOM Document not found",
        )


class SectionNotFoundException(DOMEngineException):
    """Exception raised when a requested DocumentSection is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document section not found",
        )


class EntityNotFoundException(DOMEngineException):
    """Exception raised when a requested DOM Entity node is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DOM Entity not found",
        )


class AttributeValidationException(DOMEngineException):
    """Exception raised when format normalization or check fails."""

    def __init__(self, detail: str = "Attribute validation failed") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
