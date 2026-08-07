from fastapi import HTTPException, status


class WorkerException(HTTPException):
    """Base exception for all Background Worker components."""

    pass


class TaskDispatchException(WorkerException):
    """Raised when task dispatching fails."""

    def __init__(self, detail: str = "Failed to dispatch task") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class TaskRegistrationException(WorkerException):
    """Raised when a task is registered with conflicts or is missing."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class BrokerConnectionException(WorkerException):
    """Raised when the message broker connection fails."""

    def __init__(self, detail: str = "Broker connection unavailable") -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
        )
