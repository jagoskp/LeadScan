from collections.abc import Sequence

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.monitoring.models import (
    DependencyStatus,
    MetricsSnapshot,
    ServiceStatus,
    SystemHealth,
)


class MonitoringRepository:
    """Repository managing database persistence and log queries for Observability."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_system_health(self, health: SystemHealth) -> SystemHealth:
        """Persist a new SystemHealth log entry."""
        self.session.add(health)
        await self.session.flush()
        return health

    async def create_dependency_status(
        self, dep_status: DependencyStatus
    ) -> DependencyStatus:
        """Persist a new DependencyStatus log entry."""
        self.session.add(dep_status)
        await self.session.flush()
        return dep_status

    async def create_service_status(self, svc_status: ServiceStatus) -> ServiceStatus:
        """Persist a new ServiceStatus log entry."""
        self.session.add(svc_status)
        await self.session.flush()
        return svc_status

    async def create_metrics_snapshot(
        self, snapshot: MetricsSnapshot
    ) -> MetricsSnapshot:
        """Persist a new MetricsSnapshot log entry."""
        self.session.add(snapshot)
        await self.session.flush()
        return snapshot

    async def get_latest_system_health(self) -> SystemHealth | None:
        """Retrieve the most recent SystemHealth log record."""
        stmt = select(SystemHealth).order_by(desc(SystemHealth.created_at)).limit(1)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_latest_dependency_statuses(self) -> Sequence[DependencyStatus]:
        """Fetch the latest status record for each monitored dependency."""
        # Query distinct dependencies, order by date descending
        # For simplicity, query the most recent logs (e.g. up to 10 logs)
        stmt = (
            select(DependencyStatus)
            .order_by(desc(DependencyStatus.created_at))
            .limit(10)
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_latest_service_statuses(self) -> Sequence[ServiceStatus]:
        """Fetch the latest status record for each monitored module service."""
        stmt = select(ServiceStatus).order_by(desc(ServiceStatus.created_at)).limit(12)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_latest_metrics_snapshot(self) -> MetricsSnapshot | None:
        """Retrieve the most recent metrics snapshot log record."""
        stmt = (
            select(MetricsSnapshot).order_by(desc(MetricsSnapshot.created_at)).limit(1)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
