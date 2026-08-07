import re
from typing import Any

from services.api.src.scanner.enums import ScanSource
from services.api.src.scanner.exceptions import (
    InvalidScanSourceException,
    ManualReviewValidationException,
)


def validate_bounding_box(bounding_box: dict[str, Any] | None) -> None:
    """Validate bounding box coordinates.

    Expected keys: 'x', 'y', 'width', 'height' as floats normalized between 0.0 and 1.0.
    """
    if not bounding_box:
        return

    required_keys = {"x", "y", "width", "height"}
    if not required_keys.issubset(bounding_box.keys()):
        raise ManualReviewValidationException(
            "Bounding box must contain 'x', 'y', 'width', and 'height' keys"
        )

    for key in required_keys:
        val = bounding_box[key]
        if not isinstance(val, (int, float)):
            raise ManualReviewValidationException(
                f"Bounding box coordinate '{key}' must be a number"
            )
        if not (0.0 <= float(val) <= 1.0):
            raise ManualReviewValidationException(
                f"Bounding box coordinate '{key}' "
                "must be normalized between 0.0 and 1.0"
            )


def validate_confidence(confidence: float | None) -> None:
    """Validate confidence score bounds (0.0 to 1.0)."""
    if confidence is None:
        return

    if not isinstance(confidence, (int, float)):
        raise ManualReviewValidationException("Confidence score must be a number")

    if not (0.0 <= float(confidence) <= 1.0):
        raise ManualReviewValidationException(
            "Confidence score must be between 0.0 and 1.0"
        )


def validate_scan_source(source: str) -> None:
    """Validate that the given source string is a registered ScanSource enum value."""
    try:
        ScanSource(source)
    except ValueError as err:
        raise InvalidScanSourceException(
            f"Unsupported scan source type: '{source}'"
        ) from err


def validate_email_format(email: str | None) -> bool:
    """Validate email format using a standard regular expression helper."""
    if not email:
        return False
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(email_regex, email))


def validate_phone_format(phone: str | None) -> bool:
    """Validate phone format to ensure it contains only digits, +, -, and spaces."""
    if not phone:
        return False
    phone_regex = r"^\+?[0-9\s\-]+$"
    return bool(re.match(phone_regex, phone))
