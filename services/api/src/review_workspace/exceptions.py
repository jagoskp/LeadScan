from fastapi import HTTPException, status


class ReviewWorkspaceException(HTTPException):
    """Base exception for all review workspace errors."""
    pass


class ReviewSessionNotFoundException(ReviewWorkspaceException):
    """Exception raised when a requested ReviewSession is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review session not found",
        )


class ReviewItemNotFoundException(ReviewWorkspaceException):
    """Exception raised when a requested ReviewItem is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review item not found",
        )
