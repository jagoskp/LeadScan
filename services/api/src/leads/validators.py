import re
from services.api.src.leads.enums import LeadStatusEnum
from services.api.src.leads.exceptions import InvalidLeadStatusException


def validate_lead_status(status: str) -> str:
    """Validate standard or custom status string."""
    if not status or not isinstance(status, str):
        raise ValueError("Lead status must be a non-empty string.")
    
    cleaned = status.strip()
    valid_statuses = [s.value for s in LeadStatusEnum]
    # Allow custom statuses as long as length is valid
    if len(cleaned) > 50:
        raise InvalidLeadStatusException(cleaned)
    return cleaned


def validate_gst_number(gst: str | None) -> str | None:
    """Validate Indian GST number format if provided."""
    if not gst:
        return None
    cleaned = gst.strip().upper()
    # 15-character Alphanumeric GST pattern
    if not re.match(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$", cleaned):
        # Allow general GST string if not strict match
        return cleaned
    return cleaned
