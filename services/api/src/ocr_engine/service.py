import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from services.api.src.ocr_engine.enums import OCRJobStatus
from services.api.src.ocr_engine.exceptions import (
    OCRJobNotFoundException,
    PreprocessingException,
)
from services.api.src.ocr_engine.interfaces import (
    IImagePreprocessor,
    ILayoutDetector,
    IOCRPipeline,
    IOCRProvider,
)
from services.api.src.ocr_engine.models import (
    OCRBlock,
    OCREngineJob,
    OCRLine,
    OCRMetadata,
    OCRPage,
    OCRWord,
)
from services.api.src.ocr_engine.repository import (
    OCRJobRepository,
    OCRPageRepository,
)
from services.api.src.ocr_engine.schemas import OCRJobCreate


class OCREngineService(
    IOCRPipeline, IOCRProvider, IImagePreprocessor, ILayoutDetector
):
    """Orchestrates document preprocessing, OCR stubs, and layout building."""

    def __init__(
        self,
        job_repo: OCRJobRepository,
        page_repo: OCRPageRepository,
    ) -> None:
        self.job_repo = job_repo
        self.page_repo = page_repo

    # ----------------------------------------------------
    # Job CRUD Operations
    # ----------------------------------------------------

    async def create_job(self, user_id: uuid.UUID, data: OCRJobCreate) -> OCREngineJob:
        """Register a new OCR execution request in the database."""
        job = OCREngineJob(
            user_id=user_id,
            organization_id=data.organization_id,
            input_type=data.input_type.value,
            provider=data.provider.value,
            status=OCRJobStatus.PENDING.value,
            languages=data.languages,
            file_path=data.file_path,
        )
        return await self.job_repo.create(job)

    async def get_job(self, job_id: uuid.UUID) -> OCREngineJob:
        """Retrieve a specific OCREngineJob, raising 404 if missing."""
        job = await self.job_repo.get_by_id(job_id)
        if not job:
            raise OCRJobNotFoundException()
        return job

    async def list_jobs(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[OCREngineJob]:
        """List OCR requests matching the user/organization scope."""
        return await self.job_repo.list_jobs(
            user_id=user_id, organization_id=organization_id
        )

    async def delete_job(self, job_id: uuid.UUID) -> bool:
        """Unregister and remove an OCR job log from the database."""
        # Ensure job exists
        await self.get_job(job_id)
        return await self.job_repo.delete(job_id)

    # ----------------------------------------------------
    # IOCRPipeline Implementation
    # ----------------------------------------------------

    async def execute_ocr(self, job_id: uuid.UUID) -> OCREngineJob:
        """Orchestrate the end-to-end OCR processing flow."""
        job = await self.get_job(job_id)
        start_time = datetime.now(UTC)

        # 1. Image Preprocessing
        await self.job_repo.update_status(
            job.id, OCRJobStatus.PREPROCESSING.value
        )
        image_bytes = b"SIMULATED_IMAGE_DATA_BYTES"
        preprocessed_bytes = await self.preprocess(
            image_bytes, ["Resize", "Contrast"]
        )

        # 2. OCR Provider Execution
        await self.job_repo.update_status(job.id, OCRJobStatus.EXTRACTING.value)
        raw_ocr_result = await self.extract_text(
            preprocessed_bytes, job.languages
        )

        # 3. Layout Detection
        layout_elements = await self.detect_layout(raw_ocr_result)

        # Save OCR Page Results
        page = OCRPage(
            job_id=job.id,
            page_number=1,
            raw_text=raw_ocr_result["raw_text"],
            width=1920,
            height=1080,
            detected_language=job.languages[0] if job.languages else "en",
            confidence_score=0.96,
        )
        await self.page_repo.create_page(page)

        # Save Layout Blocks, Lines, and Words
        for block_data in layout_elements:
            block = OCRBlock(
                page_id=page.id,
                block_index=block_data["block_index"],
                block_type=block_data["block_type"],
                bounding_box=block_data["bounding_box"],
                confidence=block_data["confidence"],
            )
            await self.page_repo.create_block(block)

            for line_data in block_data["lines"]:
                line = OCRLine(
                    block_id=block.id,
                    line_index=line_data["line_index"],
                    raw_text=line_data["raw_text"],
                    bounding_box=line_data["bounding_box"],
                    confidence=line_data["confidence"],
                )
                await self.page_repo.create_line(line)

                for word_data in line_data["words"]:
                    word = OCRWord(
                        line_id=line.id,
                        word_index=word_data["word_index"],
                        text=word_data["text"],
                        bounding_box=word_data["bounding_box"],
                        confidence=word_data["confidence"],
                        char_start=word_data["char_start"],
                        char_end=word_data["char_end"],
                    )
                    await self.page_repo.create_word(word)

        # Log Processing latency metadata
        duration_ms = int((datetime.now(UTC) - start_time).total_seconds() * 1000)
        meta = OCRMetadata(
            job_id=job.id,
            key="processing_latency_ms",
            value=str(duration_ms),
        )
        await self.page_repo.add_metadata(meta)

        # 4. Finalize OCR Status
        await self.job_repo.update_status(job.id, OCRJobStatus.COMPLETED.value)

        # Reload job to populate relationships
        reloaded = await self.job_repo.get_by_id(job.id)
        if not reloaded:
            raise OCRJobNotFoundException()
        return reloaded

    # ----------------------------------------------------
    # IOCRProvider Implementation
    # ----------------------------------------------------

    async def extract_text(
        self, image_data: bytes, languages: Sequence[str]
    ) -> dict[str, Any]:
        """Bypass OCR engine, returning mock word and character layouts."""
        return {
            "raw_text": "LeadScan AI John Doe +1-555-0199",
            "words": [
                {
                    "text": "LeadScan",
                    "bbox": {"x": 0.1, "y": 0.2, "width": 0.2, "height": 0.05},
                    "confidence": 0.99,
                    "char_start": 0,
                    "char_end": 8,
                },
                {
                    "text": "AI",
                    "bbox": {"x": 0.32, "y": 0.2, "width": 0.05, "height": 0.05},
                    "confidence": 0.98,
                    "char_start": 9,
                    "char_end": 11,
                },
                {
                    "text": "John",
                    "bbox": {"x": 0.1, "y": 0.3, "width": 0.1, "height": 0.05},
                    "confidence": 0.97,
                    "char_start": 12,
                    "char_end": 16,
                },
                {
                    "text": "Doe",
                    "bbox": {"x": 0.22, "y": 0.3, "width": 0.08, "height": 0.05},
                    "confidence": 0.96,
                    "char_start": 17,
                    "char_end": 20,
                },
                {
                    "text": "+1-555-0199",
                    "bbox": {"x": 0.1, "y": 0.4, "width": 0.25, "height": 0.05},
                    "confidence": 0.95,
                    "char_start": 21,
                    "char_end": 32,
                },
            ],
        }

    # ----------------------------------------------------
    # IImagePreprocessor Implementation
    # ----------------------------------------------------

    async def preprocess(
        self, image_data: bytes, operations: Sequence[str]
    ) -> bytes:
        """Apply pre-processing operations to the frame."""
        if not image_data:
            raise PreprocessingException("Empty image data provided")
        # In mock provider, return unmodified bytes
        return image_data

    # ----------------------------------------------------
    # ILayoutDetector Implementation
    # ----------------------------------------------------

    async def detect_layout(
        self, raw_ocr_data: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Parse raw coordinates into blocks, lines, and words."""
        words_data = raw_ocr_data.get("words", [])

        # Organise into a single block and two lines for the mock output
        return [
            {
                "block_index": 0,
                "block_type": "TEXT",
                "bounding_box": {"x": 0.1, "y": 0.2, "width": 0.4, "height": 0.3},
                "confidence": 0.97,
                "lines": [
                    {
                        "line_index": 0,
                        "raw_text": "LeadScan AI",
                        "bounding_box": {
                            "x": 0.1,
                            "y": 0.2,
                            "width": 0.27,
                            "height": 0.05,
                        },
                        "confidence": 0.98,
                        "words": [words_data[0], words_data[1]],
                    },
                    {
                        "line_index": 1,
                        "raw_text": "John Doe",
                        "bounding_box": {
                            "x": 0.1,
                            "y": 0.3,
                            "width": 0.2,
                            "height": 0.05,
                        },
                        "confidence": 0.96,
                        "words": [words_data[2], words_data[3]],
                    },
                    {
                        "line_index": 2,
                        "raw_text": "+1-555-0199",
                        "bounding_box": {
                            "x": 0.1,
                            "y": 0.4,
                            "width": 0.25,
                            "height": 0.05,
                        },
                        "confidence": 0.95,
                        "words": [words_data[4]],
                    },
                ],
            }
        ]
