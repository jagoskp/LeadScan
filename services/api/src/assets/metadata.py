from typing import Any

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class AssetMetadataExtractor:
    """Metadata Extractor inspecting image resolution, DPI, color space, and file size."""

    def extract_metadata(self, file_bytes: bytes) -> dict[str, Any]:
        size_bytes = len(file_bytes)
        width, height, dpi, color_space = None, None, "72 DPI", "RGB"

        if HAS_PIL:
            try:
                import io
                with Image.open(io.BytesIO(file_bytes)) as img:
                    width, height = img.size
                    color_space = img.mode
                    info_dpi = img.info.get("dpi")
                    if info_dpi:
                        dpi = f"{int(info_dpi[0])} DPI"
            except Exception:
                pass

        return {
            "file_size_bytes": size_bytes,
            "width": width,
            "height": height,
            "dpi": dpi,
            "color_space": color_space,
        }
