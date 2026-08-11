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
async def test_register_new_user_success() -> None:
    """Verify registration creates User with username equal to normalized email."""
    from unittest.mock import AsyncMock, MagicMock
    from services.api.src.auth.service import AuthService
    from services.api.src.auth.schemas import UserRegisterRequest
    from services.api.src.auth.models import User

    user_repo = MagicMock()
    token_repo = MagicMock()
    profile_repo = MagicMock()

    user_repo.get_by_email = AsyncMock(return_value=None)
    user_repo.get_by_username = AsyncMock(return_value=None)

    created_user = User(
        id=MagicMock(),
        email="rahul123@gmail.com",
        username="rahul123@gmail.com",
        hashed_password="mock_hash",
        is_active=True,
    )
    user_repo.create = AsyncMock(return_value=created_user)
    token_repo.create = AsyncMock()
    profile_repo.get_by_user_id = AsyncMock(return_value=None)
    profile_repo.create = AsyncMock()

    service = AuthService(
        user_repo=user_repo,
        token_repo=token_repo,
        profile_repo=profile_repo,
    )

    request = UserRegisterRequest(
        email="Rahul123@Gmail.com",
        password="Password123!",
        full_name="Rahul Sharma",
        phone="+15550192834",
    )

    tokens = await service.register(request)

    assert "access_token" in tokens
    assert "refresh_token" in tokens
    user_repo.create.assert_called_once()
    saved_user = user_repo.create.call_args[0][0]
    assert saved_user.email == "rahul123@gmail.com"
    assert saved_user.username == "rahul123@gmail.com"
    profile_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_register_duplicate_email_raises_exception() -> None:
    """Verify registration raises UserAlreadyExistsException when email is already registered."""
    from unittest.mock import AsyncMock, MagicMock
    from services.api.src.auth.service import AuthService
    from services.api.src.auth.schemas import UserRegisterRequest
    from services.api.src.auth.exceptions import UserAlreadyExistsException
    from services.api.src.auth.models import User

    user_repo = MagicMock()
    token_repo = MagicMock()

    existing_user = User(
        id=MagicMock(),
        email="existing@example.com",
        username="existing@example.com",
        hashed_password="mock_hash",
    )
    user_repo.get_by_email = AsyncMock(return_value=existing_user)

    service = AuthService(user_repo=user_repo, token_repo=token_repo)

    request = UserRegisterRequest(
        email="existing@example.com",
        password="Password123!",
    )

    with pytest.raises(UserAlreadyExistsException) as exc_info:
        await service.register(request)
    assert "already registered" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
async def test_register_same_name_different_emails_succeed() -> None:
    """Verify users with identical display names but different emails both register with username equal to their email."""
    from unittest.mock import AsyncMock, MagicMock
    from services.api.src.auth.service import AuthService
    from services.api.src.auth.schemas import UserRegisterRequest
    from services.api.src.auth.models import User

    user_repo = MagicMock()
    token_repo = MagicMock()
    profile_repo = MagicMock()

    user_repo.get_by_email = AsyncMock(return_value=None)
    user_repo.get_by_username = AsyncMock(return_value=None)
    user_repo.create = AsyncMock(side_effect=lambda u: u)
    token_repo.create = AsyncMock()
    profile_repo.get_by_user_id = AsyncMock(return_value=None)
    profile_repo.create = AsyncMock()

    service = AuthService(user_repo=user_repo, token_repo=token_repo, profile_repo=profile_repo)

    req_a = UserRegisterRequest(email="shyam1@gmail.com", password="Password123!", full_name="Shyam")
    req_b = UserRegisterRequest(email="shyam2@gmail.com", password="Password123!", full_name="Shyam")

    tokens_a = await service.register(req_a)
    user_a = user_repo.create.call_args_list[0][0][0]
    assert user_a.username == "shyam1@gmail.com"

    tokens_b = await service.register(req_b)
    user_b = user_repo.create.call_args_list[1][0][0]
    assert user_b.username == "shyam2@gmail.com"


