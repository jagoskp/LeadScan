import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import UTC, datetime

from services.api.src.leads.enums import LeadStatusEnum, TimelineEventTypeEnum
from services.api.src.leads.exceptions import (
    LeadAlreadyArchivedException,
    LeadNotFoundException,
)
from services.api.src.leads.models import Company, Contact, Lead, LeadMetadata, LeadTimeline
from services.api.src.leads.repository import LeadRepository
from services.api.src.leads.service import LeadService
from services.api.src.leads.schemas import (
    CompanyCreateSchema,
    ContactCreateSchema,
    LeadCreateSchema,
    LeadMergeRequestSchema,
    LeadUpdateSchema,
)


@pytest.fixture
def mock_db():
    db = AsyncMock()
    now = datetime.now(UTC)
    lead_id = uuid.uuid4()
    mock_lead = Lead(
        id=lead_id,
        title="Test Lead Acme",
        status="New",
        priority="High",
        source="Camera Scan",
        lead_score=85.0,
        is_favorite=False,
        is_archived=False,
        created_at=now,
        updated_at=now,
        company=Company(
            id=uuid.uuid4(),
            company_name="Acme Corp",
            gst_number="27AAAAA0000A1Z5",
            departments=[],
            created_at=now,
            updated_at=now,
        ),
        contacts=[
            Contact(
                id=uuid.uuid4(),
                lead_id=lead_id,
                first_name="Jane",
                last_name="Doe",
                is_primary=True,
                emails=["jane@acme.com"],
                phones=["+15550192831"],
                websites=[],
                addresses=[],
                social_profiles=[],
                custom_fields={},
                created_at=now,
                updated_at=now,
            )
        ],
        tags=[],
        notes=[],
        timeline_records=[],
        lead_metadata=LeadMetadata(
            id=uuid.uuid4(),
            lead_id=lead_id,
            original_image_url="http://example.com/scan.jpg",
            ocr_raw_output={"text": "Acme Corp"},
            ai_understanding_output={"confidence": 0.98},
            dom_entity_snapshot={"entity": "Company"},
            created_at=now,
        ),
    )

    async def mock_execute(stmt, *args, **kwargs):
        res = MagicMock()
        res.scalars.return_value.first.return_value = mock_lead
        res.scalars.return_value.all.return_value = [mock_lead]
        return res

    db.execute.side_effect = mock_execute
    return db


@pytest.mark.asyncio
async def test_create_lead(mock_db):
    service = LeadService(mock_db)
    req = LeadCreateSchema(
        title="Global Logistics Lead",
        status="New",
        priority="Medium",
        source="Camera Scan",
        lead_score=90.0,
        company=CompanyCreateSchema(company_name="Global Logistics", gst_number="29BBBBA0000B1Z2"),
        contacts=[
            ContactCreateSchema(
                first_name="John",
                last_name="Smith",
                emails=["john@globallogistics.com"],
                phones=["+15550129948"],
            )
        ],
        tags=["HighValue"],
        notes=["Key prospective client"],
    )

    result = await service.create_lead(req)
    assert result.title == "Test Lead Acme"
    assert result.status == "New"


@pytest.mark.asyncio
async def test_get_lead_detail(mock_db):
    service = LeadService(mock_db)
    lead_id = uuid.uuid4()
    result = await service.get_lead(lead_id)
    assert result.title == "Test Lead Acme"
    assert result.company is not None
    assert result.company.company_name == "Acme Corp"


@pytest.mark.asyncio
async def test_update_lead(mock_db):
    service = LeadService(mock_db)
    lead_id = uuid.uuid4()
    update_req = LeadUpdateSchema(status="Qualified", priority="Urgent", is_favorite=True)
    result = await service.update_lead(lead_id, update_req)
    assert result.id is not None


@pytest.mark.asyncio
async def test_archive_and_restore_lead(mock_db):
    service = LeadService(mock_db)
    lead_id = uuid.uuid4()

    archived = await service.archive_lead(lead_id)
    assert archived.id is not None

    restored = await service.restore_lead(lead_id)
    assert restored.id is not None


@pytest.mark.asyncio
async def test_merge_leads(mock_db):
    service = LeadService(mock_db)
    primary_id = uuid.uuid4()
    sec_id = uuid.uuid4()

    merge_req = LeadMergeRequestSchema(
        primary_lead_id=primary_id,
        secondary_lead_ids=[sec_id],
    )
    result = await service.merge_leads(merge_req)
    assert result.id is not None
