from fastapi import HTTPException, status


class OrganizationModuleException(HTTPException):
    """Base exception class for all organization/workspace module errors."""
    pass


class OrganizationNotFoundException(OrganizationModuleException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )


class SlugAlreadyExistsException(OrganizationModuleException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this slug already exists",
        )


class MemberAlreadyExistsException(OrganizationModuleException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this organization",
        )


class MemberNotFoundException(OrganizationModuleException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization member not found",
        )


class ForbiddenOrganizationActionException(OrganizationModuleException):
    def __init__(self, message: str = "Forbidden: Insufficient privileges for this organization action") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
        )
