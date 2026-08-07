from fastapi import HTTPException, status


class ConnectorStudioException(HTTPException):
    """Base exception for all connector studio errors."""
    pass


class ConnectorConnectionNotFoundException(ConnectorStudioException):
    """Exception raised when a requested Connection link is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector connection not found",
        )


class ConnectorPermissionDeniedException(ConnectorStudioException):
    """Exception raised when user does not have permission for the connector."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied for target connection configuration",
        )


class InvalidAuthCodeException(ConnectorStudioException):
    """Exception raised when an invalid authorization code is provided."""

    def __init__(self, detail: str = "Invalid OAuth code validation") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
