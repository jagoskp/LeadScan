from fastapi import HTTPException, status


class NotificationModuleException(HTTPException):
    """Base exception for all Notification management modules."""

    pass


class NotificationNotFoundException(NotificationModuleException):
    """Raised when a specific notification cannot be found or accessed."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )


class TemplateNotFoundException(NotificationModuleException):
    """Raised when a notification template cannot be found."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification template not found",
        )


class PreferenceNotFoundException(NotificationModuleException):
    """Raised when notification preferences cannot be found."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification preferences not found",
        )


class PreferenceDisabledException(NotificationModuleException):
    """Raised when attempting to send a notification via a disabled channel."""

    def __init__(self, channel: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Notification channel '{channel}' is disabled by user preferences",
        )


class TemplateValidationException(NotificationModuleException):
    """Raised when template rendering fails due to missing or invalid variables."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class InvalidRecipientException(NotificationModuleException):
    """Raised when the recipient's format is invalid for the specified channel."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
