from services.api.src.search.exceptions import SearchQueryException


def validate_search_query(query: str) -> str:
    """Validate query string length and boundaries."""
    if not query or not isinstance(query, str):
        raise SearchQueryException("Search query cannot be empty.")
    
    cleaned = query.strip()
    if len(cleaned) < 1:
        raise SearchQueryException("Search query must contain at least 1 character.")
    if len(cleaned) > 500:
        raise SearchQueryException("Search query exceeds maximum allowed length of 500 characters.")
    return cleaned
