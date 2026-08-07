# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.camera.repository import (
    CameraDeviceRepository,
    CaptureSessionRepository,
)
from services.api.src.camera.service import CameraService
from services.api.src.database import get_db


def get_camera_device_repository(
    session: AsyncSession = Depends(get_db),
) -> CameraDeviceRepository:
    """Inject CameraDeviceRepository context."""
    return CameraDeviceRepository(session)


def get_capture_session_repository(
    session: AsyncSession = Depends(get_db),
) -> CaptureSessionRepository:
    """Inject CaptureSessionRepository context."""
    return CaptureSessionRepository(session)


def get_camera_service(
    device_repo: CameraDeviceRepository = Depends(get_camera_device_repository),
    session_repo: CaptureSessionRepository = Depends(
        get_capture_session_repository
    ),
) -> CameraService:
    """Inject CameraService context."""
    return CameraService(device_repo, session_repo)
