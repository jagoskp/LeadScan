# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.audit.repository import (
    ActivityLogRepository,
    AuditLogRepository,
    SecurityEventRepository,
)
from services.api.src.audit.service import AuditService
from services.api.src.database import get_db


def get_audit_log_repository(
    session: AsyncSession = Depends(get_db),
) -> AuditLogRepository:
    """Inject AuditLogRepository context."""
    return AuditLogRepository(session)


def get_activity_log_repository(
    session: AsyncSession = Depends(get_db),
) -> ActivityLogRepository:
    """Inject ActivityLogRepository context."""
    return ActivityLogRepository(session)


def get_security_event_repository(
    session: AsyncSession = Depends(get_db),
) -> SecurityEventRepository:
    """Inject SecurityEventRepository context."""
    return SecurityEventRepository(session)


def get_audit_service(
    audit_repo: AuditLogRepository = Depends(get_audit_log_repository),
    activity_repo: ActivityLogRepository = Depends(get_activity_log_repository),
    security_repo: SecurityEventRepository = Depends(get_security_event_repository),
) -> AuditService:
    """Inject AuditService context."""
    return AuditService(audit_repo, activity_repo, security_repo)
