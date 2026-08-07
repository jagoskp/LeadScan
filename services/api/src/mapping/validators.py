import re


def validate_required_field(field_name: str, value: str | None) -> str | None:
    """Check if the field is present and non-empty."""
    if value is None or len(value.strip()) == 0:
        return f"Field '{field_name}' is required but was empty"
    return None


def validate_field_length(
    field_name: str, value: str, min_len: int | None, max_len: int | None
) -> str | None:
    """Check if the field length falls within min and max boundaries."""
    val_len = len(value)
    if min_len is not None and val_len < min_len:
        return (
            f"Field '{field_name}' length ({val_len}) "
            f"is below minimum limit ({min_len})"
        )
    if max_len is not None and val_len > max_len:
        return (
            f"Field '{field_name}' length ({val_len}) "
            f"is above maximum limit ({max_len})"
        )
    return None


def validate_field_regex(
    field_name: str, value: str, pattern: str
) -> str | None:
    """Validate if the string matches the regex format."""
    try:
        if not re.match(pattern, value):
            return (
                f"Field '{field_name}' value '{value}' "
                f"does not match format regex"
            )
    except re.error:
        return (
            f"Invalid configuration regex format check "
            f"for field '{field_name}'"
        )
    return None
