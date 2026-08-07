from fastapi import HTTPException, status


class MonitoringModuleException(HTTPException):
    """Base exception for all Monitoring and Diagnostics layers."""

    pass


class DependencyUnavailableException(MonitoringModuleException):
    """Raised when critical service checks (e.g. Postgres, Redis) fail."""

    def __init__(self, detail: str = "Critical dependencies unavailable") -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
        )
