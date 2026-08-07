import uuid
from abc import ABC, abstractmethod
from typing import Any


class IFrameProvider(ABC):
    """Interface for managing active streaming connection to camera hardware."""

    @abstractmethod
    async def start_stream(self, device_connection_id: str) -> bool:
        """Initialize and open the stream for the target device."""
        pass

    @abstractmethod
    async def stop_stream(self) -> bool:
        """Stop and release resources associated with the streaming interface."""
        pass

    @abstractmethod
    async def read_frame(self) -> bytes:
        """Acquire a single raw compressed frame buffer from the stream."""
        pass


class IFrameValidator(ABC):
    """Interface specifying standard image quality checks."""

    @abstractmethod
    async def validate_quality(self, frame: bytes) -> dict[str, Any]:
        """Perform blur, brightness, exposure, and perspective validations.

        Returns quality checklist dictionary with placeholder evaluations.
        """
        pass


class IFrameQueue(ABC):
    """Interface handling buffering and sequential queuing of frames."""

    @abstractmethod
    async def enqueue_frame(self, frame: bytes) -> None:
        """Buffer a newly received frame."""
        pass

    @abstractmethod
    async def dequeue_frame(self) -> bytes:
        """Extract the next buffered frame in FIFO order."""
        pass

    @abstractmethod
    async def clear_queue(self) -> None:
        """Purge all buffered frames."""
        pass


class IFrameDispatcher(ABC):
    """Interface coordinating frame delivery to downstream consumer handlers."""

    @abstractmethod
    async def dispatch_frame(
        self, frame: bytes, scanner_job_id: uuid.UUID
    ) -> Any:
        """Deliver the captured frame to the BF-001 scanner system."""
        pass


class ICameraControls(ABC):
    """Interface defining properties for adjusting hardware parameters."""

    @abstractmethod
    async def set_zoom(self, value: float) -> bool:
        """Set zoom scale level."""
        pass

    @abstractmethod
    async def set_focus(self, focus_mode: str) -> bool:
        """Adjust lens focus settings."""
        pass

    @abstractmethod
    async def toggle_flash(self, enabled: bool) -> bool:
        """Toggle camera flash state."""
        pass

    @abstractmethod
    async def toggle_torch(self, enabled: bool) -> bool:
        """Toggle torch/flashlight state."""
        pass

    @abstractmethod
    async def set_exposure(self, value: float) -> bool:
        """Adjust camera sensor exposure compensation."""
        pass

    @abstractmethod
    async def set_white_balance(self, mode: str) -> bool:
        """Adjust sensor white balance temperature settings."""
        pass

    @abstractmethod
    async def set_mirror(self, enabled: bool) -> bool:
        """Configure mirroring mapping overlays."""
        pass

    @abstractmethod
    async def set_orientation(self, degree: int) -> bool:
        """Set screen rendering rotation layout."""
        pass

    @abstractmethod
    async def select_lens(self, front: bool) -> bool:
        """Switch between front and rear cameras."""
        pass


class IPermissionManager(ABC):
    """Interface managing operating platform security validations."""

    @abstractmethod
    async def check_permission(self, platform: str) -> bool:
        """Evaluate if camera access permissions are currently granted."""
        pass

    @abstractmethod
    async def request_permission(self, platform: str) -> bool:
        """Trigger native system prompts requesting camera device access."""
        pass
