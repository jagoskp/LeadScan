

def validate_database_url(url: str) -> str:
    """Verify that the database URL uses PostgreSQL protocol formats."""
    if not url.startswith("postgresql"):
        raise ValueError("Database URL must start with 'postgresql'")
    return url


def validate_redis_url(url: str) -> str:
    """Verify that the Redis URL uses redis or rediss protocol formats."""
    if not (url.startswith("redis://") or url.startswith("rediss://")):
        raise ValueError("Redis URL must start with 'redis://' or 'rediss://'")
    return url


def validate_jwt_secret_strength(secret: str, environment: str) -> str:
    """Ensure JWT secret is sufficiently strong in staging/production contexts."""
    if environment in ("staging", "production"):
        if len(secret) < 32:
            raise ValueError(
                "JWT secret key must be at least 32 characters long "
                "in staging or production environments"
            )
        # Check if it is the placeholder default
        if "change_me" in secret.lower() or "secret_key" in secret.lower():
            raise ValueError(
                "Default placeholder secret key cannot be used "
                "in staging or production environments"
            )
    return secret
