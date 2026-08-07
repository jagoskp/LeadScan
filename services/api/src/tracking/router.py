import uuid
from typing import Any
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.auth.models import User
from services.api.src.auth.dependencies import get_current_user
from services.api.src.tracking.schemas import (
    DeviceRegisterRequest,
    DeviceRegisterResponse,
    SessionStartRequest,
    SessionStartResponse,
    SessionEndRequest,
    SessionEndResponse,
    UsageTrackEventRequest,
    UsageStatsResponse,
    SubscriptionStatusResponse,
    AdminDashboardAnalyticsResponse,
)
from services.api.src.tracking.service import TrackingService

router = APIRouter(prefix="/tracking", tags=["tracking"])


def get_tracking_service(db: AsyncSession = Depends(get_db)) -> TrackingService:
    return TrackingService(db)


async def get_optional_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User | None:
    """Helper to extract user if token present, or return None for public/anonymous events."""
    try:
        from services.api.src.auth.dependencies import get_access_token, get_user_repository
        token = get_access_token(request, None)
        user_repo = get_user_repository(db)
        return await get_current_user(token, user_repo)
    except Exception:
        return None


@router.post(
    "/devices/register",
    response_model=DeviceRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_device(
    data: DeviceRegisterRequest,
    current_user: User = Depends(get_current_user),
    service: TrackingService = Depends(get_tracking_service),
) -> Any:
    """Register client device, save installation ID, and enforce tier device limits."""
    return await service.register_device(current_user.id, data)


@router.post(
    "/sessions/start",
    response_model=SessionStartResponse,
    status_code=status.HTTP_201_CREATED,
)
async def start_session(
    data: SessionStartRequest,
    current_user: User = Depends(get_current_user),
    service: TrackingService = Depends(get_tracking_service),
) -> Any:
    """Record app launch session start time and update last active timestamp."""
    session_log = await service.start_session(current_user.id, data)
    return SessionStartResponse(
        session_id=session_log.id,
        session_start=session_log.session_start,
    )


@router.post(
    "/sessions/end",
    response_model=SessionEndResponse,
)
async def end_session(
    data: SessionEndRequest,
    current_user: User = Depends(get_current_user),
    service: TrackingService = Depends(get_tracking_service),
) -> Any:
    """Record app close session end time and calculate duration in seconds."""
    session_log = await service.end_session(current_user.id, data)
    return SessionEndResponse(
        session_id=session_log.id,
        session_start=session_log.session_start,
        session_end=session_log.session_end,
        duration_seconds=session_log.duration_seconds or 0,
    )


@router.post(
    "/usage/event",
    response_model=UsageStatsResponse,
)
async def track_usage_event(
    data: UsageTrackEventRequest,
    current_user: User = Depends(get_current_user),
    service: TrackingService = Depends(get_tracking_service),
) -> Any:
    """Track app feature usage counters (APP_OPEN, LOGIN, SCAN, LEAD_CREATED, BACKUP, SHEETS_SYNC)."""
    stats = await service.record_usage_event(current_user.id, data)
    return UsageStatsResponse(
        user_id=stats.user_id,
        total_app_opens=stats.total_app_opens,
        total_login_count=stats.total_login_count,
        total_scan_count=stats.total_scan_count,
        total_leads_created=stats.total_leads_created,
        total_backup_count=stats.total_backup_count,
        total_sheets_sync_count=stats.total_sheets_sync_count,
        last_active_at=stats.last_active_at,
    )


@router.get(
    "/subscription/status",
    response_model=SubscriptionStatusResponse,
)
async def get_subscription_status(
    current_user: User = Depends(get_current_user),
    service: TrackingService = Depends(get_tracking_service),
) -> Any:
    """Retrieve user subscription status, tier, and active device counts."""
    return await service.get_subscription_status(current_user.id)


@router.get(
    "/admin/dashboard",
    response_model=AdminDashboardAnalyticsResponse,
)
async def get_admin_dashboard(
    service: TrackingService = Depends(get_tracking_service),
) -> Any:
    """Retrieve live Admin Dashboard analytics (Online Users, Devices, Subscription breakdown, Usage Totals)."""
    return await service.get_admin_dashboard()
