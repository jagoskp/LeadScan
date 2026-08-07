from enum import StrEnum


class AIDocumentType(StrEnum):
    """Predefined document classification categories."""

    VISITING_CARD = "Visiting Card"
    BUSINESS_CARD = "Business Card"
    A4_DOCUMENT = "A4 Document"
    INVOICE = "Invoice"
    RECEIPT = "Receipt"
    FLYER = "Flyer"
    POSTER = "Poster"
    BANNER = "Banner"
    BILLBOARD = "Billboard"
    SHOP_BOARD = "Shop Board"
    CERTIFICATE = "Certificate"
    LETTER = "Letter"
    MOBILE_SCREEN = "Mobile Screen"
    LAPTOP_SCREEN = "Laptop Screen"
    SCREENSHOT = "Screenshot"
    UNKNOWN = "Unknown Document"


class AIEntityType(StrEnum):
    """Standardized entity classifications for structural elements."""

    PERSON = "Person"
    COMPANY = "Company"
    BUSINESS = "Business"
    PHONE = "Phone"
    EMAIL = "Email"
    WEBSITE = "Website"
    GST = "GST"
    ADDRESS = "Address"
    PIN = "PIN"
    CITY = "City"
    STATE = "State"
    COUNTRY = "Country"
    DEPARTMENT = "Department"
    DESIGNATION = "Designation"
    SOCIAL_MEDIA = "Social Media"
    QR_REFERENCE = "QR Reference"
    BARCODE_REFERENCE = "Barcode Reference"
    DATE = "Date"
    TIME = "Time"
    AMOUNT = "Amount"
    CURRENCY = "Currency"
    CUSTOM = "Custom Entity"


class AIProviderType(StrEnum):
    """Supported third-party AI/LLM providers."""

    OPENAI = "OpenAI"
    AZURE_OPENAI = "Azure OpenAI"
    CLAUDE = "Claude"
    GEMINI = "Gemini"
    LOCAL_LLM = "Local LLM"
    CUSTOM_AI = "Custom AI"


class AIJobStatus(StrEnum):
    """Tracking statuses of the AI semantic analysis process."""

    PENDING = "PENDING"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
