class LeadRepositoryException(Exception):
    """Base exception for Enterprise Lead Repository errors."""

    def __init__(self, message: str, code: str = "LEAD_REPOSITORY_ERROR", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class LeadNotFoundException(LeadRepositoryException):
    """Raised when a requested Lead record is not found."""

    def __init__(self, lead_id: str):
        super().__init__(f"Lead '{lead_id}' not found", code="LEAD_NOT_FOUND", status_code=404)


class LeadAlreadyArchivedException(LeadRepositoryException):
    """Raised when operating on an archived lead."""

    def __init__(self, lead_id: str):
        super().__init__(f"Lead '{lead_id}' is archived", code="LEAD_ALREADY_ARCHIVED", status_code=422)


class LeadMergeException(LeadRepositoryException):
    """Raised when lead merging validation fails."""

    def __init__(self, message: str):
        super().__init__(message, code="LEAD_MERGE_FAILURE", status_code=400)


class InvalidLeadStatusException(LeadRepositoryException):
    """Raised when an invalid status transition is requested."""

    def __init__(self, status: str):
        super().__init__(f"Invalid lead status '{status}'", code="INVALID_LEAD_STATUS", status_code=422)
