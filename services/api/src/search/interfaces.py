from abc import ABC, abstractmethod
from typing import Any
import uuid

from services.api.src.search.schemas import (
    AutocompleteSuggestionSchema,
    SavedSearchCreateSchema,
    SavedSearchSchema,
    UniversalSearchRequest,
    UniversalSearchResponse,
)


class ISearchService(ABC):
    """Abstract interface for Universal Search Platform operations."""

    @abstractmethod
    async def execute_universal_search(
        self, request: UniversalSearchRequest, user_id: uuid.UUID
    ) -> UniversalSearchResponse:
        pass

    @abstractmethod
    async def get_autocomplete_suggestions(
        self, prefix: str, limit: int = 5
    ) -> list[AutocompleteSuggestionSchema]:
        pass

    @abstractmethod
    async def save_search(
        self, user_id: uuid.UUID, request: SavedSearchCreateSchema
    ) -> SavedSearchSchema:
        pass

    @abstractmethod
    async def list_saved_searches(self, user_id: uuid.UUID) -> list[SavedSearchSchema]:
        pass


class IQueryParser(ABC):
    """Abstract interface for Boolean, prefix, phrase, and field query parsing."""

    @abstractmethod
    def parse(self, raw_query: str) -> dict[str, Any]:
        pass


class IRankingEngine(ABC):
    """Abstract interface for multi-field relevance scoring and ranking."""

    @abstractmethod
    def score_and_rank(self, items: list[dict[str, Any]], parsed_query: dict[str, Any]) -> list[dict[str, Any]]:
        pass
