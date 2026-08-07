from services.api.src.identity.exceptions import IdentityResolutionException


def validate_confidence_threshold(threshold: float) -> float:
    """Validate duplicate confidence score threshold."""
    if threshold < 0.0 or threshold > 100.0:
        raise IdentityResolutionException("Confidence threshold must be between 0.0 and 100.0.")
    return threshold
