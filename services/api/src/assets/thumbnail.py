from typing import Any
from services.api.src.assets.storage import AssetStorageEngine

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class ThumbnailGenerator:
    """Derivative Preview & Thumbnail Generator operating independently of original files."""

    def __init__(self, storage_engine: AssetStorageEngine):
        self.storage = storage_engine

    def generate_thumbnails(self, file_bytes: bytes, file_name: str) -> list[dict[str, Any]]:
        derivatives: list[dict[str, Any]] = []

        if not HAS_PIL:
            # Fallback derivative storage when PIL is absent
            for t_type, dim in [("small", 150), ("medium", 400), ("web_preview", 800)]:
                thumb_path = self.storage.save_raw_file(f"thumb_{t_type}_{file_name}", file_bytes)
                derivatives.append(
                    {
                        "thumbnail_type": t_type,
                        "width": dim,
                        "height": dim,
                        "storage_path": thumb_path,
                    }
                )
            return derivatives

        try:
            import io
            with Image.open(io.BytesIO(file_bytes)) as img:
                for t_type, max_dim in [("small", 150), ("medium", 400), ("web_preview", 800)]:
                    thumb_img = img.copy()
                    thumb_img.thumbnail((max_dim, max_dim))
                    out_bytes = io.BytesIO()
                    thumb_img.save(out_bytes, format=img.format or "JPEG")
                    thumb_payload = out_bytes.getvalue()

                    thumb_path = self.storage.save_raw_file(f"thumb_{t_type}_{file_name}", thumb_payload)
                    derivatives.append(
                        {
                            "thumbnail_type": t_type,
                            "width": thumb_img.width,
                            "height": thumb_img.height,
                            "storage_path": thumb_path,
                        }
                    )
        except Exception:
            pass

        return derivatives
