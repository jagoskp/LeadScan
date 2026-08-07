from services.api.src.workspaces.exceptions import WorkspacePlatformException

VALID_ROLES = {"Owner", "Admin", "Manager", "Operator", "Reviewer", "Viewer"}


def validate_role_name(role_name: str) -> str:
    if role_name not in VALID_ROLES:
        raise WorkspacePlatformException(f"Invalid role '{role_name}'. Must be one of {VALID_ROLES}")
    return role_name
