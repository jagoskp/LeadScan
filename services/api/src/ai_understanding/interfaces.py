import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any


class IAIUnderstandingPipeline(ABC):
    """Interface orchestrating raw text normalization down to semantic results."""

    @abstractmethod
    async def execute_understanding(self, job_id: uuid.UUID) -> Any:
        """Run text normalization, entity resolution, relationship mapping, and log."""
        pass


class IAIProvider(ABC):
    """Interface declaring core LLM / NLP execution methods."""

    @abstractmethod
    async def analyze_document(
        self, raw_text: str, document_type: str
    ) -> dict[str, Any]:
        """Call AI provider and extract entity and semantic relationship graphs."""
        pass


class IEntityResolver(ABC):
    """Interface resolving entity names, types, bounding boxes, and confidence."""

    @abstractmethod
    async def resolve_entities(
        self, raw_text: str
    ) -> list[dict[str, Any]]:
        """Identify individual semantic entities within the text."""
        pass


class IRelationshipDetector(ABC):
    """Interface detecting semantic connections between resolved entities."""

    @abstractmethod
    async def detect_relations(
        self, entities: Sequence[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Trace semantic links (e.g. Person works_for Company)."""
        pass
