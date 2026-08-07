import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import UTC, datetime

from services.api.src.workflow.models import SLA, FollowUp, Reminder, Task, Workflow
from services.api.src.workflow.schemas import FollowUpCreateSchema, TaskCreateSchema, WorkflowCreateSchema
from services.api.src.workflow.service import WorkflowService
from services.api.src.workflow.validators import validate_task_priority


def test_task_priority_validator():
    assert validate_task_priority("High") == "High"
    assert validate_task_priority("Medium") == "Medium"
    with pytest.raises(Exception):
        validate_task_priority("INVALID_PRIORITY")


@pytest.fixture
def mock_db():
    db = AsyncMock()
    now = datetime.now(UTC)
    task_id = uuid.uuid4()
    lead_id = uuid.uuid4()

    mock_task = Task(
        id=task_id,
        lead_id=lead_id,
        title="Schedule Product Demo",
        description="Demo product features",
        priority="High",
        status="Pending",
        due_date=now,
        assignee_id=None,
        created_at=now,
        updated_at=now,
    )

    mock_wf = Workflow(
        id=uuid.uuid4(),
        name="Auto Lead Qualification",
        trigger_type="lead_created",
        is_active=True,
        created_at=now,
        updated_at=now,
        rules=[],
    )

    mock_followup = FollowUp(
        id=uuid.uuid4(),
        lead_id=lead_id,
        follow_up_type="phone_call",
        summary="Initial Discovery Call",
        scheduled_at=now,
        is_completed=False,
        created_at=now,
    )

    mock_sla = SLA(
        id=uuid.uuid4(),
        lead_id=lead_id,
        response_due_at=now,
        resolution_due_at=now,
        is_response_breached=False,
        is_resolution_breached=False,
        created_at=now,
    )

    async def mock_execute(stmt, *args, **kwargs):
        res = MagicMock()
        res.scalars.return_value.first.return_value = mock_task
        res.scalars.return_value.all.return_value = [mock_task]
        return res

    async def mock_get(entity_cls, entity_id):
        if entity_cls == Task:
            return mock_task
        return mock_task

    db.execute.side_effect = mock_execute
    db.get.side_effect = mock_get
    return db, lead_id, mock_task


@pytest.mark.asyncio
async def test_create_and_complete_task(mock_db):
    db, lead_id, mock_task = mock_db
    service = WorkflowService(db)

    req = TaskCreateSchema(title="Schedule Product Demo", lead_id=lead_id, priority="High")
    t = await service.create_task(req)
    assert t.title == "Schedule Product Demo"

    c_task = await service.complete_task(mock_task.id)
    assert c_task.status == "Completed"


@pytest.mark.asyncio
async def test_schedule_followup_and_sla(mock_db):
    db, lead_id, _ = mock_db
    service = WorkflowService(db)

    fu_req = FollowUpCreateSchema(
        lead_id=lead_id,
        follow_up_type="phone_call",
        summary="Initial Discovery Call",
        scheduled_at=datetime.now(UTC),
    )
    fu = await service.schedule_followup(fu_req)
    assert fu.follow_up_type == "phone_call"

    sla = await service.create_sla_target(lead_id)
    assert sla.is_response_breached is False
