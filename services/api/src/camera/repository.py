import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.camera.models import (
    CameraDevice,
    CapturedFrame,
    CaptureSession,
)


class CameraDeviceRepository:
    """Repository handling persistence operations for registered camera devices."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, device: CameraDevice) -> CameraDevice:
        """Persist a new CameraDevice configuration."""
        self.session.add(device)
        await self.session.flush()
        return device

    async def get_by_id(self, device_id: uuid.UUID) -> CameraDevice | None:
        """Retrieve a specific CameraDevice by ID."""
        stmt = select(CameraDevice).where(CameraDevice.id == device_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_devices(
        self, active_only: bool = True
    ) -> Sequence[CameraDevice]:
        """List registered camera devices."""
        stmt = select(CameraDevice)
        if active_only:
            stmt = stmt.where(CameraDevice.is_active.is_(True))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(
        self, device_id: uuid.UUID, data: dict[str, Any]
    ) -> CameraDevice | None:
        """Update properties of an existing camera device."""
        if data:
            stmt = (
                update(CameraDevice)
                .where(CameraDevice.id == device_id)
                .values(**data)
            )
            await self.session.execute(stmt)
        return await self.get_by_id(device_id)

    async def delete(self, device_id: uuid.UUID) -> bool:
        """Delete a CameraDevice configuration from the database."""
        stmt = delete(CameraDevice).where(CameraDevice.id == device_id)
        result = await self.session.execute(stmt)
        return bool(getattr(result, "rowcount", 0))


class CaptureSessionRepository:
    """Repository handling persistence operations for CaptureSessions and frames."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_session(self, session: CaptureSession) -> CaptureSession:
        """Persist a new CaptureSession."""
        self.session.add(session)
        await self.session.flush()
        return session

    async def get_session_by_id(self, session_id: uuid.UUID) -> CaptureSession | None:
        """Retrieve a CaptureSession preloading frame metadata records."""
        stmt = (
            select(CaptureSession)
            .where(CaptureSession.id == session_id)
            .options(selectinload(CaptureSession.frames))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_sessions(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[CaptureSession]:
        """List capture sessions filtered by scope boundaries."""
        stmt = select(CaptureSession).options(selectinload(CaptureSession.frames))
        filters = []
        if user_id:
            filters.append(CaptureSession.user_id == user_id)
        if organization_id:
            filters.append(CaptureSession.organization_id == organization_id)
        if filters:
            stmt = stmt.where(and_(*filters))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_session(
        self, session_id: uuid.UUID, data: dict[str, Any]
    ) -> CaptureSession | None:
        """Update session fields."""
        if data:
            stmt = (
                update(CaptureSession)
                .where(CaptureSession.id == session_id)
                .values(**data)
            )
            await self.session.execute(stmt)
        return await self.get_session_by_id(session_id)

    async def create_frame(self, frame: CapturedFrame) -> CapturedFrame:
        """Persist a new CapturedFrame record."""
        self.session.add(frame)
        await self.session.flush()
        return frame
