import uuid
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.src.auth.models import User, RefreshToken


class UserRepository:
    """Repository managing User database persistence operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Fetch a user by their UUID primary key."""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by their email address."""
        result = await self.session.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        """Fetch a user by their username."""
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Persist a new User model to database."""
        user.email = user.email.lower()
        self.session.add(user)
        await self.session.flush()
        return user


class RefreshTokenRepository:
    """Repository managing RefreshToken database persistence operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_token(self, token: str) -> RefreshToken | None:
        """Fetch a refresh token record."""
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        return result.scalar_one_or_none()

    async def get_active_tokens_for_user(self, user_id: uuid.UUID) -> Sequence[RefreshToken]:
        """Fetch all non-revoked refresh tokens for a user."""
        result = await self.session.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked == False,
            )
        )
        return result.scalars().all()

    async def create(self, refresh_token: RefreshToken) -> RefreshToken:
        """Persist a new RefreshToken record."""
        self.session.add(refresh_token)
        await self.session.flush()
        return refresh_token

    async def revoke_token(self, token_id: uuid.UUID) -> None:
        """Revoke a refresh token by setting is_revoked to True."""
        await self.session.execute(
            update(RefreshToken)
            .where(RefreshToken.id == token_id)
            .values(is_revoked=True)
        )
