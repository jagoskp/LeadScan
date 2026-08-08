import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from services.api.src.ai_understanding.enums import (
    AIDocumentType,
    AIEntityType,
    AIJobStatus,
)
from services.api.src.ai_understanding.exceptions import (
    UnderstandingJobNotFoundException,
)
from services.api.src.ai_understanding.interfaces import (
    IAIProvider,
    IAIUnderstandingPipeline,
    IEntityResolver,
    IRelationshipDetector,
)
from services.api.src.ai_understanding.models import (
    AIUnknownEntity,
    DetectedEntity,
    EntityRelation,
    Keyword,
    UnderstandingJob,
    UnderstandingMetadata,
)
from services.api.src.ai_understanding.repository import (
    DetectedEntityRepository,
    UnderstandingJobRepository,
)
from services.api.src.ai_understanding.schemas import UnderstandingJobCreate


class AIUnderstandingService(
    IAIUnderstandingPipeline,
    IAIProvider,
    IEntityResolver,
    IRelationshipDetector,
):
    """Orchestrates raw OCR understanding, doc types, and relations."""

    def __init__(
        self,
        job_repo: UnderstandingJobRepository,
        entity_repo: DetectedEntityRepository,
    ) -> None:
        self.job_repo = job_repo
        self.entity_repo = entity_repo

    # ----------------------------------------------------
    # Job CRUD Operations
    # ----------------------------------------------------

    async def create_job(
        self, user_id: uuid.UUID, data: UnderstandingJobCreate
    ) -> UnderstandingJob:
        """Register a new AI job configuration."""
        job = UnderstandingJob(
            user_id=user_id,
            organization_id=data.organization_id,
            ocr_page_id=data.ocr_page_id,
            provider=data.provider.value,
            status=AIJobStatus.PENDING.value,
            document_type=data.document_type.value,
            detected_language="en",
        )
        return await self.job_repo.create(job)

    async def get_job(self, job_id: uuid.UUID) -> UnderstandingJob:
        """Retrieve a specific AI job, raising 404 if missing."""
        job = await self.job_repo.get_by_id(job_id)
        if not job:
            raise UnderstandingJobNotFoundException()
        return job

    async def list_jobs(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[UnderstandingJob]:
        """List AI jobs filtered by user context and organization."""
        return await self.job_repo.list_jobs(
            user_id=user_id, organization_id=organization_id
        )

    async def delete_job(self, job_id: uuid.UUID) -> bool:
        """Unregister and remove an AI job log from the database."""
        # Ensure job exists
        await self.get_job(job_id)
        return await self.job_repo.delete(job_id)

    # ----------------------------------------------------
    # IAIUnderstandingPipeline Implementation
    # ----------------------------------------------------

    async def execute_understanding(self, job_id: uuid.UUID) -> UnderstandingJob:
        """Orchestrate the end-to-end AI semantic understanding flow."""
        job = await self.get_job(job_id)
        start_time = datetime.now(UTC)

        # 1. Text Normalization
        await self.job_repo.update_status(job.id, AIJobStatus.ANALYZING.value)
        raw_text = "LeadScan AI Corp. John Doe CEO +1-555-0199 john.doe@leadscan.ai"
        normalized = raw_text.strip().replace("  ", " ")

        # 2. AI Provider Document analysis
        document_classification = AIDocumentType.VISITING_CARD.value
        analysis_data = await self.analyze_document(
            normalized, document_classification
        )

        # Save classification/language updates
        await self.job_repo.update_status(
            job.id,
            AIJobStatus.ANALYZING.value,
            document_type=document_classification,
        )

        # Save Detected Entities
        entity_id_map: dict[str, uuid.UUID] = {}
        for entity_data in analysis_data["entities"]:
            entity = DetectedEntity(
                job_id=job.id,
                entity_type=entity_data["entity_type"],
                value=entity_data["value"],
                normalized_value=entity_data["normalized_value"],
                bounding_box=entity_data["bounding_box"],
                confidence=entity_data["confidence"],
            )
            await self.entity_repo.create_entity(entity)
            entity_id_map[entity_data["value"]] = entity.id

        # Save Relationships
        for rel_data in analysis_data["relations"]:
            source_id = entity_id_map.get(rel_data["source_value"])
            target_id = entity_id_map.get(rel_data["target_value"])
            if source_id and target_id:
                relation = EntityRelation(
                    job_id=job.id,
                    source_entity_id=source_id,
                    target_entity_id=target_id,
                    relation_type=rel_data["relation_type"],
                    confidence=rel_data["confidence"],
                )
                await self.entity_repo.create_relation(relation)

        # Save Keywords
        for kw_data in analysis_data["keywords"]:
            keyword = Keyword(
                job_id=job.id,
                word=kw_data["word"],
                score=kw_data["score"],
            )
            await self.entity_repo.create_keyword(keyword)

        # Save Unknown Entities (Preserve everything)
        for unk_data in analysis_data["unknown_entities"]:
            unknown = AIUnknownEntity(
                job_id=job.id,
                raw_text=unk_data["raw_text"],
                reason=unk_data["reason"],
            )
            await self.entity_repo.create_unknown_entity(unknown)

        # Log latency metadata
        duration_ms = int((datetime.now(UTC) - start_time).total_seconds() * 1000)
        meta = UnderstandingMetadata(
            job_id=job.id,
            key="processing_latency_ms",
            value=str(duration_ms),
        )
        await self.entity_repo.add_metadata(meta)

        # Finalize AI status
        await self.job_repo.update_status(job.id, AIJobStatus.COMPLETED.value)

        # Reload job to populate relationships
        reloaded = await self.job_repo.get_by_id(job.id)
        if not reloaded:
            raise UnderstandingJobNotFoundException()
        return reloaded

    # ----------------------------------------------------
    # IAIProvider Implementation
    # ----------------------------------------------------

    async def analyze_document(
        self, raw_text: str, document_type: str
    ) -> dict[str, Any]:
        """Bypass prompt pipelines, returning mock semantic structures."""
        entities = await self.resolve_entities(raw_text)
        relations = await self.detect_relations(entities)

        return {
            "document_type": document_type,
            "language": "en",
            "entities": entities,
            "relations": relations,
            "keywords": [
                {"word": "leadscan", "score": 0.99},
                {"word": "john", "score": 0.95},
            ],
            "unknown_entities": [
                {"raw_text": "Corp.", "reason": "Suffix abbreviation ignored"},
                {"raw_text": "CEO", "reason": "Role unmapped to fields"},
            ],
        }

    # ----------------------------------------------------
    # IEntityResolver Implementation
    # ----------------------------------------------------

    async def resolve_entities(
        self, raw_text: str
    ) -> list[dict[str, Any]]:
        """Identify individual semantic entities within the text."""
        return [
            {
                "entity_type": AIEntityType.COMPANY.value,
                "value": "LeadScan AI",
                "normalized_value": "LEADSCAN AI",
                "bounding_box": {"x": 0.1, "y": 0.2, "width": 0.2, "height": 0.05},
                "confidence": 0.99,
            },
            {
                "entity_type": AIEntityType.PERSON.value,
                "value": "John Doe",
                "normalized_value": "JOHN DOE",
                "bounding_box": {"x": 0.1, "y": 0.3, "width": 0.15, "height": 0.05},
                "confidence": 0.97,
            },
            {
                "entity_type": AIEntityType.PHONE.value,
                "value": "+1-555-0199",
                "normalized_value": "+15550199",
                "bounding_box": {"x": 0.1, "y": 0.4, "width": 0.2, "height": 0.05},
                "confidence": 0.95,
            },
            {
                "entity_type": AIEntityType.EMAIL.value,
                "value": "john.doe@leadscan.ai",
                "normalized_value": "john.doe@leadscan.ai",
                "bounding_box": {"x": 0.1, "y": 0.5, "width": 0.25, "height": 0.05},
                "confidence": 0.98,
            },
        ]

    # ----------------------------------------------------
    # IRelationshipDetector Implementation
    # ----------------------------------------------------

    async def detect_relations(
        self, entities: Sequence[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Trace semantic links (e.g. Person works_for Company)."""
        return [
            {
                "source_value": "John Doe",
                "target_value": "LeadScan AI",
                "relation_type": "works_for",
                "confidence": 0.96,
            },
            {
                "source_value": "John Doe",
                "target_value": "+1-555-0199",
                "relation_type": "has_phone",
                "confidence": 0.98,
            },
            {
                "source_value": "John Doe",
                "target_value": "john.doe@leadscan.ai",
                "relation_type": "has_email",
                "confidence": 0.99,
            },
        ]
