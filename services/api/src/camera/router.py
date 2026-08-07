# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.camera.dependencies import get_camera_service
from services.api.src.camera.schemas import (
    CameraControlsUpdate,
    CameraDeviceCreate,
    CameraDeviceResponse,
    CameraDeviceUpdate,
    CapturedFrameResponse,
    CaptureSessionCreate,
    CaptureSessionResponse,
    PermissionRequest,
    PermissionResponse,
)
from services.api.src.camera.service import CameraService

router = APIRouter(prefix="/camera", tags=["camera"])


# ----------------------------------------------------
# Camera Devices Endpoints
# ----------------------------------------------------

@router.post(
    "/devices",
    response_model=CameraDeviceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_device(
    data: CameraDeviceCreate,
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> Any:
    """Register a new camera capture device config."""
    return await service.create_device(data)


@router.get("/devices", response_model=list[CameraDeviceResponse])
async def list_devices(
    active_only: bool = Query(True, description="Filter active devices only"),
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> Any:
    """List registered camera devices."""
    return await service.list_devices(active_only=active_only)


@router.get("/devices/{device_id}", response_model=CameraDeviceResponse)
async def get_device(
    device_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> Any:
    """Retrieve detailed properties of a registered camera device."""
    return await service.get_device(device_id)


@router.patch("/devices/{device_id}", response_model=CameraDeviceResponse)
async def update_device(
    device_id: uuid.UUID,
    data: CameraDeviceUpdate,
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> Any:
    """Update camera device properties or status configurations."""
    return await service.update_device(device_id, data)


@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> None:
    """Unregister and remove a camera device configuration."""
    await service.delete_device(device_id)


# ----------------------------------------------------
# Capture Sessions Endpoints
# ----------------------------------------------------

@router.post(
    "/sessions",
    response_model=CaptureSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def start_capture_session(
    data: CaptureSessionCreate,
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> Any:
    """Initialize a new camera capture session context."""
    return await service.create_session(user_id=current_user.id, data=data)


@router.get("/sessions", response_model=list[CaptureSessionResponse])
async def list_capture_sessions(
    organization_id: uuid.UUID | None = Query(
        None, description="Filter by organization"
    ),
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> Any:
    """List capture sessions filtered by organizational boundaries."""
    return await service.list_sessions(
        user_id=current_user.id, organization_id=organization_id
    )


@router.get("/sessions/{session_id}", response_model=CaptureSessionResponse)
async def get_capture_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> Any:
    """Retrieve detailed metadata properties of a single capture session."""
    return await service.get_session(session_id)


@router.post(
    "/sessions/{session_id}/capture",
    response_model=CapturedFrameResponse,
    status_code=status.HTTP_201_CREATED,
)
async def capture_session_frame(
    session_id: uuid.UUID,
    file_path: str = Query(..., description="Destination file storage path"),
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> Any:
    """Acquire and log a frame within the active capture session."""
    return await service.capture_frame(session_id, file_path)


# ----------------------------------------------------
# Camera Controls Endpoints
# ----------------------------------------------------

@router.post("/devices/{device_id}/controls")
async def update_camera_controls(
    device_id: uuid.UUID,
    controls: CameraControlsUpdate,
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> Any:
    """Adjust settings of camera devices (zoom, flash, white balance)."""
    # Ensure device exists
    await service.get_device(device_id)

    # Perform interface actions
    if controls.zoom is not None:
        await service.set_zoom(controls.zoom)
    if controls.focus_mode is not None:
        await service.set_focus(controls.focus_mode)
    if controls.flash is not None:
        await service.toggle_flash(controls.flash)
    if controls.torch is not None:
        await service.toggle_torch(controls.torch)
    if controls.exposure is not None:
        await service.set_exposure(controls.exposure)
    if controls.white_balance is not None:
        await service.set_white_balance(controls.white_balance)
    if controls.mirror is not None:
        await service.set_mirror(controls.mirror)
    if controls.orientation is not None:
        await service.set_orientation(controls.orientation)
    if controls.front_lens is not None:
        await service.select_lens(controls.front_lens)

    return {"success": True, "device_id": device_id}


# ----------------------------------------------------
# Permissions Endpoints
# ----------------------------------------------------

@router.post("/permissions", response_model=PermissionResponse)
async def request_platform_permission(
    payload: PermissionRequest,
    current_user: User = Depends(get_current_user),
    service: CameraService = Depends(get_camera_service),
) -> Any:
    """Evaluate or request camera permissions on the target platform."""
    platform_name = payload.platform.value
    # Assert check permission runs successfully
    await service.check_permission(platform_name)
    granted = await service.request_permission(platform_name)
    return PermissionResponse(platform=payload.platform, granted=granted)
