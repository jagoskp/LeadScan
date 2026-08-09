# Unit test cases for authentication service
import pytest


def test_password_hashing_placeholder() -> None:
    """Structure placeholder verifying password hashing and verify check matches."""
    # To be implemented using Argon2 hashing validation in Phase 3
    pass


def test_jwt_generation_placeholder() -> None:
    """Structure placeholder verifying JWT signature encoding and decoding."""
    pass


@pytest.mark.asyncio
async def test_google_authenticate_user_creation_and_restoration() -> None:
    """Verify Google authentication creates new user on first login and restores existing user on subsequent logins."""
    from unittest.mock import AsyncMock, MagicMock
    import services.api.src.users.models  # noqa: F401
    import services.api.src.organization.models  # noqa: F401
    from services.api.src.auth.service import AuthService
    from services.api.src.auth.schemas import GoogleLoginRequest
    from services.api.src.auth.models import User

    user_repo = MagicMock()
    token_repo = MagicMock()

    # First login simulation: User does not exist
    user_repo.get_by_email = AsyncMock(return_value=None)
    user_repo.get_by_username = AsyncMock(return_value=None)

    created_user = User(
        id=MagicMock(),
        email="realgoogleuser@example.com",
        username="realgoogleuser",
        hashed_password="mock_hash",
        is_active=True,
    )
    user_repo.create = AsyncMock(return_value=created_user)
    token_repo.create = AsyncMock()

    service = AuthService(user_repo=user_repo, token_repo=token_repo)

    import jwt
    valid_id_token = jwt.encode(
        {"iss": "accounts.google.com", "email": "realgoogleuser@example.com", "email_verified": True},
        "secret",
        algorithm="HS256",
    )
    request = GoogleLoginRequest(
        id_token=valid_id_token,
        email="realgoogleuser@example.com",
        name="Real Google User",
    )

    tokens = await service.google_authenticate(request)

    assert "access_token" in tokens
    assert "refresh_token" in tokens
    user_repo.create.assert_called_once()

    # Second login simulation: User already exists
    user_repo.get_by_email = AsyncMock(return_value=created_user)
    user_repo.create.reset_mock()

    tokens_existing = await service.google_authenticate(request)
    assert "access_token" in tokens_existing
    user_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_google_authenticate_audience_mismatch() -> None:
    """Verify Google authentication raises InvalidCredentialsException when token audience does not match configured client id."""
    from unittest.mock import AsyncMock, MagicMock
    import jwt
    from services.api.src.auth.service import AuthService
    from services.api.src.auth.schemas import GoogleLoginRequest
    from services.api.src.auth.exceptions import InvalidCredentialsException
    from services.api.src.auth.service import settings

    user_repo = MagicMock()
    token_repo = MagicMock()
    service = AuthService(user_repo=user_repo, token_repo=token_repo)

    # Encode a dummy token with mismatched audience
    fake_token = jwt.encode(
        {"iss": "accounts.google.com", "aud": "mismatched_client_id.apps.googleusercontent.com", "email": "user@example.com"},
        "secret",
        algorithm="HS256",
    )

    original_client_id = settings.GOOGLE_CLIENT_ID
    try:
        settings.GOOGLE_CLIENT_ID = "673923021753-pkjkh3po4mrp7l6fbe0bhcjn4837s3eu.apps.googleusercontent.com"
        request = GoogleLoginRequest(id_token=fake_token, email="user@example.com")
        with pytest.raises(InvalidCredentialsException) as exc_info:
            await service.google_authenticate(request)
        assert "audience mismatch" in str(exc_info.value.detail).lower()
    finally:
        settings.GOOGLE_CLIENT_ID = original_client_id


@pytest.mark.asyncio
async def test_google_authenticate_malformed_token() -> None:
    """Verify Google authentication raises InvalidCredentialsException when token is malformed string."""
    from unittest.mock import MagicMock
    from services.api.src.auth.service import AuthService
    from services.api.src.auth.schemas import GoogleLoginRequest
    from services.api.src.auth.exceptions import InvalidCredentialsException

    user_repo = MagicMock()
    token_repo = MagicMock()
    service = AuthService(user_repo=user_repo, token_repo=token_repo)

    request = GoogleLoginRequest(id_token="malformed_token_string", email="user@example.com")
    with pytest.raises(InvalidCredentialsException) as exc_info:
        await service.google_authenticate(request)
    assert "invalid id token structure" in str(exc_info.value.detail).lower()



