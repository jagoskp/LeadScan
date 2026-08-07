class GoogleConnectorException(Exception):
    """Base exception for Google Sheets Connector errors."""

    def __init__(self, message: str, code: str = "GOOGLE_CONNECTOR_ERROR", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class GoogleAuthException(GoogleConnectorException):
    """Raised on authentication or token refresh failures."""

    def __init__(self, message: str = "Google OAuth authentication failed"):
        super().__init__(message, code="GOOGLE_AUTH_FAILURE", status_code=401)


class GooglePermissionDeniedException(GoogleConnectorException):
    """Raised when access permissions to spreadsheet or Drive are insufficient."""

    def __init__(self, message: str = "Insufficient permissions for Google Sheet resource"):
        super().__init__(message, code="GOOGLE_PERMISSION_DENIED", status_code=403)


class GoogleRateLimitException(GoogleConnectorException):
    """Raised when Google API quota/rate limit is exceeded."""

    def __init__(self, message: str = "Google Sheets API rate limit exceeded"):
        super().__init__(message, code="GOOGLE_RATE_LIMIT_EXCEEDED", status_code=429)


class SpreadsheetNotFoundException(GoogleConnectorException):
    """Raised when requested spreadsheet is not found."""

    def __init__(self, spreadsheet_id: str):
        super().__init__(
            f"Spreadsheet '{spreadsheet_id}' not found",
            code="SPREADSHEET_NOT_FOUND",
            status_code=404,
        )


class WorksheetNotFoundException(GoogleConnectorException):
    """Raised when requested worksheet title or ID is not found."""

    def __init__(self, worksheet_title: str):
        super().__init__(
            f"Worksheet '{worksheet_title}' not found in spreadsheet",
            code="WORKSHEET_NOT_FOUND",
            status_code=404,
        )


class MappingValidationException(GoogleConnectorException):
    """Raised when pre-sync header mapping validation fails."""

    def __init__(self, message: str, report_details: dict | None = None):
        super().__init__(message, code="MAPPING_VALIDATION_FAILURE", status_code=422)
        self.report_details = report_details or {}
