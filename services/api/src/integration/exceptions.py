from fastapi import HTTPException, status


class IntegrationModuleException(HTTPException):
    """Base exception for all Integration Layer modules."""

    pass


class ServiceNotRegisteredException(IntegrationModuleException):
    """Raised when an interface is requested but no implementation is registered."""

    def __init__(self, interface_name: str) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                f"Service implementation for interface "
                f"'{interface_name}' not registered"
            ),
        )
