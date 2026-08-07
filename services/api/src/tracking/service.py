import uuid
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.tracking.models import UserDevice, UserSessionLog, UserUsageStats, UserSubscription
from services.api.src.tracking.repository import TrackingRepository
from services.api.src.tracking.schemas import (
    DeviceRegisterRequest,
    SessionStartRequest,
    SessionEndRequest,
    UsageTrackEventRequest,
)


class TrackingService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = TrackingRepository(db)

    async def register_device(self, user_id: uuid.UUID, data: DeviceRegisterRequest) -> UserDevice:
        subscription = await self.repository.ensure_default_subscription(user_id)
        existing_device = await self.repository.get_device_by_installation_id(data.installation_id)

        # Enforce device limit for new devices (Requirement 8)
        if not existing_device:
            active_count = await self.repository.count_active_devices_for_user(user_id)
            if active_count >= subscription.max_devices:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Device limit reached. Your {subscription.tier} subscription allows a maximum of {subscription.max_devices} device(s). Please upgrade to register more devices.",
                )

        device = await self.repository.register_device(
            user_id=user_id,
            installation_id=data.installation_id,
            device_model=data.device_model,
            manufacturer=data.manufacturer,
            os_version=data.os_version,
            app_version=data.app_version,
        )

        # Track LOGIN event metric
        await self.repository.record_event(user_id, "LOGIN")
        return device

    async def start_session(self, user_id: uuid.UUID, data: SessionStartRequest) -> UserSessionLog:
        device = await self.repository.get_device_by_installation_id(data.installation_id)
        if not device:
            # Auto-register fallback device if missing
            device = await self.repository.register_device(
                user_id=user_id,
                installation_id=data.installation_id,
                device_model="Generic Android Device",
                manufacturer="Android",
                os_version="14.0",
                app_version="1.0.0",
            )

        # Update last active time (Requirement 4)
        await self.repository.update_device_last_active(device.id)

        # Increment APP_OPEN metric
        await self.repository.record_event(user_id, "APP_OPEN")

        return await self.repository.start_session(user_id, device.id)

    async def end_session(self, user_id: uuid.UUID, data: SessionEndRequest) -> UserSessionLog:
        session_log = await self.repository.end_session(data.session_id, data.session_end)
        if not session_log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session log not found.",
            )
        return session_log

    async def record_usage_event(
        self, user_id: uuid.UUID, data: UsageTrackEventRequest
    ) -> UserUsageStats:
        if data.installation_id:
            device = await self.repository.get_device_by_installation_id(data.installation_id)
            if device:
                await self.repository.update_device_last_active(device.id)
        return await self.repository.record_event(user_id, data.event_type)

    async def get_subscription_status(self, user_id: uuid.UUID) -> dict:
        subscription = await self.repository.ensure_default_subscription(user_id)
        active_count = await self.repository.count_active_devices_for_user(user_id)
        return {
            "user_id": user_id,
            "tier": subscription.tier,
            "status": subscription.status,
            "max_devices": subscription.max_devices,
            "active_devices_count": active_count,
            "expires_at": subscription.expires_at,
        }

    async def get_admin_dashboard(self) -> dict:
        return await self.repository.get_admin_dashboard_metrics()
