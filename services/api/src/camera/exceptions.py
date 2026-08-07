from fastapi import HTTPException, status


class CameraModuleException(HTTPException):
    """Base exception for all camera module errors."""
    pass


class CameraNotFoundException(CameraModuleException):
    """Exception raised when a requested camera device cannot be found."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera device not found",
        )


class PermissionDeniedException(CameraModuleException):
    """Exception raised when camera access permissions are denied."""

    def __init__(self, platform: str = "target platform") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Camera access permission denied on {platform}",
        )


class CameraBusyException(CameraModuleException):
    """Exception raised when a camera device is occupied by another process."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Camera device is currently busy",
        )


class LowResolutionException(CameraModuleException):
    """Exception raised when the camera stream does not meet resolution thresholds."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resolution is below the required threshold",
        )


class DeviceRemovedException(CameraModuleException):
    """Exception raised when a hardware device is removed or unplugged."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_410_GONE,
            detail="Camera device was removed or disconnected",
        )


class UnsupportedCameraException(CameraModuleException):
    """Exception raised when a camera connection source is not supported."""

    def __init__(self, detail: str = "Unsupported camera source type") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class CameraTimeoutException(CameraModuleException):
    """Exception raised when waiting for image frame acquisition times out."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Timeout waiting for frame acquisition",
        )
