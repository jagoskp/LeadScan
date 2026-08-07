import re
import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class NotificationType(StrEnum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"
    IN_APP = "IN_APP"
    WEBHOOK = "WEBHOOK"


class NotificationPriority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class NotificationStatus(StrEnum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    READ = "READ"


# ----------------------------------------------------
# Notification Template Schemas
# ----------------------------------------------------

class NotificationTemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)
    notification_type: NotificationType
    title_template: str | None = Field(None, max_length=255)
    body_template: str = Field(..., min_length=1, max_length=4000)
    variables: list[str] = Field(default_factory=list)
    is_active: bool = True


class NotificationTemplateCreate(NotificationTemplateBase):
    organization_id: uuid.UUID | None = None


class NotificationTemplateUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)
    notification_type: NotificationType | None = None
    title_template: str | None = Field(None, max_length=255)
    body_template: str | None = Field(None, min_length=1, max_length=4000)
    variables: list[str] | None = None
    is_active: bool | None = None


class NotificationTemplateResponse(NotificationTemplateBase):
    id: uuid.UUID
    organization_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Notification Preference Schemas
# ----------------------------------------------------

class NotificationPreferenceBase(BaseModel):
    notification_type: NotificationType
    channel_enabled: bool = True
    preferences: dict[str, Any] = Field(default_factory=dict)


class NotificationPreferenceUpdate(BaseModel):
    notification_type: NotificationType
    channel_enabled: bool
    preferences: dict[str, Any] | None = None


class NotificationPreferenceResponse(NotificationPreferenceBase):
    id: uuid.UUID
    user_id: uuid.UUID
    organization_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Notification Schemas
# ----------------------------------------------------

class NotificationCreate(BaseModel):
    user_id: uuid.UUID
    organization_id: uuid.UUID | None = None
    template_id: uuid.UUID | None = None
    template_name: str | None = Field(
        None, description="Alternative lookup by template name"
    )
    notification_type: NotificationType
    recipient: str = Field(..., min_length=1, max_length=512)
    priority: NotificationPriority = NotificationPriority.MEDIUM
    title: str | None = Field(None, max_length=255)
    body: str | None = Field(
        None, description="Required if not template metadata is supplied"
    )
    template_variables: dict[str, Any] = Field(default_factory=dict)
    queue_metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_body_or_template(self) -> "NotificationCreate":
        """Ensure body is present if template elements are not provided."""
        if not self.body and not self.template_id and not self.template_name:
            raise ValueError(
                "Either 'body' must be provided, "
                "or 'template_id' / 'template_name' must be specified"
            )
        return self

    @field_validator("recipient")
    @classmethod
    def validate_recipient_format(cls, v: str, info: Any) -> str:
        """Validate recipient format matching the notification channel constraints."""
        notification_type = info.data.get("notification_type")
        if not notification_type:
            return v

        if notification_type == NotificationType.EMAIL:
            email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if not re.match(email_regex, v):
                raise ValueError(
                    "Recipient must be a valid email address for EMAIL notifications"
                )
        elif notification_type == NotificationType.SMS:
            sms_regex = r"^\+?[1-9]\d{1,14}$"
            if not re.match(sms_regex, v):
                raise ValueError(
                    "Recipient must be a valid E.164 phone number for SMS notifications"
                )
        elif notification_type == NotificationType.WEBHOOK:
            if not (v.startswith("http://") or v.startswith("https://")):
                raise ValueError(
                    "Recipient must be a valid HTTP/HTTPS URL for WEBHOOK notifications"
                )
        # PUSH and IN_APP do not have strict global constraints
        # (can be device tokens, user IDs)
        return v


class NotificationHistoryItem(BaseModel):
    status: NotificationStatus
    timestamp: datetime
    changed_by: str | None = None
    reason: str | None = None


class NotificationResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    organization_id: uuid.UUID | None
    template_id: uuid.UUID | None
    notification_type: NotificationType
    recipient: str
    priority: NotificationPriority
    status: NotificationStatus
    title: str | None
    body: str
    queue_metadata: dict[str, Any]
    status_history: list[NotificationHistoryItem]
    created_at: datetime
    updated_at: datetime
    sent_at: datetime | None
    delivered_at: datetime | None
    read_at: datetime | None

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    page: int
    size: int
