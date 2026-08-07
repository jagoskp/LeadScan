class IdentityResolutionException(Exception):
    """Base exception for Enterprise Identity Resolution & Smart Duplicate Engine errors."""

    def __init__(self, message: str, code: str = "IDENTITY_RESOLUTION_ERROR", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class DuplicateMatchNotFoundException(IdentityResolutionException):
    """Raised when a duplicate match record is not found."""

    def __init__(self, match_id: str):
        super().__init__(f"Duplicate match record '{match_id}' not found", code="MATCH_NOT_FOUND", status_code=404)


class MergeConflictException(IdentityResolutionException):
    """Raised when field merge conflict cannot be resolved automatically."""

    def __init__(self, detail: str):
        super().__init__(f"Merge conflict error: {detail}", code="MERGE_CONFLICT_UNRESOLVED", status_code=422)


class RollbackFailedException(IdentityResolutionException):
    """Raised when a merge rollback operation fails or snapshot is invalid."""

    def __init__(self, detail: str):
        super().__init__(f"Rollback operation failed: {detail}", code="ROLLBACK_FAILED", status_code=422)
