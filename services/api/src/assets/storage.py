import hashlib
from pathlib import Path
import uuid


class AssetStorageEngine:
    """Storage Engine managing lossless local storage, hashing, and file I/O."""

    def __init__(self, base_storage_dir: str = "storage/assets"):
        self.base_dir = Path(base_storage_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def calculate_sha256(self, file_bytes: bytes) -> str:
        return hashlib.sha256(file_bytes).hexdigest()

    def calculate_md5(self, file_bytes: bytes) -> str:
        return hashlib.md5(file_bytes).hexdigest()

    def save_raw_file(self, file_name: str, file_bytes: bytes) -> str:
        """Losslessly save raw binary payload to storage."""
        ext = Path(file_name).suffix or ".bin"
        unique_name = f"{uuid.uuid4()}{ext}"
        file_path = self.base_dir / unique_name
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        return str(file_path)

    def read_raw_file(self, storage_path: str) -> bytes:
        p = Path(storage_path)
        if not p.exists():
            raise FileNotFoundError(f"Storage file '{storage_path}' not found on disk.")
        with open(p, "rb") as f:
            return f.read()