@pytest.mark.asyncio
async def test_register_email_with_dot_and_plus() -> None:
    """Verify registration succeeds for email addresses containing dots and plus signs."""
    from unittest.mock import AsyncMock, MagicMock
    from services.api.src.auth.service import AuthService
    from services.api.src.auth.schemas import UserRegisterRequest

    user_repo = MagicMock()
    token_repo = MagicMock()
    profile_repo = MagicMock()

    user_repo.get_by_email = AsyncMock(return_value=None)
    user_repo.get_by_username = AsyncMock(return_value=None)
    user_repo.create = AsyncMock(side_effect=lambda u: u)
    token_repo.create = AsyncMock()
    profile_repo.get_by_user_id = AsyncMock(return_value=None)
    profile_repo.create = AsyncMock()

    service = AuthService(user_repo=user_repo, token_repo=token_repo, profile_repo=profile_repo)

    req_dot = UserRegisterRequest(email="john.doe@gmail.com", password="Password123!", full_name="John Doe")
    await service.register(req_dot)
    user_dot = user_repo.create.call_args_list[0][0][0]
    assert user_dot.email == "john.doe@gmail.com"
    assert user_dot.username == "john.doe@gmail.com"

    req_plus = UserRegisterRequest(email="john+test@gmail.com", password="Password123!", full_name="John Plus")
    await service.register(req_plus)
    user_plus = user_repo.create.call_args_list[1][0][0]
    assert user_plus.email == "john+test@gmail.com"
    assert user_plus.username == "john+test@gmail.com"


@pytest.mark.asyncio
async def test_existing_old_username_login_compatibility() -> None:
    """Verify existing user with old username (e.g. john_doe) can still authenticate cleanly."""
    from unittest.mock import AsyncMock, MagicMock
    from services.api.src.auth.service import AuthService
    from services.api.src.auth.schemas import UserLoginRequest
    from services.api.src.auth.models import User
    from services.api.src.auth.security import hash_password

    user_repo = MagicMock()
    token_repo = MagicMock()

    pwd_hash = hash_password("Password123!")
    existing_user = User(
        id=MagicMock(),
        email="john.doe@example.com",
        username="john_doe",
        hashed_password=pwd_hash,
        is_active=True,
    )

    user_repo.get_by_email = AsyncMock(return_value=None)
    user_repo.get_by_username = AsyncMock(return_value=existing_user)

    service = AuthService(user_repo=user_repo, token_repo=token_repo)

    login_req = UserLoginRequest(identifier="john_doe", password="Password123!")
    user = await service.authenticate(login_req)

    assert user.username == "john_doe"
    assert user.email == "john.doe@example.com"


@pytest.mark.asyncio
async def test_forgot_and_reset_password() -> None:
    """Verify forgot password generates reset token and reset password updates hash and revokes sessions."""
    from unittest.mock import AsyncMock, MagicMock
    from datetime import datetime, timedelta, timezone
    from services.api.src.auth.service import AuthService
    from services.api.src.auth.schemas import ResetPasswordRequest
    from services.api.src.auth.models import User, PasswordResetToken

    user_repo = MagicMock()
    token_repo = MagicMock()
    reset_token_repo = MagicMock()

    test_user = User(
        id=MagicMock(),
        email="resetuser@example.com",
        username="resetuser",
        hashed_password="old_hash",
        is_active=True,
    )

    user_repo.get_by_email = AsyncMock(return_value=test_user)
    user_repo.get_by_id = AsyncMock(return_value=test_user)
    user_repo.create = AsyncMock(return_value=test_user)
    token_repo.revoke_all_for_user = AsyncMock()

    valid_token_model = PasswordResetToken(
        id=MagicMock(),
        token_hash="mock_hash",
        user_id=test_user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
        is_used=False,
    )
    reset_token_repo.create = AsyncMock()
    reset_token_repo.get_valid_token = AsyncMock(return_value=valid_token_model)
    reset_token_repo.mark_used = AsyncMock()

    service = AuthService(
        user_repo=user_repo,
        token_repo=token_repo,
        reset_token_repo=reset_token_repo,
    )

    # 1. Test forgot password
    forgot_res = await service.forgot_password("resetuser@example.com")
    assert "reset_token" in forgot_res
    reset_token_repo.create.assert_called_once()

    # 2. Test reset password
    raw_token = forgot_res["reset_token"]
    reset_req = ResetPasswordRequest(token=raw_token, new_password="NewSecurePassword123!")
    await service.reset_password(reset_req)

    user_repo.create.assert_called_once()
    reset_token_repo.mark_used.assert_called_once()
    token_repo.revoke_all_for_user.assert_called_once_with(test_user.id)




