import re


def validate_email_format(email: str) -> bool:
    """Ensure email matches basic format criteria."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))


def validate_phone_format(phone: str) -> bool:
    """Ensure phone contains only E.164 pattern elements."""
    pattern = r"^\+?[1-9]\d{1,14}$"
    return bool(re.match(pattern, phone))


def validate_website_format(url: str) -> bool:
    """Ensure website starts with protocol prefixes."""
    pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}.*$"
    return bool(re.match(pattern, url))


def validate_gst_format(gst: str) -> bool:
    """Ensure GST matches standard format (15 digits/uppercase)."""
    pattern = r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$"
    return bool(re.match(pattern, gst))
