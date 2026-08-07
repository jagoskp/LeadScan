class WorkspacePlatformException(Exception):
    """Base exception for Enterprise Multi-Workspace Platform errors."""

    def __init__(self, message: str, code: str = "WORKSPACE_ERROR", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class OrganizationNotFoundException(WorkspacePlatformException):
    """Raised when an Organization is not found."""

    def __init__(self, org_id: str):
        super().__init__(f"Organization '{org_id}' not found", code="ORGANIZATION_NOT_FOUND", status_code=404)


class WorkspaceNotFoundException(WorkspacePlatformException):
    """Raised when a Workspace is not found."""

    def __init__(self, workspace_id: str):
        super().__init__(f"Workspace '{workspace_id}' not found", code="WORKSPACE_NOT_FOUND", status_code=404)


class AccessDeniedException(WorkspacePlatformException):
    """Raised when RBAC permission check fails."""

    def __init__(self, action: str):
        super().__init__(f"Access denied for action '{action}'", code="ACCESS_DENIED", status_code=403)


class InvitationExpiredException(WorkspacePlatformException):
    """Raised when an email invitation token has expired."""

    def __init__(self, token: str):
        super().__init__(f"Invitation token '{token}' has expired or is invalid", code="INVITATION_EXPIRED", status_code=410)
