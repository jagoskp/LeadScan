from fastapi import HTTPException, status


class SyncEngineException(HTTPException):
    """Base exception for all sync engine errors."""
    pass


class ConnectorNotFoundException(SyncEngineException):
    """Exception raised when a requested Connector profile is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target connector not found",
        )


class SyncJobNotFoundException(SyncEngineException):
    """Exception raised when a requested SyncJob is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sync job not found",
        )


class AuthenticationFailedException(SyncEngineException):
    """Exception raised when credential handshake with target integrations fail."""

    def __init__(self, detail: str = "Integration auth handshake failed") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class RateLimitExceededException(SyncEngineException):
    """Exception raised when target connectors rate limit requests."""

    def __init__(self, detail: str = "Target connector rate limit exceeded") -> None:
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
        )
