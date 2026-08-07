from enum import StrEnum


class CameraSourceType(StrEnum):
    """Supported hardware or software source types of image frames."""

    LAPTOP_WEBCAM = "Laptop Internal Webcam"
    EXTERNAL_USB = "External USB Camera"
    MOBILE_CAMERA = "Mobile Camera"
    IP_CAMERA = "IP Camera"
    RTSP_CAMERA = "RTSP Camera"
    VIRTUAL_CAMERA = "Virtual Camera"


class CaptureMode(StrEnum):
    """The mode in which the camera capture session runs."""

    SINGLE_CAPTURE = "Single Capture"
    CONTINUOUS_SCAN = "Continuous Scan"
    AUTO_CAPTURE = "Auto Capture"
    MANUAL_CAPTURE = "Manual Capture"
    BURST_CAPTURE = "Burst Capture"


class ImageFormat(StrEnum):
    """Supported output image frame compression formats."""

    PNG = "PNG"
    JPEG = "JPEG"
    WEBP = "WEBP"
    BMP = "BMP"
    TIFF = "TIFF"


class CameraResolution(StrEnum):
    """Standard predefined resolution profiles."""

    R_720P = "720p"
    R_1080P = "1080p"
    R_2K = "2K"
    R_4K = "4K"
    CUSTOM = "Custom Resolution"


class FrameRate(StrEnum):
    """Standard acquisition frame rates in FPS."""

    FPS_15 = "15 FPS"
    FPS_24 = "24 FPS"
    FPS_30 = "30 FPS"
    FPS_60 = "60 FPS"


class PermissionPlatform(StrEnum):
    """Operating platforms requiring camera hardware access permission."""

    DESKTOP = "Desktop"
    ANDROID = "Android"
    IOS = "iOS"
    WEB_BROWSER = "Web Browser"


class DeviceStatus(StrEnum):
    """Active connection status state of a registered camera device."""

    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    BUSY = "BUSY"
    ERROR = "ERROR"
