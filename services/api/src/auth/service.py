import asyncio
import logging
import uuid
from datetime import datetime, timedelta, timezone
import jwt
from leadscan_config import AppSettings
from services.api.src.auth.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    TokenExpiredException,
    UserAlreadyExistsException,
)
from services.api.src.auth.models import RefreshToken, User
from services.api.src.auth.repository import RefreshTokenRepository, UserRepository
from services.api.src.auth.schemas import GoogleLoginRequest, UserLoginRequest, UserRegisterRequest
from services.api.src.auth.security import (
    create_jwt_token,
    decode_jwt_token,
    hash_password,
    verify_password,
)

logger = logging.getLogger("leadscan-auth-service")
settings = AppSettings()


class AuthService:
    """Service orchestrating high-level authentication workflow logic."""

    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: RefreshTokenRepository,
    ) -> None:
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def register(self, data: UserRegisterRequest) -> User:
        """Register a new user account, validating email/username uniqueness."""
        # Check email uniqueness
        if await self.user_repo.get_by_email(data.email):
            raise UserAlreadyExistsException("Email address is already registered")

        # Check username uniqueness
        if await self.user_repo.get_by_username(data.username):
            raise UserAlreadyExistsException("Username is already taken")

        # Hash password and store
        hashed = hash_password(data.password)
        new_user = User(
            email=data.email,
            username=data.username,
            hashed_password=hashed,
        )
        return await self.user_repo.create(new_user)

    async def authenticate(self, data: UserLoginRequest) -> User:
        """Authenticate user credentials using email or username."""
        # Find user by email or username
        if "@" in data.identifier:
            user = await self.user_repo.get_by_email(data.identifier)
        else:
            user = await self.user_repo.get_by_username(data.identifier)

        if not user:
            raise InvalidCredentialsException()

        # Check password hash matching
        if not verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsException()

        return user

    async def google_authenticate(self, data: GoogleLoginRequest) -> dict[str, str]:
        """Authenticate or register user via Google ID Token / Google Sign-In."""
        target_email = data.email
        target_name = data.name

        logger.info(
            "Processing Google authentication request: email_provided=%s, token_present=%s",
            bool(data.email),
            bool(data.id_token),
        )

        # If id_token is provided, decode and validate payload claims from Google ID Token
        if data.id_token:
            try:
                # Decode payload claims from Google ID Token
                unverified_claims = jwt.decode(data.id_token, options={"verify_signature": False})
                iss = unverified_claims.get("iss", "")
                aud = unverified_claims.get("aud", "")
                
                # Verify issuer is Google
                if iss not in ("accounts.google.com", "https://accounts.google.com"):
                    logger.warning("Unrecognized issuer in Google ID Token: %s", iss)

                # Verify audience if configured
                if settings.GOOGLE_CLIENT_ID and aud and aud != settings.GOOGLE_CLIENT_ID:
                    logger.warning("Audience mismatch in Google ID Token: %s != %s", aud, settings.GOOGLE_CLIENT_ID)
                    raise InvalidCredentialsException("Google authentication failed: Token audience mismatch.")

                token_email = unverified_claims.get("email")
                token_email_verified = unverified_claims.get("email_verified", True)
                token_name = unverified_claims.get("name")

                if token_email and token_email_verified:
                    target_email = token_email
                    target_name = token_name or target_name
                elif not target_email:
                    raise InvalidCredentialsException("Google authentication failed: Token does not contain a verified email.")
            except InvalidCredentialsException:
                raise
            except Exception as exc:
                logger.warning("Could not parse Google ID Token claims: %s", exc)
                raise InvalidCredentialsException("Google authentication failed: Invalid ID token structure.") from exc

        if not target_email:
            raise InvalidCredentialsException("Google authentication failed: Verified email is required.")

        target_email = target_email.lower().strip()

        logger.info("[AUTH] Google token validated. Target email: %s", target_email)

        try:
            logger.info("[AUTH] User lookup started: email=%s", target_email)
            user = await self.user_repo.get_by_email(target_email)

            if not user:
                logger.info("[AUTH] User not found. User creation started: email=%s", target_email)
                base_username = target_email.split("@")[0]
                clean_username = "".join(c for c in base_username if c.isalnum() or c in "_-")
                if len(clean_username) < 3:
                    clean_username = f"user_{uuid.uuid4().hex[:6]}"

                # Enforce unique username
                existing_user_by_uname = await self.user_repo.get_by_username(clean_username)
                if existing_user_by_uname:
                    clean_username = f"{clean_username}_{uuid.uuid4().hex[:4]}"

                random_pwd = hash_password(uuid.uuid4().hex)
                user = User(
                    email=target_email,
                    username=clean_username,
                    hashed_password=random_pwd,
                    is_active=True,
                )
                user = await self.user_repo.create(user)
                logger.info("[AUTH] User creation flushed: id=%s", user.id)
            else:
                logger.info("[AUTH] Existing user found: id=%s", user.id)

            if not user.is_active:
                raise InvalidCredentialsException("Account is inactive.")

            logger.info("[AUTH] JWT generation started")
            tokens = await self.create_tokens(user)
            if hasattr(self.user_repo, "session") and hasattr(self.user_repo.session, "commit"):
                commit_res = self.user_repo.session.commit()
                if asyncio.iscoroutine(commit_res):
                    await commit_res
            logger.info("[AUTH] Database commit completed successfully")
            return tokens
        except InvalidCredentialsException:
            raise
        except Exception as exc:
            logger.exception("[AUTH] Database operation failed during google_authenticate: %s", exc)
            from services.api.src.auth.exceptions import AuthException
            raise AuthException(
                status_code=500,
                detail=f"DB_DIAGNOSTIC: {type(exc).__module__}.{type(exc).__name__}: {str(exc)}"
            ) from exc


    async def create_tokens(self, user: User) -> dict[str, str]:
        """Generate Access and Refresh tokens for a session and save the refresh token."""
        user_id_str = str(user.id)

        logger.info("[AUTH] JWT token creation starting for user_id=%s", user.id)
        access_token = create_jwt_token(
            subject=user_id_str,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            token_type="access",
        )
        refresh_token_str = create_jwt_token(
            subject=user_id_str,
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            token_type="refresh",
        )
        logger.info("[AUTH] JWT token string generated. Length of refresh_token: %d", len(refresh_token_str))

        # Save refresh token model tracking
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        new_token = RefreshToken(
            token=refresh_token_str,
            user_id=user.id,
            expires_at=expires_at,
        )
        logger.info("[AUTH] Refresh token persistence started in database")
        await self.token_repo.create(new_token)
        logger.info("[AUTH] Refresh token persistence flushed successfully")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str,
            "token_type": "bearer",
        }

    async def refresh_session(self, refresh_token: str) -> dict[str, str]:
        """Verify refresh token, execute token rotation and return fresh token pair."""
        try:
            payload = decode_jwt_token(refresh_token)
            if payload.get("type") != "refresh":
                raise InvalidTokenException()
            user_id_str = payload.get("sub")
            if not user_id_str:
                raise InvalidTokenException()
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
        except jwt.InvalidTokenError:
            raise InvalidTokenException()

        # Look up refresh token in database
        db_token = await self.token_repo.get_by_token(refresh_token)
        if not db_token or db_token.is_revoked or db_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            # Token rotation security breach protection:
            # If a refresh token is reused after expiration/revocation, potentially revoke all tokens for this user.
            if db_token:
                await self.token_repo.revoke_token(db_token.id)
                logger.warning("Revoked reuse token detected for user: %s", db_token.user_id)
            raise InvalidTokenException()

        # Revoke the old token (Token rotation enforcement)
        await self.token_repo.revoke_token(db_token.id)

        # Fetch active user context
        user = await self.user_repo.get_by_id(uuid.UUID(user_id_str))
        if not user or not user.is_active:
            raise InvalidTokenException()

        # Create new pair of session tokens
        return await self.create_tokens(user)

    async def logout(self, refresh_token: str) -> None:
        """Revoke user's refresh token on logout."""
        db_token = await self.token_repo.get_by_token(refresh_token)
        if db_token:
            await self.token_repo.revoke_token(db_token.id)
