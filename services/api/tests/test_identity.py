import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import UTC, datetime

from services.api.src.identity.conflict import ConflictResolver
from services.api.src.identity.matcher import IdentityMatcher
from services.api.src.identity.models import DuplicateMatch, MergeHistory, RollbackHistory
from services.api.src.identity.schemas import MergeExecuteRequest
from services.api.src.identity.scorer import IdentityScorer
from services.api.src.identity.service import IdentityService
from services.api.src.leads.models import Company, Contact, Lead


def test_identity_matcher_exact_gst_and_phone():
    matcher = IdentityMatcher()
    lead_a = {"title": "Acme Corp", "company_name": "Acme", "gst_number": "27AAAAA0000A1Z5", "phone": "+15550192831"}
    lead_b = {"title": "Acme Corp", "company_name": "Acme", "gst_number": "27AAAAA0000A1Z5", "phone": "+15550192831"}

    res = matcher.evaluate_match(lead_a, lead_b)
    assert res["is_exact_match"] is True
    assert "Exact GST Match" in res["match_reasons"]


def test_identity_scorer_confidence():
    scorer = IdentityScorer()
    eval_exact = {"is_exact_match": True}
    scores = scorer.compute_scores(eval_exact)
    assert scores["duplicate_score"] == 100.0
    assert scores["confidence_level"] == "100%"

    eval_fuzzy = {"is_exact_match": False, "title_similarity": 0.85, "company_similarity": 0.85}
    scores_fuzzy = scorer.compute_scores(eval_fuzzy)
    assert scores_fuzzy["duplicate_score"] == 85.0
    assert scores_fuzzy["confidence_level"] == "High"


def test_conflict_resolver_policies():
    resolver = ConflictResolver()
    val_orig, _ = resolver.resolve_field_conflict("title", "Acme Original", "Acme Updated", policy="keep_original")
    assert val_orig == "Acme Original"

    val_latest, _ = resolver.resolve_field_conflict("title", "Acme Original", "Acme Updated", policy="keep_latest")
    assert val_latest == "Acme Updated"


@pytest.fixture
def mock_db_fixture():
    db = AsyncMock()
    now = datetime.now(UTC)

    lead_p_id = uuid.uuid4()
    lead_s_id = uuid.uuid4()

    primary_lead = Lead(
        id=lead_p_id,
        title="Primary Acme Lead",
        status="New",
        priority="High",
        source="Scan",
        lead_score=90.0,
        is_favorite=False,
        is_archived=False,
        created_at=now,
        updated_at=now,
        company=Company(id=uuid.uuid4(), company_name="Acme Corp", gst_number="27AAAAA0000A1Z5"),
        contacts=[Contact(id=uuid.uuid4(), first_name="Jane", emails=["jane@acme.com"], phones=["+15550192831"])],
        tags=[],
        notes=[],
    )

    secondary_lead = Lead(
        id=lead_s_id,
        title="Secondary Acme Lead",
        status="New",
        priority="Medium",
        source="Scan",
        lead_score=80.0,
        is_favorite=False,
        is_archived=False,
        created_at=now,
        updated_at=now,
        company=Company(id=uuid.uuid4(), company_name="Acme Corp", gst_number="27AAAAA0000A1Z5"),
        contacts=[Contact(id=uuid.uuid4(), first_name="John", emails=["john@acme.com"], phones=["+15550192832"])],
        tags=[],
        notes=[],
    )

    async def mock_execute(stmt, *args, **kwargs):
        res = MagicMock()
        stmt_str = str(stmt)

        if str(lead_s_id) in stmt_str:
            res.scalars.return_value.first.return_value = secondary_lead
            res.scalars.return_value.all.return_value = [secondary_lead]
        elif str(lead_p_id) in stmt_str:
            res.scalars.return_value.first.return_value = primary_lead
            res.scalars.return_value.all.return_value = [primary_lead]
        else:
            res.scalars.return_value.first.return_value = primary_lead
            res.scalars.return_value.all.return_value = [primary_lead, secondary_lead]
        return res

    async def mock_get(entity_cls, entity_id):
        if str(entity_id) == str(lead_s_id):
            return secondary_lead
        return primary_lead

    db.execute.side_effect = mock_execute
    db.get.side_effect = mock_get
    return db, lead_p_id, lead_s_id, primary_lead, secondary_lead


@pytest.mark.asyncio
async def test_identity_service_scan(mock_db_fixture):
    db, lead_p_id, lead_s_id, primary_lead, secondary_lead = mock_db_fixture
    service = IdentityService(db)

    # Directly evaluate matcher & scorer for unit validation
    eval_a = {"title": primary_lead.title, "company_name": "Acme Corp", "gst_number": "27AAAAA0000A1Z5"}
    eval_b = {"title": secondary_lead.title, "company_name": "Acme Corp", "gst_number": "27AAAAA0000A1Z5"}

    m_eval = service.matcher.evaluate_match(eval_a, eval_b)
    scores = service.scorer.compute_scores(m_eval)

    assert scores["duplicate_score"] >= 50.0
    assert scores["confidence_level"] == "100%"


@pytest.mark.asyncio
async def test_merge_preview_and_execute(mock_db_fixture):
    db, p_id, s_id, primary_lead, secondary_lead = mock_db_fixture
    service = IdentityService(db)

    # Patch repo.get_by_id for precise control
    service.lead_repo.get_by_id = AsyncMock(side_effect=lambda lid: primary_lead if lid == p_id else secondary_lead)

    preview = await service.get_merge_preview(p_id, s_id)
    assert preview.has_conflicts is True
    assert preview.primary_title == "Primary Acme Lead"
    assert preview.secondary_title == "Secondary Acme Lead"

    req = MergeExecuteRequest(primary_lead_id=p_id, secondary_lead_ids=[s_id])
    res = await service.execute_merge(req)
    assert res.primary_lead_id == p_id
