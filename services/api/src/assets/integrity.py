from pathlib import Path
from services.api.src.assets.storage import AssetStorageEngine


class AssetIntegrityValidator:
    """Integrity Validator checking SHA256 file hashes to detect corruption or missing files."""

    def __init__(self, storage_engine: AssetStorageEngine):
        self.storage = storage_engine

    def validate_integrity(self, storage_path: str, expected_sha256: str) -> tuple[str, str | None]:
        p = Path(storage_path)
        if not p.exists():
            return "missing", None

        file_bytes = self.storage.read_raw_file(storage_path)
        actual_hash = self.storage.calculate_sha256(file_bytes)

        if actual_hash.lower() == expected_sha256.lower():
            return "healthy", actual_hash
        else:
            return "corrupted", actual_hash
