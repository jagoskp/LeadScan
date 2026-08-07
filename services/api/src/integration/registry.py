from typing import Any, Type
from services.api.src.integration.interfaces import (
    IAuthService,
    IUserService,
    IOrganizationService,
    IDocumentService,
    IOCRService,
    IAIService,
    IWorkflowService,
    ISearchService,
    IReportService,
    INotificationService,
    IAuditService,
    IStorageService,
)
from services.api.src.integration.exceptions import ServiceNotRegisteredException


class ServiceRegistry:
    """Registry managing interface-to-implementation bindings."""

    _registry: dict[Type[Any], Any] = {}

    @classmethod
    def register(cls, interface: Type[Any], implementation: Any) -> None:
        """Bind a concrete implementation instance to an interface class type."""
        cls._registry[interface] = implementation

    @classmethod
    def get(cls, interface: Any) -> Any:
        """Retrieve the registered implementation instance."""
        if interface not in cls._registry:
            raise ServiceNotRegisteredException(interface.__name__)
        return cls._registry[interface]

    @classmethod
    def clear(cls) -> None:
        """Clear all active registrations."""
        cls._registry.clear()

    @classmethod
    def get_bindings(cls) -> dict[str, str]:
        """List all active bindings as name strings."""
        return {
            interface.__name__: implementation.__class__.__name__
            for interface, implementation in cls._registry.items()
        }
