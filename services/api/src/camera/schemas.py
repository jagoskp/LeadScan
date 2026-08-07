import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from services.api.src.camera.enums import (
    CameraResolution,
    CameraSourceType,
    CaptureMode,
    DeviceStatus,
    FrameRate,
    ImageFormat,
    PermissionPlatform,
)


class CameraDeviceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    connection_id: str = Field(..., min_length=1, max_length=255)
    source_type: CameraSourceType
    supported_resolutions: list[CameraResolution] = Field(default_factory=list)
    supported_framerates: list[FrameRate] = Field(default_factory=list)


class CameraDeviceUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    status: DeviceStatus | None = None
    is_active: bool | None = None


class CameraDeviceResponse(BaseModel):
    id: uuid.UUID
    name: str
    connection_id: str
    source_type: CameraSourceType
    status: DeviceStatus
    supported_resolutions: list[str] | None
    supported_framerates: list[str] | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CaptureSessionCreate(BaseModel):
    device_id: uuid.UUID
    mode: CaptureMode
    resolution: CameraResolution
    framerate: FrameRate
    format: ImageFormat
    organization_id: uuid.UUID | None = None


class CaptureSessionUpdate(BaseModel):
    is_active: bool


class CapturedFrameResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    file_path: str
    file_size: int | None
    width: int | None
    height: int | None
    quality_score: float | None
    quality_checks: dict[str, Any] | None
    created_at: datetime

    class Config:
        from_attributes = True


class CaptureSessionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    organization_id: uuid.UUID | None
    device_id: uuid.UUID | None
    mode: CaptureMode
    resolution: str
    framerate: str
    format: ImageFormat
    is_active: bool
    frames: list[CapturedFrameResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PermissionRequest(BaseModel):
    platform: PermissionPlatform


class PermissionResponse(BaseModel):
    platform: PermissionPlatform
    granted: bool


class CameraControlsUpdate(BaseModel):
    zoom: float | None = Field(None, ge=1.0, le=10.0)
    focus_mode: str | None = Field(None, max_length=50)
    flash: bool | None = None
    torch: bool | None = None
    exposure: float | None = Field(None, ge=-2.0, le=2.0)
    white_balance: str | None = Field(None, max_length=50)
    mirror: bool | None = None
    orientation: int | None = Field(None, ge=0, le=360)
    front_lens: bool | None = None
