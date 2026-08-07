from enum import StrEnum


class ConnectorHealthStatus(StrEnum):
    """Health monitor status codes for third-party connections."""

    HEALTHY = "Healthy"
    WARNING = "Warning"
    DISCONNECTED = "Disconnected"
    EXPIRED = "Expired"
    AUTHENTICATION_FAILED = "Authentication Failed"
    RATE_LIMITED = "Rate Limited"
    MAINTENANCE = "Maintenance"


class ConnectorPermissionType(StrEnum):
    """User access permission rights for target connectors configurations."""

    READ = "Read"
    WRITE = "Write"
    ADMIN = "Admin"
