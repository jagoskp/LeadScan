import uuid
from datetime import datetime, timezone
from typing import Any, Sequence
from sqlalchemy import select, update, delete, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.src.notifications.models import (
    Notification,
    NotificationTemplate,
    NotificationPreference,
)


class NotificationTemplateRepository:
    """Repository handling database operations for NotificationTemplates."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, template_id: uuid.UUID) -> NotificationTemplate | None:
        """Fetch template by primary key ID."""
        result = await self.session.execute(
            select(NotificationTemplate).where(NotificationTemplate.id == template_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(
        self, name: str, organization_id: uuid.UUID | None = None
    ) -> NotificationTemplate | None:
        """Fetch active template by name, matching org or system scope."""
        stmt = select(NotificationTemplate).where(
            and_(
                NotificationTemplate.name == name,
                NotificationTemplate.is_active.is_(True),
            )
        )
        if organization_id:
            # Query organization-specific template, fallback to system-wide
            stmt = stmt.where(
                or_(
                    NotificationTemplate.organization_id == organization_id,
                    NotificationTemplate.organization_id.is_(None),
                )
            ).order_by(
                # Org-specific overrides system-wide
                NotificationTemplate.organization_id.desc()
            )
        else:
            stmt = stmt.where(NotificationTemplate.organization_id.is_(None))

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_templates(
        self, organization_id: uuid.UUID | None = None, skip: int = 0, limit: int = 100
    ) -> Sequence[NotificationTemplate]:
        """List active templates available to an organization context."""
        stmt = select(NotificationTemplate).where(
            NotificationTemplate.is_active.is_(True)
        )
        if organization_id:
            stmt = stmt.where(
                or_(
                    NotificationTemplate.organization_id == organization_id,
                    NotificationTemplate.organization_id.is_(None),
                )
            )
        else:
            stmt = stmt.where(NotificationTemplate.organization_id.is_(None))

        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, template: NotificationTemplate) -> NotificationTemplate:
        """Persist a new NotificationTemplate record."""
        self.session.add(template)
        await self.session.flush()
        return template

    async def update(
        self, template_id: uuid.UUID, data: dict[str, Any]
    ) -> NotificationTemplate | None:
        """Update fields on an existing template."""
        if data:
            data["updated_at"] = datetime.now(timezone.utc)
            await self.session.execute(
                update(NotificationTemplate)
                .where(NotificationTemplate.id == template_id)
                .values(**data)
            )
        return await self.get_by_id(template_id)

    async def delete(self, template_id: uuid.UUID) -> bool:
        """Delete or deactivate a template."""
        result = await self.session.execute(
            delete(NotificationTemplate).where(NotificationTemplate.id == template_id)
        )
        rowcount = getattr(result, "rowcount", 0)
        return rowcount > 0


class NotificationPreferenceRepository:
    """Repository handling database operations for NotificationPreferences."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_user_id(
        self, user_id: uuid.UUID, organization_id: uuid.UUID | None = None
    ) -> Sequence[NotificationPreference]:
        """Get all preferences configured for a user in an org context."""
        stmt = select(NotificationPreference).where(
            NotificationPreference.user_id == user_id
        )
        if organization_id:
            stmt = stmt.where(NotificationPreference.organization_id == organization_id)
        else:
            stmt = stmt.where(NotificationPreference.organization_id.is_(None))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_user_and_type(
        self,
        user_id: uuid.UUID,
        notification_type: str,
        organization_id: uuid.UUID | None = None,
    ) -> NotificationPreference | None:
        """Get specific preferences configured for a user and type."""
        stmt = select(NotificationPreference).where(
            and_(
                NotificationPreference.user_id == user_id,
                NotificationPreference.notification_type == notification_type,
            )
        )
        if organization_id:
            stmt = stmt.where(
                or_(
                    NotificationPreference.organization_id == organization_id,
                    NotificationPreference.organization_id.is_(None),
                )
            ).order_by(
                NotificationPreference.organization_id.desc()
            )
        else:
            stmt = stmt.where(NotificationPreference.organization_id.is_(None))

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def upsert_preference(
        self,
        user_id: uuid.UUID,
        notification_type: str,
        channel_enabled: bool,
        preferences: dict[str, Any] | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> NotificationPreference:
        """Create or update a preference mapping for a user."""
        # Ensure exact match in org id for upsert logic
        exact_stmt = select(NotificationPreference).where(
            and_(
                NotificationPreference.user_id == user_id,
                NotificationPreference.notification_type == notification_type,
                NotificationPreference.organization_id == organization_id,
            )
        )
        exact_res = await self.session.execute(exact_stmt)
        exact_match = exact_res.scalar_one_or_none()

        if exact_match:
            exact_match.channel_enabled = channel_enabled
            if preferences is not None:
                exact_match.preferences = preferences
            exact_match.updated_at = datetime.now(timezone.utc)
            await self.session.flush()
            return exact_match
        else:
            new_pref = NotificationPreference(
                user_id=user_id,
                organization_id=organization_id,
                notification_type=notification_type,
                channel_enabled=channel_enabled,
                preferences=preferences or {},
            )
            self.session.add(new_pref)
            await self.session.flush()
            return new_pref


class NotificationRepository:
    """Repository handling database operations for Notifications."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, notification_id: uuid.UUID) -> Notification | None:
        """Fetch notification metadata by ID."""
        result = await self.session.execute(
            select(Notification).where(Notification.id == notification_id)
        )
        return result.scalar_one_or_none()

    async def create(self, notification: Notification) -> Notification:
        """Save a new notification log."""
        self.session.add(notification)
        await self.session.flush()
        return notification

    async def update_status(
        self,
        notification_id: uuid.UUID,
        status: str,
        queue_metadata: dict[str, Any] | None = None,
        history_item: dict[str, Any] | None = None,
    ) -> Notification | None:
        """Update notification status, tracking dates and status history."""
        notification = await self.get_by_id(notification_id)
        if not notification:
            return None

        notification.status = status
        notification.updated_at = datetime.now(timezone.utc)

        if status == "SENT":
            notification.sent_at = datetime.now(timezone.utc)
        elif status == "DELIVERED":
            notification.delivered_at = datetime.now(timezone.utc)
            if not notification.sent_at:
                notification.sent_at = datetime.now(timezone.utc)
        elif status == "READ":
            notification.read_at = datetime.now(timezone.utc)
            if not notification.delivered_at:
                notification.delivered_at = datetime.now(timezone.utc)
            if not notification.sent_at:
                notification.sent_at = datetime.now(timezone.utc)

        if queue_metadata is not None:
            meta = dict(notification.queue_metadata or {})
            meta.update(queue_metadata)
            notification.queue_metadata = meta

        if history_item:
            history = list(notification.status_history or [])
            history.append(history_item)
            notification.status_history = history

        await self.session.flush()
        return notification

    async def delete(self, notification_id: uuid.UUID) -> bool:
        """Hard delete a notification record."""
        result = await self.session.execute(
            delete(Notification).where(Notification.id == notification_id)
        )
        rowcount = getattr(result, "rowcount", 0)
        return rowcount > 0

    async def list_notifications(
        self,
        user_id: uuid.UUID,
        organization_ids: list[uuid.UUID] | None = None,
        status: str | None = None,
        notification_type: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[Notification], int]:
        """List notifications belonging to user or user's organizations."""
        conditions = [Notification.user_id == user_id]
        if organization_ids:
            conditions.append(Notification.organization_id.in_(organization_ids))

        base_filter = or_(*conditions)

        if status:
            base_filter = and_(base_filter, Notification.status == status)
        if notification_type:
            base_filter = and_(
                base_filter, Notification.notification_type == notification_type
            )

        # Count total
        count_stmt = select(func.count()).select_from(Notification).where(base_filter)
        count_res = await self.session.execute(count_stmt)
        total = count_res.scalar() or 0

        # Fetch records paginated
        stmt = (
            select(Notification)
            .where(base_filter)
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return items, total
