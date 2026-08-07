import logging
from typing import Any
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.search.filters import SearchFilterEngine
from services.api.src.search.indexer import SearchIndexer
from services.api.src.search.interfaces import ISearchService
from services.api.src.search.query_parser import SearchQueryParser
from services.api.src.search.ranking import SearchRankingEngine
from services.api.src.search.repository import SearchRepository
from services.api.src.search.schemas import (
    AutocompleteSuggestionSchema,
    RecentSearchSchema,
    SavedSearchCreateSchema,
    SavedSearchSchema,
    SearchResultItemSchema,
    UniversalSearchRequest,
    UniversalSearchResponse,
)
from services.api.src.search.validators import validate_search_query

logger = logging.getLogger(__name__)


class SearchService(ISearchService):
    """Facade Service for Enterprise Universal Search Engine Platform."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = SearchRepository(db)
        self.parser = SearchQueryParser()
        self.ranking = SearchRankingEngine()
        self.filter_engine = SearchFilterEngine()
        self.indexer = SearchIndexer(db)

    async def execute_universal_search(
        self, request: UniversalSearchRequest, user_id: uuid.UUID
    ) -> UniversalSearchResponse:
        """Parse query, execute database search, filter, score & rank results."""
        query_str = validate_search_query(request.query)

        # 1. Parse Query
        parsed = self.parser.parse(query_str)

        # 2. Execute DB search across all platform entities
        raw_items = await self.repo.global_query_indices(query_str, limit=100)

        # 3. Filter Items
        filtered_items = self.filter_engine.filter_items(raw_items, request.filters)

        # 4. Score & Rank Results
        ranked_items = self.ranking.score_and_rank(filtered_items, parsed)

        # 5. Log Search History
        await self.repo.log_search_history(
            user_id=user_id,
            query=query_str,
            filters=request.filters.model_dump() if request.filters else None,
            count=len(ranked_items),
        )

        # Pagination
        start = (request.page - 1) * request.page_size
        end = start + request.page_size
        paged_items = ranked_items[start:end]

        results = [
            SearchResultItemSchema(
                id=item["id"],
                lead_id=item.get("lead_id"),
                document_id=item.get("document_id"),
                company_id=item.get("company_id"),
                contact_id=item.get("contact_id"),
                title=item["title"],
                company_name=item.get("company_name"),
                gst_number=item.get("gst_number"),
                email=item.get("email"),
                phone=item.get("phone"),
                matched_field=item.get("matched_field", "Content"),
                highlighted_match=item.get("highlighted_match", f"Query match: {query_str}"),
                score=item.get("score", 10.0),
                source_type=item.get("source_type", "Platform Search"),
                created_at=item["created_at"],
            )
            for item in paged_items
        ]

        return UniversalSearchResponse(
            query=query_str,
            total_matches=len(ranked_items),
            results=results,
            page=request.page,
            page_size=request.page_size,
        )

    async def get_autocomplete_suggestions(
        self, prefix: str, limit: int = 5
    ) -> list[AutocompleteSuggestionSchema]:
        if not prefix or len(prefix.strip()) < 1:
            return []

        raw_items = await self.repo.global_query_indices(prefix, limit=20)
        suggestions: list[AutocompleteSuggestionSchema] = []
        seen = set()

        for item in raw_items:
            title = item.get("title")
            company = item.get("company_name")
            gst = item.get("gst_number")

            for text, field in [(title, "Title"), (company, "Company"), (gst, "GST")]:
                if text and prefix.lower() in text.lower() and text not in seen:
                    seen.add(text)
                    suggestions.append(
                        AutocompleteSuggestionSchema(
                            suggestion=text,
                            target_field=field,
                            score=1.0 if text.lower().startswith(prefix.lower()) else 0.8,
                        )
                    )
                    if len(suggestions) >= limit:
                        break

        return suggestions

    async def save_search(
        self, user_id: uuid.UUID, request: SavedSearchCreateSchema
    ) -> SavedSearchSchema:
        saved = await self.repo.save_search(
            user_id=user_id,
            title=request.title,
            query=request.query_string,
            filters=request.filters,
            is_pinned=request.is_pinned,
        )
        return SavedSearchSchema.model_validate(saved)

    async def list_saved_searches(self, user_id: uuid.UUID) -> list[SavedSearchSchema]:
        saved_list = await self.repo.list_saved_searches(user_id)
        return [SavedSearchSchema.model_validate(s) for s in saved_list]

    async def list_recent_searches(self, user_id: uuid.UUID, limit: int = 10) -> list[RecentSearchSchema]:
        history = await self.repo.list_recent_searches(user_id, limit)
        return [RecentSearchSchema.model_validate(h) for h in history]
