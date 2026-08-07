import logging
from datetime import UTC, datetime
from typing import Any, Sequence
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.leads.enums import LeadStatusEnum, TimelineEventTypeEnum
from services.api.src.leads.exceptions import (
    LeadAlreadyArchivedException,
    LeadMergeException,
    LeadNotFoundException,
)
from services.api.src.leads.interfaces import ILeadService
from services.api.src.leads.models import (
    Company,
    Contact,
    Lead,
    LeadHistory,
    LeadMetadata,
    LeadNote,
    LeadTag,
    LeadTimeline,
)
from services.api.src.leads.repository import LeadRepository
from services.api.src.leads.schemas import (
    CompanySchema,
    ContactSchema,
    LeadCreateSchema,
    LeadMergeRequestSchema,
    LeadMetadataSchema,
    LeadNoteSchema,
    LeadSchema,
    LeadTagSchema,
    LeadTimelineSchema,
    LeadUpdateSchema,
)

logger = logging.getLogger(__name__)


class LeadService(ILeadService):
    """Facade service for Enterprise Lead Repository operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = LeadRepository(db)

    async def _log_timeline(
        self,
        lead_id: uuid.UUID,
        event_type: str,
        title: str,
        description: str | None = None,
        actor_id: uuid.UUID | None = None,
        metadata_snapshot: dict[str, Any] | None = None,
    ) -> LeadTimeline:
        now = datetime.now(UTC)
        timeline = LeadTimeline(
            id=uuid.uuid4(),
            lead_id=lead_id,
            event_type=event_type,
            title=title,
            description=description,
            actor_id=actor_id,
            metadata_snapshot=metadata_snapshot,
            created_at=now,
        )
        self.db.add(timeline)
        return timeline

    async def create_lead(
        self, request: LeadCreateSchema, actor_id: uuid.UUID | None = None
    ) -> LeadSchema:
        """Create a new master lead record with company, contacts, tags, notes, and metadata."""
        now = datetime.now(UTC)

        # 1. Company Handling
        company_obj: Company | None = None
        if request.company:
            existing_co = await self.repo.get_company_by_name(request.company.company_name)
            if existing_co:
                company_obj = existing_co
            else:
                company_obj = Company(
                    id=uuid.uuid4(),
                    company_name=request.company.company_name,
                    logo_url=request.company.logo_url,
                    industry=request.company.industry,
                    gst_number=request.company.gst_number,
                    website=request.company.website,
                    address=request.company.address,
                    departments=request.company.departments,
                    employees_count=request.company.employees_count,
                    notes=request.company.notes,
                    created_at=now,
                    updated_at=now,
                )
                self.db.add(company_obj)
                await self.db.flush()

        # 2. Create Lead Aggregate Root
        lead = Lead(
            id=uuid.uuid4(),
            company_id=company_obj.id if company_obj else None,
            owner_id=actor_id,
            title=request.title,
            status=request.status,
            priority=request.priority,
            source=request.source,
            lead_score=request.lead_score,
            is_favorite=False,
            is_archived=False,
            created_at=now,
            updated_at=now,
        )
        self.db.add(lead)
        await self.db.flush()

        # 3. Create Contacts
        for contact_req in request.contacts:
            contact = Contact(
                id=uuid.uuid4(),
                lead_id=lead.id,
                first_name=contact_req.first_name,
                last_name=contact_req.last_name,
                designation=contact_req.designation,
                is_primary=contact_req.is_primary,
                phones=contact_req.phones,
                emails=contact_req.emails,
                websites=contact_req.websites,
                addresses=contact_req.addresses,
                social_profiles=contact_req.social_profiles,
                custom_fields=contact_req.custom_fields,
                created_at=now,
                updated_at=now,
            )
            self.db.add(contact)

        # 4. Create Tags
        for tag_name in request.tags:
            tag = LeadTag(
                id=uuid.uuid4(),
                lead_id=lead.id,
                tag_name=tag_name,
                color="#10B981",
                is_system=False,
            )
            self.db.add(tag)

        # 5. Create Notes
        for note_text in request.notes:
            note = LeadNote(
                id=uuid.uuid4(),
                lead_id=lead.id,
                content=note_text,
                is_pinned=False,
                is_internal=True,
                author_id=actor_id,
                created_at=now,
            )
            self.db.add(note)

        # 6. Create Metadata Snapshot
        lead_meta = LeadMetadata(
            id=uuid.uuid4(),
            lead_id=lead.id,
            original_image_url=request.original_image_url,
            ocr_raw_output=request.ocr_raw_output,
            ai_understanding_output=request.ai_understanding_output,
            dom_entity_snapshot=request.dom_entity_snapshot,
            review_session_id=request.review_session_id,
            google_sync_job_id=request.google_sync_job_id,
            created_at=now,
        )
        self.db.add(lead_meta)

        # 7. Log Timeline Event
        await self._log_timeline(
            lead_id=lead.id,
            event_type=TimelineEventTypeEnum.CREATED.value,
            title="Lead Created",
            description=f"Lead record '{lead.title}' ingested into Master Lead Repository",
            actor_id=actor_id,
        )

        await self.db.commit()
        full_lead = await self.repo.get_by_id(lead.id)
        return self._to_schema(full_lead)

    async def get_lead(self, lead_id: uuid.UUID) -> LeadSchema:
        lead = await self.repo.get_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException(str(lead_id))
        return self._to_schema(lead)

    async def list_leads(
        self,
        search_query: str | None = None,
        status: str | None = None,
        is_archived: bool = False,
        limit: int = 50,
    ) -> list[LeadSchema]:
        leads = await self.repo.list_leads(search_query, status, is_archived, limit)
        return [self._to_schema(l) for l in leads]

    async def update_lead(
        self, lead_id: uuid.UUID, request: LeadUpdateSchema, actor_id: uuid.UUID | None = None
    ) -> LeadSchema:
        lead = await self.repo.get_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException(str(lead_id))
        if lead.is_archived:
            raise LeadAlreadyArchivedException(str(lead_id))

        changes = []
        if request.title is not None:
            lead.title = request.title
            changes.append("title")
        if request.status is not None:
            lead.status = request.status
            changes.append("status")
        if request.priority is not None:
            lead.priority = request.priority
            changes.append("priority")
        if request.lead_score is not None:
            lead.lead_score = request.lead_score
            changes.append("lead_score")
        if request.is_favorite is not None:
            lead.is_favorite = request.is_favorite
            changes.append("is_favorite")

        lead.updated_at = datetime.now(UTC)

        if changes:
            await self._log_timeline(
                lead_id=lead.id,
                event_type=TimelineEventTypeEnum.UPDATED.value,
                title="Lead Details Updated",
                description=f"Fields updated: {', '.join(changes)}",
                actor_id=actor_id,
            )

        await self.db.commit()
        full_lead = await self.repo.get_by_id(lead.id)
        return self._to_schema(full_lead)

    async def archive_lead(
        self, lead_id: uuid.UUID, actor_id: uuid.UUID | None = None
    ) -> LeadSchema:
        lead = await self.repo.get_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException(str(lead_id))

        lead.is_archived = True
        lead.status = LeadStatusEnum.ARCHIVED.value
        lead.updated_at = datetime.now(UTC)

        await self._log_timeline(
            lead_id=lead.id,
            event_type=TimelineEventTypeEnum.ARCHIVED.value,
            title="Lead Archived",
            description="Lead record moved to soft archive",
            actor_id=actor_id,
        )

        await self.db.commit()
        full_lead = await self.repo.get_by_id(lead.id)
        return self._to_schema(full_lead)

    async def restore_lead(
        self, lead_id: uuid.UUID, actor_id: uuid.UUID | None = None
    ) -> LeadSchema:
        lead = await self.repo.get_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException(str(lead_id))

        lead.is_archived = False
        lead.status = LeadStatusEnum.NEW.value
        lead.updated_at = datetime.now(UTC)

        await self._log_timeline(
            lead_id=lead.id,
            event_type=TimelineEventTypeEnum.RESTORED.value,
            title="Lead Restored",
            description="Lead record restored from archive",
            actor_id=actor_id,
        )

        await self.db.commit()
        full_lead = await self.repo.get_by_id(lead.id)
        return self._to_schema(full_lead)

    async def merge_leads(
        self, request: LeadMergeRequestSchema, actor_id: uuid.UUID | None = None
    ) -> LeadSchema:
        primary = await self.repo.get_by_id(request.primary_lead_id)
        if not primary:
            raise LeadNotFoundException(str(request.primary_lead_id))

        for sec_id in request.secondary_lead_ids:
            sec_lead = await self.repo.get_by_id(sec_id)
            if not sec_lead:
                continue

            # Re-assign contacts to primary lead
            for contact in sec_lead.contacts:
                contact.lead_id = primary.id

            # Re-assign notes to primary lead
            for note in sec_lead.notes:
                note.lead_id = primary.id

            # Re-assign tags
            for tag in sec_lead.tags:
                tag.lead_id = primary.id

            # Soft delete secondary lead
            sec_lead.is_archived = True
            sec_lead.status = "Merged"

            await self._log_timeline(
                lead_id=sec_lead.id,
                event_type=TimelineEventTypeEnum.MERGED.value,
                title="Lead Merged into Primary",
                description=f"Merged into lead '{primary.title}' ({primary.id})",
                actor_id=actor_id,
            )

        primary.updated_at = datetime.now(UTC)
        await self._log_timeline(
            lead_id=primary.id,
            event_type=TimelineEventTypeEnum.MERGED.value,
            title="Leads Merged",
            description=f"Merged {len(request.secondary_lead_ids)} secondary lead(s) into this record",
            actor_id=actor_id,
        )

        await self.db.commit()
        full_lead = await self.repo.get_by_id(primary.id)
        return self._to_schema(full_lead)

    async def get_timeline(self, lead_id: uuid.UUID) -> list[LeadTimelineSchema]:
        records = await self.repo.get_timeline(lead_id)
        return [LeadTimelineSchema.model_validate(r) for r in records]

    def _to_schema(self, lead: Lead) -> LeadSchema:
        company_schema = CompanySchema.model_validate(lead.company) if lead.company else None
        contacts_schema = [ContactSchema.model_validate(c) for c in lead.contacts]
        tags_schema = [LeadTagSchema.model_validate(t) for t in lead.tags]
        notes_schema = [LeadNoteSchema.model_validate(n) for n in lead.notes]
        meta_schema = LeadMetadataSchema.model_validate(lead.lead_metadata) if lead.lead_metadata else None

        return LeadSchema(
            id=lead.id,
            organization_id=lead.organization_id,
            company_id=lead.company_id,
            owner_id=lead.owner_id,
            title=lead.title,
            status=lead.status,
            priority=lead.priority,
            source=lead.source,
            lead_score=lead.lead_score,
            is_favorite=lead.is_favorite,
            is_archived=lead.is_archived,
            created_at=lead.created_at,
            updated_at=lead.updated_at,
            company=company_schema,
            contacts=contacts_schema,
            tags=tags_schema,
            notes=notes_schema,
            lead_metadata=meta_schema,
        )
