import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DeviceRegisterRequest(BaseModel):
    installation_id: str
    device_model: str
    manufacturer: str
    os_version: str
    app_version: str

    model_config = ConfigDict(from_attributes=True)


class DeviceRegisterResponse(BaseModel):
    id: uuid.UUID
    installation_id: str
    device_model: str
    manufacturer: str
    os_version: str
    app_version: str
    is_active: bool
    last_active_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionStartRequest(BaseModel):
    installation_id: str

    model_config = ConfigDict(from_attributes=True)


class SessionStartResponse(BaseModel):
    session_id: uuid.UUID
    session_start: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionEndRequest(BaseModel):
    session_id: uuid.UUID
    session_end: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class SessionEndResponse(BaseModel):
    session_id: uuid.UUID
    session_start: datetime
    session_end: datetime
    duration_seconds: int

    model_config = ConfigDict(from_attributes=True)


class UsageTrackEventRequest(BaseModel):
    event_type: str  # APP_OPEN, LOGIN, SCAN, LEAD_CREATED, BACKUP, SHEETS_SYNC
    installation_id: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UsageStatsResponse(BaseModel):
    user_id: uuid.UUID
    total_app_opens: int
    total_login_count: int
    total_scan_count: int
    total_leads_created: int
    total_backup_count: int
    total_sheets_sync_count: int
    last_active_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SubscriptionStatusResponse(BaseModel):
    user_id: uuid.UUID
    tier: str
    status: str
    max_devices: int
    active_devices_count: int
    expires_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserActivitySummary(BaseModel):
    user_id: uuid.UUID
    email: str
    display_name: str
    last_active_at: datetime
    registered_devices_count: int
    subscription_tier: str

    model_config = ConfigDict(from_attributes=True)


class AdminDashboardAnalyticsResponse(BaseModel):
    online_users_count: int
    total_registered_users: int
    total_registered_devices: int
    subscriptions_breakdown: dict[str, int]
    usage_totals: dict[str, int]
    last_active_users: list[UserActivitySummary]

    model_config = ConfigDict(from_attributes=True)
