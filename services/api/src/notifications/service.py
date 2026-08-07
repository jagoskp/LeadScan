import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from services.api.src.auth.models import User
from services.api.src.notifications.exceptions import (
    NotificationNotFoundException,
    PreferenceDisabledException,
    TemplateNotFoundException,
    TemplateValidationException,
)
from services.api.src.notifications.models import (
    Notification,
    NotificationPreference,
    NotificationTemplate,
)
from services.api.src.notifications.repository import (
    NotificationPreferenceRepository,
    NotificationRepository,
    NotificationTemplateRepository,
)
from services.api.src.notifications.schemas import (
    NotificationCreate,
    NotificationPreferenceUpdate,
    NotificationStatus,
    NotificationTemplateCreate,
    NotificationTemplateUpdate,
    NotificationType,
)


class NotificationService:
    """Service orchestrating notifications, templates, and preferences."""

    def __init__(
        self,
        notification_repo: NotificationRepository,
        template_repo: NotificationTemplateRepository,
        preference_repo: NotificationPreferenceRepository,
    ) -> None:
        self.notification_repo = notification_repo
        self.template_repo = template_repo
        self.preference_repo = preference_repo

    def _get_user_organization_ids(self, user: User) -> list[uuid.UUID]:
        """Helper to extract organization IDs where the user has active membership."""
        return [m.organization_id for m in getattr(user, "memberships", [])]

    # ----------------------------------------------------
    # Notification Preferences
    # ----------------------------------------------------

    async def get_preferences(
        self, user: User, organization_id: uuid.UUID | None = None
    ) -> Sequence[NotificationPreference]:
        """Fetch all notification preferences for a user in an org context."""
        org_ids = self._get_user_organization_ids(user)
        if organization_id and organization_id not in org_ids:
            organization_id = None

        return await self.preference_repo.get_by_user_id(user.id, organization_id)

    async def update_preference(
        self,
        user: User,
        data: NotificationPreferenceUpdate,
        organization_id: uuid.UUID | None = None,
    ) -> NotificationPreference:
        """Upsert a user's notification channel preference settings."""
        org_ids = self._get_user_organization_ids(user)
        if organization_id and organization_id not in org_ids:
            raise NotificationNotFoundException()

        return await self.preference_repo.upsert_preference(
            user_id=user.id,
            notification_type=data.notification_type.value,
            channel_enabled=data.channel_enabled,
            preferences=data.preferences,
            organization_id=organization_id,
        )

    # ----------------------------------------------------
    # Notification Templates
    # ----------------------------------------------------

    async def create_template(
        self, user: User, data: NotificationTemplateCreate
    ) -> NotificationTemplate:
        """Create a new template, verifying organization ownership if scoped."""
        org_ids = self._get_user_organization_ids(user)
        if data.organization_id and data.organization_id not in org_ids:
            raise TemplateNotFoundException()

        template = NotificationTemplate(
            organization_id=data.organization_id,
            name=data.name,
            description=data.description,
            notification_type=data.notification_type.value,
            title_template=data.title_template,
            body_template=data.body_template,
            variables=data.variables,
            is_active=data.is_active,
        )
        return await self.template_repo.create(template)

    async def get_template(
        self, template_id: uuid.UUID, user: User
    ) -> NotificationTemplate:
        """Retrieve a notification template by ID, verifying tenant scope."""
        template = await self.template_repo.get_by_id(template_id)
        if not template:
            raise TemplateNotFoundException()

        org_ids = self._get_user_organization_ids(user)
        if template.organization_id and template.organization_id not in org_ids:
            raise TemplateNotFoundException()

        return template

    async def list_templates(
        self,
        user: User,
        organization_id: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[NotificationTemplate]:
        """List all active templates accessible by the user."""
        org_ids = self._get_user_organization_ids(user)
        if organization_id and organization_id not in org_ids:
            organization_id = None

        return await self.template_repo.list_templates(
            organization_id=organization_id, skip=skip, limit=limit
        )

    async def update_template(
        self, template_id: uuid.UUID, user: User, data: NotificationTemplateUpdate
    ) -> NotificationTemplate:
        """Modify fields on an existing template, ensuring tenant restrictions."""
        await self.get_template(template_id, user)

        update_dict = data.model_dump(exclude_unset=True)
        if (
            "notification_type" in update_dict
            and update_dict["notification_type"] is not None
        ):
            update_dict["notification_type"] = update_dict[
                "notification_type"
            ].value

        updated = await self.template_repo.update(template_id, update_dict)
        if not updated:
            raise TemplateNotFoundException()
        return updated

    async def delete_template(self, template_id: uuid.UUID, user: User) -> None:
        """Delete template by ID, ensuring tenant access rules."""
        await self.get_template(template_id, user)
        await self.template_repo.delete(template_id)

    # ----------------------------------------------------
    # Notifications Lifecycle
    # ----------------------------------------------------

    def _render_template(
        self, template: NotificationTemplate, variables: dict[str, Any]
    ) -> tuple[str | None, str]:
        """Validate placeholders and format template body and title."""
        missing = [v for v in template.variables if v not in variables]
        if missing:
            raise TemplateValidationException(
                f"Missing required template parameters: {', '.join(missing)}"
            )

        body = template.body_template
        title = template.title_template

        for key, val in variables.items():
            placeholder = f"{{{{{key}}}}}"
            body = body.replace(placeholder, str(val))
            if title:
                title = title.replace(placeholder, str(val))

        return title, body

    async def create_notification(
        self, user: User, data: NotificationCreate
    ) -> Notification:
        """Initialize, validate, render, and enqueue a notification record."""
        org_ids = self._get_user_organization_ids(user)
        if data.organization_id and data.organization_id not in org_ids:
            raise NotificationNotFoundException()

        # 1. Check Channel Preferences
        preference = await self.preference_repo.get_by_user_and_type(
            user_id=data.user_id,
            notification_type=data.notification_type.value,
            organization_id=data.organization_id,
        )
        if preference and not preference.channel_enabled:
            raise PreferenceDisabledException(data.notification_type.value)

        # 2. Resolve Template & Content Rendering
        template_id = data.template_id
        rendered_title = data.title
        rendered_body = data.body

        if data.template_id or data.template_name:
            template = None
            if data.template_id:
                template = await self.template_repo.get_by_id(data.template_id)
            elif data.template_name:
                template = await self.template_repo.get_by_name(
                    data.template_name, organization_id=data.organization_id
                )

            if not template:
                raise TemplateNotFoundException()

            template_id = template.id
            rendered_title, rendered_body = self._render_template(
                template, data.template_variables
            )

        if rendered_body is None:
            raise TemplateValidationException(
                "Rendering resulted in empty notification body content"
            )

        # 3. Build Notification Record in PENDING state
        now = datetime.now(UTC)
        history_log = [
            {
                "status": NotificationStatus.PENDING.value,
                "timestamp": now.isoformat(),
                "changed_by": "SYSTEM",
                "reason": "Notification created and validated.",
            }
        ]

        notification = Notification(
            user_id=data.user_id,
            organization_id=data.organization_id,
            template_id=template_id,
            notification_type=data.notification_type.value,
            recipient=data.recipient,
            priority=data.priority.value,
            status=NotificationStatus.PENDING.value,
            title=rendered_title,
            body=rendered_body,
            queue_metadata=data.queue_metadata or {},
            status_history=history_log,
        )

        created_notification = await self.notification_repo.create(notification)

        # 4. Orchestrate Queue Placement / Metadata Simulation
        job_id = f"job_{uuid.uuid4().hex[:12]}"
        simulated_queue_meta = {
            "job_id": job_id,
            "queue_name": f"notifications_{data.notification_type.value.lower()}_queue",
            "enqueued_at": datetime.now(UTC).isoformat(),
            "attempts": 1,
        }

        merged_meta = dict(data.queue_metadata)
        merged_meta.update(simulated_queue_meta)

        queued_log = {
            "status": NotificationStatus.QUEUED.value,
            "timestamp": datetime.now(UTC).isoformat(),
            "changed_by": "SYSTEM",
            "reason": f"Dispatched to queue worker with identifier {job_id}",
        }

        # Transition to QUEUED
        updated_notification = await self.notification_repo.update_status(
            notification_id=created_notification.id,
            status=NotificationStatus.QUEUED.value,
            queue_metadata=merged_meta,
            history_item=queued_log,
        )

        return updated_notification or created_notification

    async def get_notification(
        self, notification_id: uuid.UUID, user: User
    ) -> Notification:
        """Fetch notification, checking ownership or memberships."""
        notification = await self.notification_repo.get_by_id(notification_id)
        if not notification:
            raise NotificationNotFoundException()

        org_ids = self._get_user_organization_ids(user)
        if notification.user_id != user.id:
            if (
                not notification.organization_id
                or notification.organization_id not in org_ids
            ):
                raise NotificationNotFoundException()

        return notification

    async def list_notifications(
        self,
        user: User,
        status: NotificationStatus | None = None,
        notification_type: NotificationType | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[Notification], int]:
        """List paginated notifications query result for the user's scope."""
        org_ids = self._get_user_organization_ids(user)
        status_val = status.value if status else None
        type_val = notification_type.value if notification_type else None

        return await self.notification_repo.list_notifications(
            user_id=user.id,
            organization_ids=org_ids,
            status=status_val,
            notification_type=type_val,
            skip=skip,
            limit=limit,
        )

    async def mark_as_read(
        self, notification_id: uuid.UUID, user: User
    ) -> Notification:
        """Mark notification status to READ and record read timestamp."""
        await self.get_notification(notification_id, user)

        read_log = {
            "status": NotificationStatus.READ.value,
            "timestamp": datetime.now(UTC).isoformat(),
            "changed_by": str(user.id),
            "reason": "Marked read by user API request",
        }

        updated = await self.notification_repo.update_status(
            notification_id=notification_id,
            status=NotificationStatus.READ.value,
            history_item=read_log,
        )
        if not updated:
            raise NotificationNotFoundException()
        return updated

    async def mark_as_unread(
        self, notification_id: uuid.UUID, user: User
    ) -> Notification:
        """Revert status from READ to DELIVERED and clear read_at timestamp."""
        notification = await self.get_notification(notification_id, user)

        unread_log = {
            "status": NotificationStatus.DELIVERED.value,
            "timestamp": datetime.now(UTC).isoformat(),
            "changed_by": str(user.id),
            "reason": "Marked unread by user API request",
        }

        notification.read_at = None
        updated = await self.notification_repo.update_status(
            notification_id=notification_id,
            status=NotificationStatus.DELIVERED.value,
            history_item=unread_log,
        )
        if not updated:
            raise NotificationNotFoundException()
        return updated

    async def delete_notification(
        self, notification_id: uuid.UUID, user: User
    ) -> None:
        """Delete notification metadata log from storage."""
        await self.get_notification(notification_id, user)
        await self.notification_repo.delete(notification_id)
