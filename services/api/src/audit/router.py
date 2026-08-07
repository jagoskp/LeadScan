# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.audit.dependencies import get_audit_service
from services.api.src.audit.schemas import (
    ActivityLogCreate,
    ActivityLogListResponse,
    ActivityLogResponse,
    AuditEventType,
    AuditLogCreate,
    AuditLogListResponse,
    AuditLogResponse,
    AuditSeverity,
    SecurityEventCreate,
    SecurityEventListResponse,
    SecurityEventResponse,
)
from services.api.src.audit.service import AuditService
from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User

router = APIRouter(prefix="/audit", tags=["audit"])


# ----------------------------------------------------
# Audit Logs Endpoints
# ----------------------------------------------------


@router.post(
    "/logs", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED
)
async def create_audit_log(
    data: AuditLogCreate,
    current_user: User = Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
) -> Any:
    """Create a new system-level audit log entry."""
    return await service.create_audit_log(data)


@router.get("/logs", response_model=AuditLogListResponse)
async def list_audit_logs(
    organization_id: uuid.UUID | None = Query(
        None, description="Scope to organization (requires admin status)"
    ),
    event_type: AuditEventType | None = Query(
        None, description="Filter by event category"
    ),
    severity: AuditSeverity | None = Query(
        None, description="Filter by severity level"
    ),
    search: str | None = Query(
        None, description="Full-text search on action, type, or IP address"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
) -> Any:
    """List, filter, and search system audit logs."""
    event_type_str = event_type.value if event_type else None
    severity_str = severity.value if severity else None

    items, total = await service.list_audit_logs(
        user=current_user,
        organization_id=organization_id,
        event_type=event_type_str,
        severity=severity_str,
        search=search,
        skip=skip,
        limit=limit,
    )
    return AuditLogListResponse(
        items=[AuditLogResponse.model_validate(item) for item in items],
        total=total,
        page=skip // limit + 1,
        size=limit,
    )


@router.get("/logs/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(
    log_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
) -> Any:
    """Retrieve detailed state of a single system audit log."""
    return await service.get_audit_log(log_id, current_user)


# ----------------------------------------------------
# Activity Logs Endpoints
# ----------------------------------------------------


@router.post(
    "/activity", response_model=ActivityLogResponse, status_code=status.HTTP_201_CREATED
)
async def create_activity_log(
    data: ActivityLogCreate,
    current_user: User = Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
) -> Any:
    """Create a new activity tracking event."""
    return await service.create_activity_log(data)


@router.get("/activity", response_model=ActivityLogListResponse)
async def list_activity_logs(
    organization_id: uuid.UUID | None = Query(
        None, description="Scope to organization context"
    ),
    resource_type: str | None = Query(
        None, description="Filter by resource (e.g. Document)"
    ),
    resource_id: str | None = Query(None, description="Filter by target resource UUID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
) -> Any:
    """List activity logs with optional resource filtering."""
    items, total = await service.list_activity_logs(
        user=current_user,
        organization_id=organization_id,
        resource_type=resource_type,
        resource_id=resource_id,
        skip=skip,
        limit=limit,
    )
    return ActivityLogListResponse(
        items=[ActivityLogResponse.model_validate(item) for item in items],
        total=total,
        page=skip // limit + 1,
        size=limit,
    )


@router.get("/activity/user/{target_user_id}", response_model=list[ActivityLogResponse])
async def get_user_activity_timeline(
    target_user_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
) -> Any:
    """Retrieve User Activity Timeline chronologically."""
    items = await service.get_user_timeline(
        user=current_user,
        target_user_id=target_user_id,
        skip=skip,
        limit=limit,
    )
    return [ActivityLogResponse.model_validate(item) for item in items]


@router.get(
    "/activity/resource/{resource_type}/{resource_id}",
    response_model=list[ActivityLogResponse],
)
async def get_resource_activity_timeline(
    resource_type: str,
    resource_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
) -> Any:
    """Retrieve Resource Activity Timeline chronologically."""
    items = await service.get_resource_timeline(
        user=current_user,
        resource_type=resource_type,
        resource_id=resource_id,
        skip=skip,
        limit=limit,
    )
    return [ActivityLogResponse.model_validate(item) for item in items]


# ----------------------------------------------------
# Security Events Endpoints
# ----------------------------------------------------


@router.post(
    "/security",
    response_model=SecurityEventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_security_event(
    data: SecurityEventCreate,
    current_user: User = Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
) -> Any:
    """Create a security event (e.g. failed logins, brute-force logs)."""
    return await service.create_security_event(data)


@router.get("/security", response_model=SecurityEventListResponse)
async def list_security_events(
    organization_id: uuid.UUID | None = Query(
        None, description="Scope to organization (requires admin status)"
    ),
    event_type: str | None = Query(
        None, description="Filter by security type (e.g. failed_login)"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
) -> Any:
    """List and query security logs."""
    items, total = await service.list_security_events(
        user=current_user,
        organization_id=organization_id,
        event_type=event_type,
        skip=skip,
        limit=limit,
    )
    return SecurityEventListResponse(
        items=[SecurityEventResponse.model_validate(item) for item in items],
        total=total,
        page=skip // limit + 1,
        size=limit,
    )
