# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.notifications.repository import (
    NotificationPreferenceRepository,
    NotificationRepository,
    NotificationTemplateRepository,
)
from services.api.src.notifications.service import NotificationService


def get_notification_repository(
    session: AsyncSession = Depends(get_db),
) -> NotificationRepository:
    """Inject NotificationRepository context."""
    return NotificationRepository(session)


def get_notification_template_repository(
    session: AsyncSession = Depends(get_db),
) -> NotificationTemplateRepository:
    """Inject NotificationTemplateRepository context."""
    return NotificationTemplateRepository(session)


def get_notification_preference_repository(
    session: AsyncSession = Depends(get_db),
) -> NotificationPreferenceRepository:
    """Inject NotificationPreferenceRepository context."""
    return NotificationPreferenceRepository(session)


def get_notification_service(
    notification_repo: NotificationRepository = Depends(get_notification_repository),
    template_repo: NotificationTemplateRepository = Depends(
        get_notification_template_repository
    ),
    preference_repo: NotificationPreferenceRepository = Depends(
        get_notification_preference_repository
    ),
) -> NotificationService:
    """Inject NotificationService context."""
    return NotificationService(notification_repo, template_repo, preference_repo)
