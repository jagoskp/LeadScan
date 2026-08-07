from enum import StrEnum


class ReviewApprovalStatus(StrEnum):
    """Approval status states for review sessions and items."""

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class ConfidenceLevel(StrEnum):
    """OCR/AI extraction confidence thresholds."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ValidationIssueType(StrEnum):
    """Identified database field formatting validation errors."""

    REQUIRED_FIELD_MISSING = "Required Field Missing"
    DUPLICATE_VALUE = "Duplicate Value"
    INVALID_EMAIL = "Invalid Email"
    INVALID_PHONE = "Invalid Phone"
    INVALID_WEBSITE = "Invalid Website"
    INVALID_GST = "Invalid GST"
