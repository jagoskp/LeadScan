from fastapi import HTTPException, status


class SecretVaultException(HTTPException):
    """Base exception for all secret vault errors."""
    pass


class SecretNotFoundException(SecretVaultException):
    """Raised when a requested secret does not exist in the vault."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Secret not found in the vault",
        )


class SecretAccessDeniedException(SecretVaultException):
    """Raised when a requester lacks the required role for a secret."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied — insufficient vault permission",
        )


class SecretExpiredException(SecretVaultException):
    """Raised when an expired secret is accessed."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_410_GONE,
            detail="Secret has expired and is no longer accessible",
        )


class SecretRotationFailedException(SecretVaultException):
    """Raised when a rotation attempt encounters an unrecoverable error."""

    def __init__(self, detail: str = "Secret rotation failed") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
