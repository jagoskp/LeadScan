import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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


class DocumentRepository:
    """Repository handling persistence operations for DOM Documents."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, doc: Document) -> Document:
        """Persist a new DOM Document root."""
        self.session.add(doc)
        await self.session.flush()
        return doc

    async def get_by_id(self, doc_id: uuid.UUID) -> Document | None:
        """Retrieve a specific DOM Document preloading all tree partitions."""
        stmt = (
            select(Document)
            .where(Document.id == doc_id)
            .options(
                selectinload(Document.sections).selectinload(
                    DocumentSection.entities
                ),
                selectinload(Document.entity_groups).selectinload(
                    EntityGroup.entities
                ),
                selectinload(Document.extra_informations),
                selectinload(Document.unknown_entities),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_documents(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[Document]:
        """List DOM documents filtered by user context and organization."""
        stmt = select(Document).options(
            selectinload(Document.sections),
        )
        filters = []
        if user_id:
            filters.append(Document.user_id == user_id)
        if organization_id:
            filters.append(Document.organization_id == organization_id)
        if filters:
            stmt = stmt.where(and_(*filters))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_status(
        self, doc_id: uuid.UUID, status: str
    ) -> Document | None:
        """Update document review status."""
        stmt = (
            update(Document)
            .where(Document.id == doc_id)
            .values(status=status)
        )
        await self.session.execute(stmt)
        return await self.get_by_id(doc_id)

    async def delete(self, doc_id: uuid.UUID) -> bool:
        """Delete a DOM Document root by ID."""
        stmt = delete(Document).where(Document.id == doc_id)
        result = await self.session.execute(stmt)
        return bool(getattr(result, "rowcount", 0))


class EntityRepository:
    """Repository handling persistence operations for elements and relations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_section(self, section: DocumentSection) -> DocumentSection:
        """Persist a new DocumentSection."""
        self.session.add(section)
        await self.session.flush()
        return section

    async def create_entity_group(self, group: EntityGroup) -> EntityGroup:
        """Persist a new EntityGroup."""
        self.session.add(group)
        await self.session.flush()
        return group

    async def create_entity(self, entity: Entity) -> Entity:
        """Persist a new Entity node."""
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def get_entity_by_id(self, entity_id: uuid.UUID) -> Entity | None:
        """Retrieve an Entity node preloading its attributes."""
        stmt = (
            select(Entity)
            .where(Entity.id == entity_id)
            .options(selectinload(Entity.attributes))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_attribute(self, attr: EntityAttribute) -> EntityAttribute:
        """Persist a new EntityAttribute."""
        self.session.add(attr)
        await self.session.flush()
        return attr

    async def get_attribute_by_id(self, attr_id: uuid.UUID) -> EntityAttribute | None:
        """Retrieve a specific EntityAttribute."""
        stmt = select(EntityAttribute).where(EntityAttribute.id == attr_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_attribute(
        self, attr_id: uuid.UUID, data: dict[str, Any]
    ) -> EntityAttribute | None:
        """Update an EntityAttribute's values or status configurations."""
        if data:
            stmt = (
                update(EntityAttribute)
                .where(EntityAttribute.id == attr_id)
                .values(**data)
            )
            await self.session.execute(stmt)
        return await self.get_attribute_by_id(attr_id)

    async def create_relationship(
        self, relation: EntityRelationship
    ) -> EntityRelationship:
        """Persist a new EntityRelationship link."""
        self.session.add(relation)
        await self.session.flush()
        return relation

    async def create_extra_info(self, info: DOMExtraInformation) -> DOMExtraInformation:
        """Persist a DOMExtraInformation unmapped text log."""
        self.session.add(info)
        await self.session.flush()
        return info

    async def create_unknown(self, unknown: DOMUnknownEntity) -> DOMUnknownEntity:
        """Persist a DOMUnknownEntity record."""
        self.session.add(unknown)
        await self.session.flush()
        return unknown

    async def add_metadata(self, metadata: DocumentMetadata) -> DocumentMetadata:
        """Persist DocumentMetadata latency stats."""
        self.session.add(metadata)
        await self.session.flush()
        return metadata
