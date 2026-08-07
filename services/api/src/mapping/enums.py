from enum import StrEnum


class MappingTargetType(StrEnum):
    """Supported target systems for data export."""

    GOOGLE_SHEETS = "Google Sheets"
    EXCEL = "Excel"
    CSV = "CSV"
    JSON = "JSON"
    CRM = "CRM"
    DATABASE = "Database"
    REST_API = "REST API"
    WEBHOOK = "Webhook"


class MappingFieldType(StrEnum):
    """Predefined field types supported by the mapping engine."""

    TEXT = "Text"
    NUMBER = "Number"
    EMAIL = "Email"
    PHONE = "Phone"
    WEBSITE = "Website"
    DATE = "Date"
    TIME = "Time"
    BOOLEAN = "Boolean"
    CURRENCY = "Currency"
    ADDRESS = "Address"
    MULTI_VALUE = "Multi Value"
    OBJECT = "Object"
    ARRAY = "Array"
    CUSTOM = "Custom Type"


class TransformationType(StrEnum):
    """String and format manipulation rules."""

    TRIM = "Trim"
    UPPERCASE = "Uppercase"
    LOWERCASE = "Lowercase"
    REPLACE = "Replace"
    REGEX = "Regex"
    SPLIT = "Split"
    MERGE = "Merge"
    JOIN = "Join"
    PHONE_NORMALIZE = "Phone Normalize"
    EMAIL_NORMALIZE = "Email Normalize"
    DATE_NORMALIZE = "Date Normalize"


class ValidationRuleType(StrEnum):
    """Data validation rules applied during mapping."""

    REQUIRED = "Required"
    UNIQUE = "Unique"
    LENGTH = "Length"
    REGEX = "Regex"
    MIN = "Min"
    MAX = "Max"
    CUSTOM = "Custom Validation"
