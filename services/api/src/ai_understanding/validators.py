from services.api.src.ai_understanding.enums import AIDocumentType
from services.api.src.ai_understanding.exceptions import (
    InvalidDocumentTypeException,
)


def validate_document_type(document_type: str) -> None:
    """Ensure that the target document type matches supported classifications."""
    try:
        AIDocumentType(document_type)
    except ValueError:
        raise InvalidDocumentTypeException(document_type) from None


def validate_confidence_score(confidence: float) -> None:
    """Ensure confidence boundaries fall within [0.0, 1.0]."""
    if not (0.0 <= confidence <= 1.0):
        raise ValueError("Confidence score must fall within 0.0 and 1.0 limits")
