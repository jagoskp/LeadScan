class SearchException(Exception):
    """Base exception for Enterprise Universal Search Engine errors."""

    def __init__(self, message: str, code: str = "SEARCH_ERROR", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class SearchQueryException(SearchException):
    """Raised when search query string validation fails."""

    def __init__(self, message: str):
        super().__init__(message, code="INVALID_SEARCH_QUERY", status_code=400)


class SearchIndexNotFoundException(SearchException):
    """Raised when search index entry is not found."""

    def __init__(self, index_id: str):
        super().__init__(f"Search index entry '{index_id}' not found", code="SEARCH_INDEX_NOT_FOUND", status_code=404)
