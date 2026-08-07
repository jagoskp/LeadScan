from enum import StrEnum


class SecretType(StrEnum):
    """Supported secret value types stored in the vault."""

    GOOGLE_OAUTH_TOKEN = "Google OAuth Token"
    REFRESH_TOKEN = "Refresh Token"
    ACCESS_TOKEN = "Access Token"
    API_KEY = "API Key"
    API_SECRET = "API Secret"
    WEBHOOK_SECRET = "Webhook Secret"
    DB_PASSWORD = "Database Password"
    SMTP_CREDENTIALS = "SMTP Credentials"
    CUSTOM = "Custom"


class SecretStatus(StrEnum):
    """Lifecycle status of a vault secret."""

    ACTIVE = "Active"
    ARCHIVED = "Archived"
    DISABLED = "Disabled"
    EXPIRED = "Expired"
    ROTATED = "Rotated"


class SecretAccessRole(StrEnum):
    """Access permission roles scoped to individual secrets."""

    OWNER = "Owner"
    ADMIN = "Admin"
    EDITOR = "Editor"
    VIEWER = "Viewer"
    READ_ONLY = "Read Only"
    CONNECTOR_ACCESS = "Connector Access"
    SCOPED_ACCESS = "Scoped Access"


class AuditAction(StrEnum):
    """Actions tracked in the secret audit trail."""

    CREATE = "Create"
    READ = "Read"
    UPDATE = "Update"
    DELETE = "Delete"
    ROTATE = "Rotate"
    ARCHIVE = "Archive"
    RECOVER = "Recover"
    DISABLE = "Disable"
    ENABLE = "Enable"
    ACCESS_ATTEMPT = "Access Attempt"
    ROTATION_FAILURE = "Rotation Failure"
