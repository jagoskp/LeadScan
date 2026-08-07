import uuid
from typing import Any, Sequence
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.src.audit.models import AuditLog, ActivityLog, SecurityEvent


class AuditLogRepository:
    """Repository managing AuditLog persistence and query operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_memberships(self, user_id: uuid.UUID) -> Sequence[Any]:
        """Query user organization memberships to bypass lazy-loading issues."""
        from services.api.src.organization.models import OrganizationMember
        result = await self.session.execute(
            select(OrganizationMember).where(OrganizationMember.user_id == user_id)
        )
        return result.scalars().all()

    async def create(self, log: AuditLog) -> AuditLog:
        """Persist a new AuditLog record."""
        self.session.add(log)
        await self.session.flush()
        return log

    async def get_by_id(self, log_id: uuid.UUID) -> AuditLog | None:
        """Retrieve an AuditLog record by ID."""
        result = await self.session.execute(
            select(AuditLog).where(AuditLog.id == log_id)
        )
        return result.scalar_one_or_none()

    async def list_logs(
        self,
        user_id: uuid.UUID | None = None,
        organization_ids: list[uuid.UUID] | None = None,
        event_type: str | None = None,
        severity: str | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[AuditLog], int]:
        """Query and filter system audit logs with pagination."""
        conditions = []

        if user_id and organization_ids:
            conditions.append(
                or_(
                    AuditLog.user_id == user_id,
                    AuditLog.organization_id.in_(organization_ids),
                )
            )
        elif user_id:
            conditions.append(AuditLog.user_id == user_id)
        elif organization_ids:
            conditions.append(AuditLog.organization_id.in_(organization_ids))

        if event_type:
            conditions.append(AuditLog.event_type == event_type)
        if severity:
            conditions.append(AuditLog.severity == severity)

        if search:
            search_pat = f"%{search}%"
            conditions.append(
                or_(
                    AuditLog.action.ilike(search_pat),
                    AuditLog.resource_type.ilike(search_pat),
                    AuditLog.ip_address.ilike(search_pat),
                )
            )

        # Count total
        count_stmt = select(func.count()).select_from(AuditLog)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
        count_res = await self.session.execute(count_stmt)
        total = count_res.scalar() or 0

        # Retrieve records
        stmt = (
            select(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        if conditions:
            stmt = stmt.where(and_(*conditions))
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return items, total


class ActivityLogRepository:
    """Repository managing ActivityLog database tracking operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, log: ActivityLog) -> ActivityLog:
        """Persist a new ActivityLog record."""
        self.session.add(log)
        await self.session.flush()
        return log

    async def list_activities(
        self,
        user_id: uuid.UUID | None = None,
        organization_ids: list[uuid.UUID] | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[ActivityLog], int]:
        """List activity logs with filtering."""
        conditions = []

        if user_id and organization_ids:
            conditions.append(
                or_(
                    ActivityLog.user_id == user_id,
                    ActivityLog.organization_id.in_(organization_ids),
                )
            )
        elif user_id:
            conditions.append(ActivityLog.user_id == user_id)
        elif organization_ids:
            conditions.append(ActivityLog.organization_id.in_(organization_ids))

        if resource_type:
            conditions.append(ActivityLog.resource_type == resource_type)
        if resource_id:
            conditions.append(ActivityLog.resource_id == resource_id)

        # Count total
        count_stmt = select(func.count()).select_from(ActivityLog)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
        count_res = await self.session.execute(count_stmt)
        total = count_res.scalar() or 0

        # Retrieve records
        stmt = (
            select(ActivityLog)
            .order_by(ActivityLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        if conditions:
            stmt = stmt.where(and_(*conditions))
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def get_user_timeline(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[ActivityLog]:
        """Fetch user activity timeline sorted chronologically."""
        stmt = (
            select(ActivityLog)
            .where(ActivityLog.user_id == user_id)
            .order_by(ActivityLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_resource_timeline(
        self, resource_type: str, resource_id: str, skip: int = 0, limit: int = 100
    ) -> Sequence[ActivityLog]:
        """Fetch resource activity timeline sorted chronologically."""
        stmt = (
            select(ActivityLog)
            .where(
                and_(
                    ActivityLog.resource_type == resource_type,
                    ActivityLog.resource_id == resource_id,
                )
            )
            .order_by(ActivityLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()


class SecurityEventRepository:
    """Repository managing SecurityEvent persistence and querying."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, event: SecurityEvent) -> SecurityEvent:
        """Persist a new SecurityEvent record."""
        self.session.add(event)
        await self.session.flush()
        return event

    async def list_events(
        self,
        user_id: uuid.UUID | None = None,
        organization_ids: list[uuid.UUID] | None = None,
        event_type: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[SecurityEvent], int]:
        """Query security events with pagination."""
        conditions = []

        if user_id and organization_ids:
            conditions.append(
                or_(
                    SecurityEvent.user_id == user_id,
                    SecurityEvent.organization_id.in_(organization_ids),
                )
            )
        elif user_id:
            conditions.append(SecurityEvent.user_id == user_id)
        elif organization_ids:
            conditions.append(SecurityEvent.organization_id.in_(organization_ids))

        if event_type:
            conditions.append(SecurityEvent.event_type == event_type)

        # Count total
        count_stmt = select(func.count()).select_from(SecurityEvent)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
        count_res = await self.session.execute(count_stmt)
        total = count_res.scalar() or 0

        # Retrieve records
        stmt = (
            select(SecurityEvent)
            .order_by(SecurityEvent.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        if conditions:
            stmt = stmt.where(and_(*conditions))
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return items, total
