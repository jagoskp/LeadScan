from fastapi import HTTPException, status


class ReportModuleException(HTTPException):
    """Base exception for all Reporting & Analytics module errors."""

    pass


class ReportNotFoundException(ReportModuleException):
    """Raised when a requested completed report does not exist."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )


class ReportJobNotFoundException(ReportModuleException):
    """Raised when a requested report generation job does not exist."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report job not found",
        )


class InvalidReportStateException(ReportModuleException):
    """Raised when an operation is performed on an invalid report state."""

    def __init__(self, detail: str = "Invalid report state transition") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
