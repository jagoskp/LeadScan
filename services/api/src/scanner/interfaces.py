import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any


class IScanPipeline(ABC):
    """Interface orchestrating the multi-stage Universal Smart Scanner pipeline."""

    @abstractmethod
    async def validate_image(self, file_path: str) -> bool:
        """Validate input image dimensions, format, and metadata."""
        pass

    @abstractmethod
    async def run_ocr_bypass(self, file_path: str) -> str:
        """Bypass OCR engine execution, returning structure placeholder text."""
        pass

    @abstractmethod
    async def run_ai_understanding_bypass(self, raw_text: str) -> dict[str, Any]:
        """Bypass AI engine, mapping raw OCR outputs to suggestions."""
        pass

    @abstractmethod
    async def detect_fields(
        self, raw_text: str, ai_data: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Identify potential structural fields in the scanned inputs."""
        pass

    @abstractmethod
    async def map_fields(
        self, detected_fields: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Map generic detected fields onto standard business attributes."""
        pass

    @abstractmethod
    async def extract_extra_information(
        self, raw_text: str, mapped_fields: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Ensure all unmapped text sections are captured as ExtraInformation."""
        pass

    @abstractmethod
    async def generate_ai_suggestions(
        self, raw_text: str, mapped_fields: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Generate high-level metadata predictions like company or duplicates."""
        pass

    @abstractmethod
    async def compute_confidence_score(self, fields: list[dict[str, Any]]) -> float:
        """Aggregate confidence scores across all detected attributes."""
        pass

    @abstractmethod
    async def check_duplicates_bypass(
        self,
        mapped_fields: list[dict[str, Any]],
        organization_id: uuid.UUID | None,
    ) -> list[dict[str, Any]]:
        """Mock duplicate checks against existing records."""
        pass

    @abstractmethod
    async def save_original_image_metadata(
        self, file_path: str, job_id: uuid.UUID
    ) -> Any:
        """Preserve original uncompressed image metadata."""
        pass

    @abstractmethod
    async def execute_pipeline(self, job_id: uuid.UUID) -> Any:
        """Coordinate execution across all pipeline stages."""
        pass


class IManualReviewEngine(ABC):
    """Interface defining actions for human-in-the-loop review overrides."""

    @abstractmethod
    async def edit_field(self, field_id: uuid.UUID, new_value: str) -> Any:
        """Edit the value of an existing detected field."""
        pass

    @abstractmethod
    async def delete_field(self, field_id: uuid.UUID) -> bool:
        """Delete an incorrectly detected field."""
        pass

    @abstractmethod
    async def merge_fields(
        self, field_ids: Sequence[uuid.UUID], target_field_name: str
    ) -> Any:
        """Merge values from multiple fields into a single field."""
        pass

    @abstractmethod
    async def split_field(
        self,
        field_id: uuid.UUID,
        delimiter: str,
        new_field_keys: Sequence[str],
    ) -> list[Any]:
        """Split a compound field value into multiple separate fields."""
        pass

    @abstractmethod
    async def rename_field(self, field_id: uuid.UUID, new_name: str) -> Any:
        """Rename the attribute type classification of a field."""
        pass

    @abstractmethod
    async def approve_result(self, result_id: uuid.UUID) -> Any:
        """Mark a ScanResult review status as APPROVED."""
        pass

    @abstractmethod
    async def reject_result(self, result_id: uuid.UUID) -> Any:
        """Mark a ScanResult review status as REJECTED."""
        pass


class IDuplicateDetectionEngine(ABC):
    """Interface specifying the duplicate validation rules."""

    @abstractmethod
    async def compare_by_phone(
        self, phone: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Compare phone fields to locate matching job IDs."""
        pass

    @abstractmethod
    async def compare_by_email(
        self, email: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Compare email addresses to locate matching job IDs."""
        pass

    @abstractmethod
    async def compare_by_website(
        self, website: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Compare websites to find matching job IDs."""
        pass

    @abstractmethod
    async def compare_by_gst(
        self, gst: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Compare GST numbers to locate matching job IDs."""
        pass

    @abstractmethod
    async def compare_by_company(
        self, company: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Compare company names to find matching job IDs."""
        pass

    @abstractmethod
    async def compare_by_person_name(
        self, name: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Compare person names to locate matching job IDs."""
        pass
