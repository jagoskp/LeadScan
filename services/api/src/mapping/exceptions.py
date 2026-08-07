from fastapi import HTTPException, status


class MappingEngineException(HTTPException):
    """Base exception for all mapping engine errors."""
    pass


class MappingProfileNotFoundException(MappingEngineException):
    """Exception raised when a requested MappingProfile is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mapping profile not found",
        )


class MappingRuleException(MappingEngineException):
    """Exception raised when mapping rule creation or query fails."""

    def __init__(self, detail: str = "Invalid mapping rule layout") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class ValidationFailedException(MappingEngineException):
    """Exception raised when validation checks fail on mapped fields."""

    def __init__(self, detail: str = "Field validations failed") -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )
