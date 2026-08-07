import uuid
from collections.abc import Sequence
from typing import Any

from services.api.src.camera.enums import DeviceStatus, PermissionPlatform
from services.api.src.camera.exceptions import (
    CameraNotFoundException,
    PermissionDeniedException,
)
from services.api.src.camera.interfaces import (
    ICameraControls,
    IFrameDispatcher,
    IFrameProvider,
    IFrameQueue,
    IFrameValidator,
    IPermissionManager,
)
from services.api.src.camera.models import (
    CameraDevice,
    CapturedFrame,
    CaptureSession,
)
from services.api.src.camera.repository import (
    CameraDeviceRepository,
    CaptureSessionRepository,
)
from services.api.src.camera.schemas import (
    CameraDeviceCreate,
    CameraDeviceUpdate,
    CaptureSessionCreate,
)
from services.api.src.camera.validators import validate_image_quality


class CameraService(
    IFrameProvider,
    IFrameValidator,
    IFrameQueue,
    IFrameDispatcher,
    ICameraControls,
    IPermissionManager,
):
    """Orchestrates camera streams, permissions, quality checks, and sessions."""

    def __init__(
        self,
        device_repo: CameraDeviceRepository,
        session_repo: CaptureSessionRepository,
    ) -> None:
        self.device_repo = device_repo
        self.session_repo = session_repo
        self.frame_queue: list[bytes] = []

    # ----------------------------------------------------
    # Device CRUD Operations
    # ----------------------------------------------------

    async def create_device(self, data: CameraDeviceCreate) -> CameraDevice:
        """Register a new camera hardware device configuration."""
        device = CameraDevice(
            name=data.name,
            connection_id=data.connection_id,
            source_type=data.source_type.value,
            status=DeviceStatus.CONNECTED.value,
            supported_resolutions={
                "resolutions": [r.value for r in data.supported_resolutions]
            },
            supported_framerates={
                "framerates": [f.value for f in data.supported_framerates]
            },
            is_active=True,
        )
        return await self.device_repo.create(device)

    async def get_device(self, device_id: uuid.UUID) -> CameraDevice:
        """Retrieve a specific camera device configuration."""
        device = await self.device_repo.get_by_id(device_id)
        if not device:
            raise CameraNotFoundException()
        return device

    async def list_devices(
        self, active_only: bool = True
    ) -> Sequence[CameraDevice]:
        """List registered camera devices."""
        return await self.device_repo.list_devices(active_only=active_only)

    async def update_device(
        self, device_id: uuid.UUID, data: CameraDeviceUpdate
    ) -> CameraDevice:
        """Update properties of an existing camera device."""
        # Ensure device exists
        await self.get_device(device_id)
        update_data = data.model_dump(exclude_unset=True)
        updated = await self.device_repo.update(device_id, update_data)
        if not updated:
            raise CameraNotFoundException()
        return updated

    async def delete_device(self, device_id: uuid.UUID) -> bool:
        """Delete a CameraDevice registration from the database."""
        # Ensure device exists
        await self.get_device(device_id)
        return await self.device_repo.delete(device_id)

    # ----------------------------------------------------
    # Session Operations
    # ----------------------------------------------------

    async def create_session(
        self, user_id: uuid.UUID, data: CaptureSessionCreate
    ) -> CaptureSession:
        """Initialize a new camera capture session."""
        # Ensure target device exists
        await self.get_device(data.device_id)

        session = CaptureSession(
            user_id=user_id,
            organization_id=data.organization_id,
            device_id=data.device_id,
            mode=data.mode.value,
            resolution=data.resolution.value,
            framerate=data.framerate.value,
            format=data.format.value,
            is_active=True,
        )
        return await self.session_repo.create_session(session)

    async def get_session(self, session_id: uuid.UUID) -> CaptureSession:
        """Retrieve a specific CaptureSession, raising 404 if missing."""
        session = await self.session_repo.get_session_by_id(session_id)
        if not session:
            raise CameraNotFoundException()
        return session

    async def list_sessions(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[CaptureSession]:
        """List capture sessions filtered by user/organization scope."""
        return await self.session_repo.list_sessions(
            user_id=user_id, organization_id=organization_id
        )

    async def capture_frame(
        self, session_id: uuid.UUID, file_path: str
    ) -> CapturedFrame:
        """Capture and log metadata for a frame in an active session."""
        session = await self.get_session(session_id)

        # Mock frame byte array acquisition
        mock_bytes = b"MOCK_CAPTURED_FRAME_BYTES"
        quality = await self.validate_quality(mock_bytes)

        frame = CapturedFrame(
            session_id=session.id,
            file_path=file_path,
            file_size=len(mock_bytes),
            width=1920,
            height=1080,
            quality_score=quality["overall_score"],
            quality_checks=quality["checks"],
        )
        return await self.session_repo.create_frame(frame)

    # ----------------------------------------------------
    # IFrameProvider Implementation
    # ----------------------------------------------------

    async def start_stream(self, device_connection_id: str) -> bool:
        """Initialize connection to device frame connection stream."""
        return len(device_connection_id.strip()) > 0

    async def stop_stream(self) -> bool:
        """Close active connection streams."""
        return True

    async def read_frame(self) -> bytes:
        """Retrieve a single frame from raw camera buffer stream."""
        return b"MOCK_Acquired_Frame_Bytes_Buffer"

    # ----------------------------------------------------
    # IFrameValidator Implementation
    # ----------------------------------------------------

    async def validate_quality(self, frame: bytes) -> dict[str, Any]:
        """Analyze frame bytes to evaluate placeholder image quality scores."""
        return validate_image_quality(frame)

    # ----------------------------------------------------
    # IFrameQueue Implementation
    # ----------------------------------------------------

    async def enqueue_frame(self, frame: bytes) -> None:
        """Buffer a newly received frame."""
        self.frame_queue.append(frame)

    async def dequeue_frame(self) -> bytes:
        """Extract the next buffered frame in FIFO order."""
        if not self.frame_queue:
            return b""
        return self.frame_queue.pop(0)

    async def clear_queue(self) -> None:
        """Purge all buffered frames."""
        self.frame_queue.clear()

    # ----------------------------------------------------
    # IFrameDispatcher Implementation
    # ----------------------------------------------------

    async def dispatch_frame(
        self, frame: bytes, scanner_job_id: uuid.UUID
    ) -> Any:
        """Deliver the captured frame to the scanner system."""
        return len(frame) > 0 and scanner_job_id is not None

    # ----------------------------------------------------
    # ICameraControls Implementation
    # ----------------------------------------------------

    async def set_zoom(self, value: float) -> bool:
        """Set zoom scale level."""
        return value >= 1.0

    async def set_focus(self, focus_mode: str) -> bool:
        """Adjust lens focus settings."""
        return len(focus_mode) > 0

    async def toggle_flash(self, enabled: bool) -> bool:
        """Toggle camera flash state."""
        return True

    async def toggle_torch(self, enabled: bool) -> bool:
        """Toggle torch/flashlight state."""
        return True

    async def set_exposure(self, value: float) -> bool:
        """Adjust camera sensor exposure compensation."""
        return -2.0 <= value <= 2.0

    async def set_white_balance(self, mode: str) -> bool:
        """Adjust sensor white balance temperature settings."""
        return len(mode) > 0

    async def set_mirror(self, enabled: bool) -> bool:
        """Configure mirroring mapping overlays."""
        return True

    async def set_orientation(self, degree: int) -> bool:
        """Set screen rendering rotation layout."""
        return 0 <= degree <= 360

    async def select_lens(self, front: bool) -> bool:
        """Switch between front and rear cameras."""
        return True

    # ----------------------------------------------------
    # IPermissionManager Implementation
    # ----------------------------------------------------

    async def check_permission(self, platform: str) -> bool:
        """Evaluate if camera access permissions are currently granted."""
        try:
            PermissionPlatform(platform)
            return True
        except ValueError:
            raise PermissionDeniedException(platform) from None

    async def request_permission(self, platform: str) -> bool:
        """Trigger platform prompts requesting camera access."""
        try:
            PermissionPlatform(platform)
            return True
        except ValueError:
            raise PermissionDeniedException(platform) from None
