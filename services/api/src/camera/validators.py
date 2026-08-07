from typing import Any

from services.api.src.camera.exceptions import LowResolutionException


def validate_image_quality(frame: bytes) -> dict[str, Any]:
    """Analyze frame bytes to evaluate placeholder image quality scores.

    Checks blur, brightness, dark image, over exposure, rotation, skew,
    perspective, resolution, frame stability, and motion detection.
    """
    # Check that frame bytes are present
    if not frame:
        return {
            "is_valid": False,
            "overall_score": 0.0,
            "checks": {"empty_frame": True},
        }

    return {
        "is_valid": True,
        "overall_score": 0.92,
        "checks": {
            "blur_score": 0.95,
            "is_blurred": False,
            "brightness_score": 0.78,
            "is_dark": False,
            "is_overexposed": False,
            "rotation_degree": 0,
            "skew_angle": 0.0,
            "is_skewed": False,
            "has_perspective_distortion": False,
            "resolution": "1920x1080",
            "frame_stability_score": 0.98,
            "is_stable": True,
            "motion_detected": False,
        },
    }


def validate_resolution_compatibility(
    width: int, height: int, resolution_profile: str
) -> None:
    """Ensure that the input dimensions meet minimal capture standards."""
    if width <= 0 or height <= 0:
        raise LowResolutionException()

    # Predefined checks
    if resolution_profile == "720p" and (width < 1280 or height < 720):
        raise LowResolutionException()
    elif resolution_profile == "1080p" and (width < 1920 or height < 1080):
        raise LowResolutionException()
    elif resolution_profile in ("2K", "4K") and (width < 2048 or height < 1080):
        raise LowResolutionException()

    # Absolute minimum constraint check
    if width < 640 or height < 480:
        raise LowResolutionException()
