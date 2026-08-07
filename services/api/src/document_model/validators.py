import re

from services.api.src.document_model.exceptions import (
    AttributeValidationException,
)

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
PHONE_REGEX = re.compile(r"^\+?1?\d{9,15}$")
GST_REGEX = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$")


def validate_email_format(email: str) -> None:
    """Validate email format."""
    if not EMAIL_REGEX.match(email):
        raise AttributeValidationException(
            f"Invalid email address format: '{email}'"
        )


def validate_phone_format(phone: str) -> None:
    """Validate phone format."""
    cleaned = phone.replace(" ", "").replace("-", "")
    if not PHONE_REGEX.match(cleaned):
        raise AttributeValidationException(f"Invalid phone number format: '{phone}'")


def validate_gst_format(gst: str) -> None:
    """Validate GST format."""
    if not GST_REGEX.match(gst):
        raise AttributeValidationException(f"Invalid GST number format: '{gst}'")
