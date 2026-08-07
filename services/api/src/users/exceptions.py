from fastapi import HTTPException, status


class UserModuleException(HTTPException):
    """Base exception for all User management modules."""
    pass


class ProfileNotFoundException(UserModuleException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found",
        )


class InvalidPasswordException(UserModuleException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password verification failed",
        )


class PasswordsMatchException(UserModuleException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from your current password",
        )
