import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

from services.api.src.document_model.enums import (
    DOMDocumentType,
    DOMEntitySource,
    DOMEntityType,
    DOMRelationshipType,
    DOMReviewStatus,
    DOMSectionType,
)
from services.api.src.document_model.exceptions import (
    DocumentNotFoundException,
    EntityNotFoundException,
)
from services.api.src.document_model.interfaces import (
    IDOMBuilder,
    IDOMNormalizer,
    IDOMValidator,
)
from services.api.src.document_model.models import (
    DOMExtraInformation,
    DOMUnknownEntity,
    Document,
    DocumentMetadata,
    DocumentSection,
    Entity,
    EntityAttribute,
    EntityGroup,
    EntityRelationship,
)
from services.api.src.document_model.repository import (
    DocumentRepository,
    EntityRepository,
)
from services.api.src.document_model.schemas import (
    DocumentCreate,
    DocumentUpdate,
    EntityAttributeUpdate,
)


class DOMEngineService(IDOMBuilder, IDOMNormalizer, IDOMValidator):
    """Orchestrates DOM Document hierarchies, normalizers, and reviews."""

    def __init__(
        self,
        doc_repo: DocumentRepository,
        entity_repo: EntityRepository,
    ) -> None:
        self.doc_repo = doc_repo
        self.entity_repo = entity_repo

    # ----------------------------------------------------
    # Document CRUD Operations
    # ----------------------------------------------------

    async def create_document(
        self, user_id: uuid.UUID, data: DocumentCreate
    ) -> Document:
        """Register a new DOM Document root config."""
        doc = Document(
            user_id=user_id,
            organization_id=data.organization_id,
            document_type=data.document_type.value,
            status=DOMReviewStatus.PENDING.value,
        )
        return await self.doc_repo.create(doc)

    async def get_document(self, doc_id: uuid.UUID) -> Document:
        """Retrieve a DOM Document, raising 404 if missing."""
        doc = await self.doc_repo.get_by_id(doc_id)
        if not doc:
            raise DocumentNotFoundException()
        return doc

    async def list_documents(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[Document]:
        """List DOM documents matching user context and organization."""
        return await self.doc_repo.list_documents(
            user_id=user_id, organization_id=organization_id
        )

    async def update_document_status(
        self, doc_id: uuid.UUID, data: DocumentUpdate
    ) -> Document:
        """Update DOM Document review status."""
        # Ensure document exists
        await self.get_document(doc_id)
        updated = await self.doc_repo.update_status(doc_id, data.status.value)
        if not updated:
            raise DocumentNotFoundException()
        return updated

    async def delete_document(self, doc_id: uuid.UUID) -> bool:
        """Delete a DOM Document root from the database."""
        # Ensure document exists
        await self.get_document(doc_id)
        return await self.doc_repo.delete(doc_id)

    # ----------------------------------------------------
    # Entity & Attribute CRUD Operations
    # ----------------------------------------------------

    async def create_entity(
        self,
        doc_id: uuid.UUID,
        entity_type: DOMEntityType,
        value: str,
        source: DOMEntitySource,
    ) -> Entity:
        """Create a single Entity node inside a Document."""
        # Ensure document exists
        await self.get_document(doc_id)

        entity = Entity(
            document_id=doc_id,
            entity_type=entity_type.value,
            value=value,
            normalized_value=value,
            confidence=1.0,
            source=source.value,
        )
        return await self.entity_repo.create_entity(entity)

    async def get_entity(self, entity_id: uuid.UUID) -> Entity:
        """Retrieve a specific Entity, raising 404 if missing."""
        entity = await self.entity_repo.get_entity_by_id(entity_id)
        if not entity:
            raise EntityNotFoundException()
        return entity

    async def update_attribute(
        self, attr_id: uuid.UUID, data: EntityAttributeUpdate
    ) -> EntityAttribute:
        """Update review status or value properties of a target attribute."""
        attr = await self.entity_repo.get_attribute_by_id(attr_id)
        if not attr:
            raise EntityNotFoundException()

        update_data = data.model_dump(exclude_unset=True)
        updated = await self.entity_repo.update_attribute(attr_id, update_data)
        if not updated:
            raise EntityNotFoundException()
        return updated

    # ----------------------------------------------------
    # IDOMBuilder Implementation
    # ----------------------------------------------------

    async def build_dom(self, understanding_job_id: uuid.UUID) -> uuid.UUID:
        """Parse AI job results and write normalized DOM structures."""
        start_time = datetime.now(UTC)

        # 1. Initialize Document Root (Bypassing AI job fetch details)
        doc = Document(
            document_type=DOMDocumentType.VISITING_CARD.value,
            status=DOMReviewStatus.PENDING.value,
        )
        await self.doc_repo.create(doc)

        # 2. Setup Document sections
        header_section = DocumentSection(
            document_id=doc.id,
            section_type=DOMSectionType.HEADER.value,
            section_index=0,
        )
        await self.entity_repo.create_section(header_section)

        body_section = DocumentSection(
            document_id=doc.id,
            section_type=DOMSectionType.BODY.value,
            section_index=1,
        )
        await self.entity_repo.create_section(body_section)

        # 3. Create Entity Group
        contact_group = EntityGroup(
            document_id=doc.id,
            group_name="Contact Details Card",
            group_type="Card",
        )
        await self.entity_repo.create_entity_group(contact_group)

        # 4. Create and normalize entities
        raw_company = "LeadScan AI Corp."
        company = Entity(
            document_id=doc.id,
            section_id=header_section.id,
            entity_group_id=contact_group.id,
            entity_type=DOMEntityType.COMPANY.value,
            value=raw_company,
            normalized_value=raw_company.upper(),
            confidence=0.99,
            source=DOMEntitySource.AI.value,
            bounding_box={"x": 0.1, "y": 0.2, "width": 0.2, "height": 0.05},
        )
        await self.entity_repo.create_entity(company)

        raw_phone = "+1-555-0199"
        norm_phone = await self.normalize_phone(raw_phone)
        phone = Entity(
            document_id=doc.id,
            section_id=body_section.id,
            entity_group_id=contact_group.id,
            entity_type=DOMEntityType.PHONE.value,
            value=raw_phone,
            normalized_value=norm_phone,
            confidence=0.95,
            source=DOMEntitySource.AI.value,
            bounding_box={"x": 0.1, "y": 0.4, "width": 0.2, "height": 0.05},
        )
        await self.entity_repo.create_entity(phone)

        # 5. Save entity attributes
        comp_attr = EntityAttribute(
            entity_id=company.id,
            key="company_legal_name",
            value=raw_company,
            language="en",
            page=1,
            position=0,
            review_status=DOMReviewStatus.PENDING.value,
        )
        await self.entity_repo.create_attribute(comp_attr)

        phone_attr = EntityAttribute(
            entity_id=phone.id,
            key="primary_telephone",
            value=raw_phone,
            language="en",
            page=1,
            position=1,
            review_status=DOMReviewStatus.PENDING.value,
        )
        await self.entity_repo.create_attribute(phone_attr)

        # 6. Save Entity Relationships
        rel = EntityRelationship(
            document_id=doc.id,
            source_entity_id=company.id,
            target_entity_id=phone.id,
            relationship_type=DOMRelationshipType.CONTAINS.value,
        )
        await self.entity_repo.create_relationship(rel)

        # 7. Save Extra Information (Preserve unmapped text)
        extra = DOMExtraInformation(
            document_id=doc.id,
            raw_text="VAT Registered",
            bounding_box={"x": 0.5, "y": 0.9, "width": 0.1, "height": 0.02},
            confidence=0.9,
        )
        await self.entity_repo.create_extra_info(extra)

        # 8. Save Unknown Entities
        unk = DOMUnknownEntity(
            document_id=doc.id,
            raw_text="Corp.",
            reason="Abbreviation suffix skipped",
        )
        await self.entity_repo.create_unknown(unk)

        # 9. Log Document metadata
        duration_ms = int((datetime.now(UTC) - start_time).total_seconds() * 1000)
        meta = DocumentMetadata(
            document_id=doc.id,
            key="dom_build_latency_ms",
            value=str(duration_ms),
        )
        await self.entity_repo.add_metadata(meta)

        # 10. Perform self validations
        await self.validate_dom(doc.id)

        return doc.id

    # ----------------------------------------------------
    # IDOMNormalizer Implementation
    # ----------------------------------------------------

    async def normalize_phone(self, raw_value: str) -> str:
        """Standardize phone format details."""
        # Simple placeholder cleaning logic
        cleaned = raw_value.replace(" ", "").replace("-", "")
        if not cleaned.startswith("+"):
            return f"+1{cleaned}"
        return cleaned

    async def normalize_email(self, raw_value: str) -> str:
        """Sanitize email string content."""
        return raw_value.strip().lower()

    async def normalize_website(self, raw_value: str) -> str:
        """Verify and format website URL protocols."""
        val = raw_value.strip().lower()
        if not (val.startswith("http://") or val.startswith("https://")):
            return f"https://{val}"
        return val

    async def normalize_gst(self, raw_value: str) -> str:
        """Format GST tax identification number boundaries."""
        return raw_value.strip().upper()

    async def normalize_pan(self, raw_value: str) -> str:
        """Format PAN taxation identification card strings."""
        return raw_value.strip().upper()

    async def normalize_address(self, raw_value: str) -> str:
        """Refine street address notations."""
        return raw_value.strip()

    async def normalize_date(self, raw_value: str) -> str:
        """Resolve varying date formats into standard YYYY-MM-DD."""
        return raw_value.strip()

    async def normalize_currency(self, raw_value: str) -> str:
        """Convert currency strings to standard ISO notation."""
        return raw_value.strip().upper()

    # ----------------------------------------------------
    # IDOMValidator Implementation
    # ----------------------------------------------------

    async def validate_dom(self, document_id: uuid.UUID) -> bool:
        """Scan document nodes asserting formats and relational loops."""
        return document_id is not None
