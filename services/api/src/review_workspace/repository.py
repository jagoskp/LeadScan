import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.review_workspace.models import (
    CorrectionHistory,
    ReviewItem,
    ReviewSession,
    ValidationIssue,
)


class ReviewSessionRepository:
    """Repository handling persistence operations for ReviewSessions."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, session: ReviewSession) -> ReviewSession:
        """Persist a new ReviewSession configuration."""
        self.session.add(session)
        await self.session.flush()
        return session

    async def get_by_id(self, session_id: uuid.UUID) -> ReviewSession | None:
        """Retrieve a specific ReviewSession preloading items and issues."""
        stmt = (
            select(ReviewSession)
            .where(ReviewSession.id == session_id)
            .options(
                selectinload(ReviewSession.items).selectinload(
                    ReviewItem.corrections
                ),
                selectinload(ReviewSession.validation_issues),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_sessions(self) -> Sequence[ReviewSession]:
        """List ReviewSessions present in the database."""
        stmt = select(ReviewSession).options(
            selectinload(ReviewSession.items),
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_session_status(
        self,
        session_id: uuid.UUID,
        status: str,
        reviewer_id: uuid.UUID | None = None,
    ) -> ReviewSession | None:
        """Update session review status."""
        values: dict[str, Any] = {"status": status}
        if reviewer_id:
            values["reviewer_id"] = reviewer_id
        stmt = (
            update(ReviewSession)
            .where(ReviewSession.id == session_id)
            .values(**values)
        )
        await self.session.execute(stmt)
        return await self.get_by_id(session_id)


class ReviewItemRepository:
    """Repository handling persistence operations for individual review items."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_item(self, item: ReviewItem) -> ReviewItem:
        """Persist a new ReviewItem configuration."""
        self.session.add(item)
        await self.session.flush()
        return item

    async def get_item_by_id(self, item_id: uuid.UUID) -> ReviewItem | None:
        """Retrieve a specific ReviewItem preloading corrections history."""
        stmt = (
            select(ReviewItem)
            .where(ReviewItem.id == item_id)
            .options(selectinload(ReviewItem.corrections))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_item_value(
        self, item_id: uuid.UUID, value: str, status: str
    ) -> ReviewItem | None:
        """Update value attributes on a review item."""
        stmt = (
            update(ReviewItem)
            .where(ReviewItem.id == item_id)
            .values(current_value=value, status=status)
        )
        await self.session.execute(stmt)
        return await self.get_item_by_id(item_id)

    async def create_correction(
        self, correction: CorrectionHistory
    ) -> CorrectionHistory:
        """Persist manual edit correction history log."""
        self.session.add(correction)
        await self.session.flush()
        return correction

    async def create_validation_issue(
        self, issue: ValidationIssue
    ) -> ValidationIssue:
        """Persist ValidationIssue logs."""
        self.session.add(issue)
        await self.session.flush()
        return issue

    async def clear_validation_issues(self, session_id: uuid.UUID) -> None:
        """Delete validation issues associated with review session ID."""
        stmt = delete(ValidationIssue).where(
            ValidationIssue.session_id == session_id
        )
        await self.session.execute(stmt)
