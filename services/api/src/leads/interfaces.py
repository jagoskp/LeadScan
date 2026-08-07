from abc import ABC, abstractmethod
from typing import Any, Sequence
import uuid

from services.api.src.leads.schemas import (
    LeadCreateSchema,
    LeadMergeRequestSchema,
    LeadSchema,
    LeadTimelineSchema,
    LeadUpdateSchema,
)


class ILeadRepository(ABC):
    """Abstract interface for Lead persistence layer."""

    @abstractmethod
    async def get_by_id(self, lead_id: uuid.UUID) -> Any:
        pass

    @abstractmethod
    async def list_leads(
        self, search_query: str | None = None, status: str | None = None, is_archived: bool = False, limit: int = 50
    ) -> Sequence[Any]:
        pass

    @abstractmethod
    async def save(self, lead: Any) -> Any:
        pass

    @abstractmethod
    async def delete(self, lead_id: uuid.UUID) -> bool:
        pass


class ILeadService(ABC):
    """Abstract interface for Lead management service operations."""

    @abstractmethod
    async def create_lead(self, request: LeadCreateSchema, actor_id: uuid.UUID | None = None) -> LeadSchema:
        pass

    @abstractmethod
    async def update_lead(
        self, lead_id: uuid.UUID, request: LeadUpdateSchema, actor_id: uuid.UUID | None = None
    ) -> LeadSchema:
        pass

    @abstractmethod
    async def archive_lead(self, lead_id: uuid.UUID, actor_id: uuid.UUID | None = None) -> LeadSchema:
        pass

    @abstractmethod
    async def restore_lead(self, lead_id: uuid.UUID, actor_id: uuid.UUID | None = None) -> LeadSchema:
        pass

    @abstractmethod
    async def merge_leads(self, request: LeadMergeRequestSchema, actor_id: uuid.UUID | None = None) -> LeadSchema:
        pass

    @abstractmethod
    async def get_timeline(self, lead_id: uuid.UUID) -> list[LeadTimelineSchema]:
        pass
