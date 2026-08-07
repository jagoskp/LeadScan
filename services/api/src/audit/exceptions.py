from fastapi import HTTPException, status


class AuditModuleException(HTTPException):
    """Base exception for all Audit & Activity tracking modules."""

    pass


class AuditLogNotFoundException(AuditModuleException):
    """Raised when an audit, activity, or security log cannot be found."""

    def __init__(self, detail: str = "Audit log not found") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class AdminAccessRequiredException(AuditModuleException):
    """Raised when non-administrators attempt to read organization-wide audit logs."""

    def __init__(self, detail: str = "Administrator access is required") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class InvalidEventValidationException(AuditModuleException):
    """Raised when validation check of event context fails."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
