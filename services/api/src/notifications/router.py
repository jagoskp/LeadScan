# ruff: noqa: B008
import uuid
from typing import Any
from fastapi import APIRouter, Depends, Query, status
from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.notifications.dependencies import get_notification_service
from services.api.src.notifications.service import NotificationService
from services.api.src.notifications.schemas import (
    NotificationCreate,
    NotificationResponse,
    NotificationListResponse,
    NotificationStatus,
    NotificationType,
    NotificationTemplateCreate,
    NotificationTemplateUpdate,
    NotificationTemplateResponse,
    NotificationPreferenceUpdate,
    NotificationPreferenceResponse,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


# ----------------------------------------------------
# Notification Preferences
# ----------------------------------------------------

@router.get("/preferences", response_model=list[NotificationPreferenceResponse])
async def get_my_preferences(
    organization_id: uuid.UUID | None = Query(
        None, description="Optional organization filter"
    ),
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """Retrieve all channel preferences for the user, optionally org-scoped."""
    return await service.get_preferences(current_user, organization_id)


@router.put("/preferences", response_model=NotificationPreferenceResponse)
async def update_my_preference(
    data: NotificationPreferenceUpdate,
    organization_id: uuid.UUID | None = Query(
        None, description="Optional organization scope"
    ),
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """Upsert preference settings for a channel and organization tenant."""
    return await service.update_preference(current_user, data, organization_id)


# ----------------------------------------------------
# Notification Templates
# ----------------------------------------------------

@router.post(
    "/templates",
    response_model=NotificationTemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_template(
    data: NotificationTemplateCreate,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """Create a new reusable notification message template."""
    return await service.create_template(current_user, data)


@router.get("/templates", response_model=list[NotificationTemplateResponse])
async def list_templates(
    organization_id: uuid.UUID | None = Query(
        None, description="Scope templates list to an organization"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """Retrieve a list of templates available to the user and org."""
    return await service.list_templates(current_user, organization_id, skip, limit)


@router.get("/templates/{template_id}", response_model=NotificationTemplateResponse)
async def get_template(
    template_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """Retrieve a specific notification template detail."""
    return await service.get_template(template_id, current_user)


@router.put("/templates/{template_id}", response_model=NotificationTemplateResponse)
async def update_template(
    template_id: uuid.UUID,
    data: NotificationTemplateUpdate,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """Update details of an existing notification template."""
    return await service.update_template(template_id, current_user, data)


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> None:
    """Remove a notification template."""
    await service.delete_template(template_id, current_user)


# ----------------------------------------------------
# Notifications Lifecycle Endpoints
# ----------------------------------------------------

@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_notification(
    data: NotificationCreate,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """Trigger, render, and enqueue a notification to the recipient."""
    return await service.create_notification(current_user, data)


@router.get("", response_model=NotificationListResponse)
async def list_notifications(
    status: NotificationStatus | None = Query(
        None, description="Filter by status (e.g. READ, DELIVERED)"
    ),
    notification_type: NotificationType | None = Query(
        None, description="Filter by notification channel"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """List paginated notifications for user and organization context."""
    items, total = await service.list_notifications(
        current_user, status, notification_type, skip, limit
    )
    return NotificationListResponse(
        items=[NotificationResponse.model_validate(item) for item in items],
        total=total,
        page=skip // limit + 1,
        size=limit,
    )


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """Retrieve detailed state and logs of a single notification."""
    return await service.get_notification(notification_id, current_user)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_as_read(
    notification_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """Mark a notification log status to READ."""
    return await service.mark_as_read(notification_id, current_user)


@router.patch("/{notification_id}/unread", response_model=NotificationResponse)
async def mark_as_unread(
    notification_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> Any:
    """Mark a notification log status back to UNREAD (DELIVERED)."""
    return await service.mark_as_unread(notification_id, current_user)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> None:
    """Hard delete a notification record from logs."""
    await service.delete_notification(notification_id, current_user)
