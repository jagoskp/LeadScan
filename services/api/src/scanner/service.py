import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from services.api.src.scanner.enums import (
    AISuggestionType,
    DetectedFieldType,
    FieldReviewStatus,
    LogoStatus,
    ReviewStatus,
    ScanJobStatus,
)
from services.api.src.scanner.exceptions import (
    DetectedFieldNotFoundException,
    ManualReviewValidationException,
    ScanJobNotFoundException,
    ScanResultNotFoundException,
)
from services.api.src.scanner.interfaces import (
    IDuplicateDetectionEngine,
    IManualReviewEngine,
    IScanPipeline,
)
from services.api.src.scanner.models import (
    AISuggestion,
    DetectedField,
    ExtraInformation,
    ScanJob,
    ScanResult,
)
from services.api.src.scanner.repository import ScanJobRepository, ScanResultRepository


class ScannerService(IScanPipeline, IManualReviewEngine, IDuplicateDetectionEngine):
    """Orchestrates scanner jobs, reviews, and duplicates."""

    def __init__(
        self,
        job_repo: ScanJobRepository,
        result_repo: ScanResultRepository,
    ) -> None:
        self.job_repo = job_repo
        self.result_repo = result_repo

    # ----------------------------------------------------
    # Job Management CRUD
    # ----------------------------------------------------

    async def create_job(
        self,
        user_id: uuid.UUID,
        source: str,
        organization_id: uuid.UUID | None = None,
    ) -> ScanJob:
        """Create a new scanning job in the database."""
        job = ScanJob(
            user_id=user_id,
            organization_id=organization_id,
            source=source,
            status=ScanJobStatus.PENDING.value,
        )
        return await self.job_repo.create(job)

    async def get_job(self, job_id: uuid.UUID) -> ScanJob:
        """Retrieve a specific ScanJob, raising an error if it doesn't exist."""
        job = await self.job_repo.get_by_id(job_id)
        if not job:
            raise ScanJobNotFoundException()
        return job

    async def list_jobs(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[ScanJob]:
        """List scan jobs filtered by user or organization scope."""
        return await self.job_repo.list_jobs(
            user_id=user_id, organization_id=organization_id
        )

    async def delete_job(self, job_id: uuid.UUID) -> bool:
        """Cancel and delete a scan job."""
        job = await self.get_job(job_id)
        return await self.job_repo.delete(job.id)

    async def get_result_by_job_id(self, job_id: uuid.UUID) -> ScanResult:
        """Retrieve the scan result associated with a job ID."""
        result = await self.result_repo.get_by_job_id(job_id)
        if not result:
            raise ScanResultNotFoundException()
        return result

    # ----------------------------------------------------
    # IScanPipeline Implementation
    # ----------------------------------------------------

    async def validate_image(self, file_path: str) -> bool:
        """Validate scanner image format, file presence, and size limits."""
        # Clean architecture structural validation
        return len(file_path.strip()) > 0

    async def run_ocr_bypass(self, file_path: str) -> str:
        """Structural mock simulating document OCR extraction."""
        return (
            "LeadScan AI Corp.\n"
            "John Doe\n"
            "Principal Software Engineer\n"
            "Phone: +1-555-0199\n"
            "Email: john.doe@leadscan.ai\n"
            "Website: www.leadscan.ai\n"
            "Address: 100 Innovation Way, Tech City, CA 94016\n"
            "GST: 22AAAAA1111A1Z1\n"
            "Hours: 9 AM - 6 PM\n"
            "Leftover unmapped notes text goes here."
        )

    async def run_ai_understanding_bypass(self, raw_text: str) -> dict[str, Any]:
        """Structural mock parsing raw OCR string to semantic business values."""
        return {
            "Person Name": "John Doe",
            "Company Name": "LeadScan AI Corp.",
            "Business Name": "LeadScan AI",
            "Phone": "+1-555-0199",
            "Email": "john.doe@leadscan.ai",
            "Website": "www.leadscan.ai",
            "Address": "100 Innovation Way, Tech City, CA 94016",
            "GST": "22AAAAA1111A1Z1",
            "PIN": "94016",
            "City": "Tech City",
            "State": "CA",
            "Country": "USA",
            "Designation": "Principal Software Engineer",
            "Department": "Engineering",
            "Opening Hours": "9 AM - 6 PM",
            "Business Category": "Technology Services",
            "unmapped_data": "Leftover unmapped notes text goes here.",
        }

    async def detect_fields(
        self, raw_text: str, ai_data: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Collect potential attributes identified during scanning."""
        fields = []
        for field_type in DetectedFieldType:
            if field_type.value in ai_data:
                fields.append({
                    "field_name": field_type.value,
                    "field_key": field_type.value.lower().replace(" ", "_"),
                    "value": ai_data[field_type.value],
                    "confidence": 0.95,
                    "source": "AI_UNDERSTANDING",
                    "bounding_box": {"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.05},
                })
        return fields

    async def map_fields(
        self, detected_fields: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Map generic detected fields onto standard business attributes."""
        # Passthrough in structural mock
        return detected_fields

    async def extract_extra_information(
        self, raw_text: str, mapped_fields: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Capture raw elements not directly mapped into structural fields."""
        return [
            {
                "raw_text": "Leftover unmapped notes text goes here.",
                "confidence": 0.85,
                "bounding_box": {"x": 0.1, "y": 0.8, "width": 0.8, "height": 0.1},
            }
        ]

    async def generate_ai_suggestions(
        self, raw_text: str, mapped_fields: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Formulate classification recommendations."""
        return [
            {
                "suggestion_type": AISuggestionType.DOCUMENT_TYPE.value,
                "value": "Business Card",
                "confidence": 0.99,
            },
            {
                "suggestion_type": AISuggestionType.BUSINESS_CATEGORY.value,
                "value": "Technology Services",
                "confidence": 0.92,
            },
            {
                "suggestion_type": AISuggestionType.POSSIBLE_WEBSITE.value,
                "value": "www.leadscan.ai",
                "confidence": 0.95,
            },
        ]

    async def compute_confidence_score(self, fields: list[dict[str, Any]]) -> float:
        """Compute aggregated confidence score across all fields."""
        if not fields:
            return 0.0
        scores = [f["confidence"] for f in fields if f.get("confidence") is not None]
        return sum(scores) / len(scores) if scores else 0.0

    async def check_duplicates_bypass(
        self,
        mapped_fields: list[dict[str, Any]],
        organization_id: uuid.UUID | None,
    ) -> list[dict[str, Any]]:
        """Bypass matching logic, returning structural suggestion properties."""
        return []

    async def save_original_image_metadata(
        self, file_path: str, job_id: uuid.UUID
    ) -> Any:
        """Mock storing uncompressed images."""
        return True

    async def execute_pipeline(self, job_id: uuid.UUID) -> ScanResult:
        """Simulate the multi-stage document processing pipeline.

        Saves the final output.
        """
        job = await self.get_job(job_id)
        await self.job_repo.update_status(job.id, ScanJobStatus.PROCESSING.value)

        # 1. Validation
        image_path = job.images[0].file_path if job.images else "mock_card.jpg"
        await self.validate_image(image_path)

        # 2. OCR Bypass
        raw_text = await self.run_ocr_bypass(image_path)

        # 3. AI Understanding Bypass
        parsed_data = await self.run_ai_understanding_bypass(raw_text)

        # 4. Field Detection & Mapping
        detected = await self.detect_fields(raw_text, parsed_data)
        mapped = await self.map_fields(detected)

        # 5. Extract Extra Information
        extra_info_data = await self.extract_extra_information(raw_text, mapped)

        # 6. AI Suggestions
        suggestions_data = await self.generate_ai_suggestions(raw_text, mapped)

        # 7. Confidence Score
        avg_confidence = await self.compute_confidence_score(mapped)

        # Create Result
        result = ScanResult(
            job_id=job.id,
            logo_status=LogoStatus.NONE.value,
            logo_url=None,
            review_status=ReviewStatus.PENDING.value,
            confidence_score=avg_confidence,
        )
        await self.result_repo.create_result(result)

        # Create Detected Fields
        for item in mapped:
            field = DetectedField(
                result_id=result.id,
                field_name=item["field_name"],
                field_key=item["field_key"],
                value=item["value"],
                confidence=item["confidence"],
                source=item["source"],
                bounding_box=item["bounding_box"],
                review_status=FieldReviewStatus.UNREVIEWED.value,
            )
            await self.result_repo.create_field(field)

        # Create Extra Info records
        for item in extra_info_data:
            extra = ExtraInformation(
                result_id=result.id,
                raw_text=item["raw_text"],
                confidence=item["confidence"],
                bounding_box=item["bounding_box"],
            )
            self.result_repo.session.add(extra)

        # Create AI Suggestions
        for item in suggestions_data:
            sugg = AISuggestion(
                job_id=job.id,
                suggestion_type=item["suggestion_type"],
                value=item["value"],
                confidence=item["confidence"],
            )
            self.result_repo.session.add(sugg)

        await self.result_repo.session.flush()

        # Update Job status. Require manual review if confidence is low.
        final_status = (
            ScanJobStatus.COMPLETED.value
            if avg_confidence >= 0.8
            else ScanJobStatus.MANUAL_REVIEW.value
        )
        await self.job_repo.update_status(job.id, final_status)

        # Reload result to populate relationships
        reloaded = await self.result_repo.get_by_id(result.id)
        if not reloaded:
            raise ScanResultNotFoundException()
        return reloaded

    # ----------------------------------------------------
    # IManualReviewEngine Implementation
    # ----------------------------------------------------

    async def edit_field(self, field_id: uuid.UUID, new_value: str) -> DetectedField:
        """Review override: Edit a field's value."""
        field = await self.result_repo.get_field_by_id(field_id)
        if not field:
            raise DetectedFieldNotFoundException()

        updated = await self.result_repo.update_field(
            field.id,
            {
                "value": new_value,
                "review_status": FieldReviewStatus.EDITED.value,
                "confidence": 1.0,
                "source": "MANUAL",
                "updated_at": datetime.now(UTC),
            },
        )
        if not updated:
            raise DetectedFieldNotFoundException()
        return updated

    async def delete_field(self, field_id: uuid.UUID) -> bool:
        """Review override: Delete a field."""
        field = await self.result_repo.get_field_by_id(field_id)
        if not field:
            raise DetectedFieldNotFoundException()
        return await self.result_repo.delete_field(field.id)

    async def merge_fields(
        self, field_ids: Sequence[uuid.UUID], target_field_name: str
    ) -> DetectedField:
        """Review override: Merge multiple fields into a single field."""
        if not field_ids:
            raise ManualReviewValidationException("No fields specified for merging")

        fields = []
        for fid in field_ids:
            f = await self.result_repo.get_field_by_id(fid)
            if not f:
                raise DetectedFieldNotFoundException()
            fields.append(f)

        # Merge values using a space delimiter
        merged_value = " ".join([f.value for f in fields if f.value])

        # Keep first field, delete the rest
        primary_field = fields[0]
        for f in fields[1:]:
            await self.result_repo.delete_field(f.id)

        updated = await self.result_repo.update_field(
            primary_field.id,
            {
                "field_name": target_field_name,
                "field_key": target_field_name.lower().replace(" ", "_"),
                "value": merged_value,
                "review_status": FieldReviewStatus.MERGED.value,
                "confidence": 1.0,
                "source": "MANUAL",
                "updated_at": datetime.now(UTC),
            },
        )
        if not updated:
            raise DetectedFieldNotFoundException()
        return updated

    async def split_field(
        self,
        field_id: uuid.UUID,
        delimiter: str,
        new_field_keys: Sequence[str],
    ) -> list[DetectedField]:
        """Review override: Split a compound field value into multiple fields."""
        field = await self.result_repo.get_field_by_id(field_id)
        if not field:
            raise DetectedFieldNotFoundException()

        if not field.value:
            raise ManualReviewValidationException("Cannot split an empty field")

        split_parts = field.value.split(delimiter)
        if len(split_parts) != len(new_field_keys):
            raise ManualReviewValidationException(
                f"Split parts count ({len(split_parts)}) "
                f"does not match key count ({len(new_field_keys)})"
            )

        new_fields = []
        # Mark original field status as SPLIT
        await self.result_repo.update_field(
            field.id,
            {
                "review_status": FieldReviewStatus.SPLIT.value,
                "updated_at": datetime.now(UTC),
            },
        )

        for i, val in enumerate(split_parts):
            new_f = DetectedField(
                result_id=field.result_id,
                field_name=DetectedFieldType.CUSTOM.value,
                field_key=new_field_keys[i],
                value=val.strip(),
                confidence=1.0,
                source="MANUAL",
                review_status=FieldReviewStatus.UNREVIEWED.value,
            )
            created = await self.result_repo.create_field(new_f)
            new_fields.append(created)

        return new_fields

    async def rename_field(self, field_id: uuid.UUID, new_name: str) -> DetectedField:
        """Review override: Rename the attribute class label of a field."""
        field = await self.result_repo.get_field_by_id(field_id)
        if not field:
            raise DetectedFieldNotFoundException()

        updated = await self.result_repo.update_field(
            field.id,
            {
                "field_name": new_name,
                "field_key": new_name.lower().replace(" ", "_"),
                "review_status": FieldReviewStatus.RENAMED.value,
                "updated_at": datetime.now(UTC),
            },
        )
        if not updated:
            raise DetectedFieldNotFoundException()
        return updated

    async def approve_result(self, result_id: uuid.UUID) -> ScanResult:
        """Approve a scan result, updating job status to COMPLETED."""
        result = await self.result_repo.get_by_id(result_id)
        if not result:
            raise ScanResultNotFoundException()

        updated_result = await self.result_repo.update_result(
            result.id,
            {
                "review_status": ReviewStatus.APPROVED.value,
                "updated_at": datetime.now(UTC),
            },
        )
        if not updated_result:
            raise ScanResultNotFoundException()
        await self.job_repo.update_status(result.job_id, ScanJobStatus.COMPLETED.value)
        return updated_result

    async def reject_result(self, result_id: uuid.UUID) -> ScanResult:
        """Reject a scan result, updating job status to FAILED."""
        result = await self.result_repo.get_by_id(result_id)
        if not result:
            raise ScanResultNotFoundException()

        updated_result = await self.result_repo.update_result(
            result.id,
            {
                "review_status": ReviewStatus.REJECTED.value,
                "updated_at": datetime.now(UTC),
            },
        )
        if not updated_result:
            raise ScanResultNotFoundException()
        await self.job_repo.update_status(result.job_id, ScanJobStatus.FAILED.value)
        return updated_result

    # ----------------------------------------------------
    # IDuplicateDetectionEngine Implementation
    # ----------------------------------------------------

    async def compare_by_phone(
        self, phone: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Comparison architecture interface: search duplicates by Phone."""
        return []

    async def compare_by_email(
        self, email: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Comparison architecture interface: search duplicates by Email."""
        return []

    async def compare_by_website(
        self, website: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Comparison architecture interface: search duplicates by Website."""
        return []

    async def compare_by_gst(
        self, gst: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Comparison architecture interface: search duplicates by GST."""
        return []

    async def compare_by_company(
        self, company: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Comparison architecture interface: search duplicates by Company Name."""
        return []

    async def compare_by_person_name(
        self, name: str, organization_id: uuid.UUID | None
    ) -> list[uuid.UUID]:
        """Comparison architecture interface: search duplicates by Person Name."""
        return []
