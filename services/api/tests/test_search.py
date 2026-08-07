import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import UTC, datetime

from services.api.src.search.filters import SearchFilterEngine
from services.api.src.search.indexer import SearchIndexer
from services.api.src.search.query_parser import SearchQueryParser
from services.api.src.search.ranking import SearchRankingEngine
from services.api.src.search.repository import SearchRepository
from services.api.src.search.schemas import (
    SavedSearchCreateSchema,
    UniversalSearchFilterSchema,
    UniversalSearchRequest,
)
from services.api.src.search.service import SearchService


def test_query_parser_boolean_and_fields():
    parser = SearchQueryParser()
    raw = 'Acme AND gst:27AAAAA0000A1Z5 OR tag:HighValue "Global Logistics"'
    parsed = parser.parse(raw)

    assert parsed["exact_phrases"] == ["Global Logistics"]
    assert parsed["field_specs"]["gst"] == "27AAAAA0000A1Z5"
    assert parsed["field_specs"]["tag"] == "HighValue"
    assert parsed["boolean_operators"]["AND"] is True
    assert parsed["boolean_operators"]["OR"] is True


def test_ranking_engine_exact_match_boost():
    ranking = SearchRankingEngine()
    now = datetime.now(UTC)

    items = [
        {"id": uuid.uuid4(), "title": "Acme Corp", "company_name": "Acme", "gst_number": "27AAAAA", "created_at": now},
        {"id": uuid.uuid4(), "title": "Random Lead", "company_name": "Beta", "gst_number": "12345", "created_at": now},
    ]

    parser = SearchQueryParser()
    parsed = parser.parse("Acme Corp")

    ranked = ranking.score_and_rank(items, parsed)
    assert len(ranked) == 2
    assert ranked[0]["title"] == "Acme Corp"
    assert ranked[0]["score"] >= 50.0


def test_search_filter_engine():
    filter_engine = SearchFilterEngine()
    items = [
        {"id": uuid.uuid4(), "company_name": "Acme Corp", "status": "New", "source_type": "Lead Repository"},
        {"id": uuid.uuid4(), "company_name": "Beta Industries", "status": "Qualified", "source_type": "Lead Repository"},
    ]

    filters = UniversalSearchFilterSchema(status="New", company_name="Acme")
    filtered = filter_engine.filter_items(items, filters)

    assert len(filtered) == 1
    assert filtered[0]["company_name"] == "Acme Corp"


@pytest.fixture
def mock_db():
    db = AsyncMock()
    now = datetime.now(UTC)
    mock_lead = MagicMock()
    mock_lead.id = uuid.uuid4()
    mock_lead.title = "Acme Global Lead"
    mock_lead.company_id = uuid.uuid4()
    mock_lead.company = MagicMock(company_name="Acme Global", gst_number="27AAAAA0000A1Z5")
    mock_lead.contacts = [MagicMock(id=uuid.uuid4(), emails=["info@acme.com"], phones=["+15550192831"])]
    mock_lead.created_at = now
    mock_lead.status = "New"

    async def mock_execute(stmt, *args, **kwargs):
        res = MagicMock()
        res.scalars.return_value.first.return_value = mock_lead
        res.scalars.return_value.all.return_value = [mock_lead]
        return res

    db.execute.side_effect = mock_execute
    return db


@pytest.mark.asyncio
async def test_universal_search_execution(mock_db):
    service = SearchService(mock_db)
    user_id = uuid.uuid4()
    req = UniversalSearchRequest(query="Acme", page=1, page_size=10)

    res = await service.execute_universal_search(req, user_id)
    assert res.total_matches == 1
    assert res.results[0].title == "Acme Global Lead"


@pytest.mark.asyncio
async def test_autocomplete_suggestions(mock_db):
    service = SearchService(mock_db)
    suggestions = await service.get_autocomplete_suggestions("Acme", limit=5)
    assert len(suggestions) > 0
    assert "Acme" in suggestions[0].suggestion
