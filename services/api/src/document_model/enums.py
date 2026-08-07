from enum import StrEnum


class DOMDocumentType(StrEnum):
    """Predefined classification categories for DOM Documents."""

    VISITING_CARD = "Visiting Card"
    BUSINESS_CARD = "Business Card"
    A4_DOCUMENT = "A4 Document"
    INVOICE = "Invoice"
    RECEIPT = "Receipt"
    BANNER = "Banner"
    POSTER = "Poster"
    BILLBOARD = "Billboard"
    SHOP_BOARD = "Shop Board"
    CERTIFICATE = "Certificate"
    LETTER = "Letter"
    MOBILE_SCREEN = "Mobile Screen"
    LAPTOP_SCREEN = "Laptop Screen"
    SCREENSHOT = "Screenshot"
    UNKNOWN = "Unknown Document"


class DOMEntityType(StrEnum):
    """Standardized DOM Entity node types."""

    PERSON = "Person"
    COMPANY = "Company"
    BUSINESS = "Business"
    PHONE = "Phone"
    MOBILE = "Mobile"
    EMAIL = "Email"
    WEBSITE = "Website"
    GST = "GST"
    PAN = "PAN"
    ADDRESS = "Address"
    CITY = "City"
    STATE = "State"
    COUNTRY = "Country"
    PIN = "PIN"
    DEPARTMENT = "Department"
    DESIGNATION = "Designation"
    BUSINESS_CATEGORY = "Business Category"
    OPENING_HOURS = "Opening Hours"
    SOCIAL_LINKS = "Social Links"
    QR_REFERENCE = "QR Reference"
    BARCODE_REFERENCE = "Barcode Reference"
    AMOUNT = "Amount"
    CURRENCY = "Currency"
    DATE = "Date"
    TIME = "Time"
    CUSTOM = "Custom Entity"


class DOMEntitySource(StrEnum):
    """Origin source of the DOM Entity attribute entry."""

    OCR = "OCR"
    AI = "AI"
    USER = "User"


class DOMSectionType(StrEnum):
    """Document layout partition sections."""

    HEADER = "Header"
    BODY = "Body"
    FOOTER = "Footer"
    UNKNOWN = "Unknown"


class DOMRelationshipType(StrEnum):
    """Semantic mapping relationships between DOM Entities."""

    BELONGS_TO = "Belongs To"
    CONTAINS = "Contains"
    REFERENCES = "References"
    RELATED_TO = "Related To"
    PARENT = "Parent"
    CHILD = "Child"
    DUPLICATE_OF = "Duplicate Of"


class DOMReviewStatus(StrEnum):
    """State status for manual review workflows."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
