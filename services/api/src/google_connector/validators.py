import re
from typing import Any
from services.api.src.google_connector.exceptions import MappingValidationException


def validate_spreadsheet_id(spreadsheet_id: str) -> str:
    """Validate Google Spreadsheet ID format."""
    if not spreadsheet_id or not isinstance(spreadsheet_id, str):
        raise ValueError("Invalid spreadsheet ID: must be a non-empty string.")
    
    cleaned = spreadsheet_id.strip()
    # Match standard Google Drive file/spreadsheet ID pattern (alphanumeric, hyphens, underscores)
    if not re.match(r"^[a-zA-Z0-9-_]{20,100}$", cleaned):
        # Extract from full Google Sheets URL if user pasted a link
        match = re.search(r"/d/([a-zA-Z0-9-_]+)", cleaned)
        if match:
            return match.group(1)
        raise ValueError(f"Invalid Google Spreadsheet ID format: '{spreadsheet_id}'")
    return cleaned


def validate_worksheet_title(title: str) -> str:
    """Validate worksheet title."""
    if not title or not isinstance(title, str):
        raise ValueError("Worksheet title cannot be empty.")
    cleaned = title.strip()
    if len(cleaned) > 100:
        raise ValueError("Worksheet title exceeds maximum allowed length of 100 characters.")
    return cleaned


def validate_sync_payload(headers: list[str], rows: list[dict[str, Any]]) -> None:
    """Ensure rows conform to expected non-empty payload rules."""
    if not rows:
        raise MappingValidationException("Sync payload contains 0 rows to synchronize.")
    if not headers:
        raise MappingValidationException("Worksheet has no column headers defined.")
