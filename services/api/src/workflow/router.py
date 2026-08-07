import logging
from typing import Any
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.workflow.exceptions import WorkflowException
from services.api.src.workflow.schemas import (
    FollowUpCreateSchema,
    FollowUpSchema,
    SLASchema,
    TaskCreateSchema,
    TaskSchema,
    WorkflowCreateSchema,
    WorkflowSchema,
)
from services.api.src.workflow.service import WorkflowService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/workflows", tags=["Enterprise Workflow & Automation Engine"])
templates_router = router
executions_router = router


@router.get("", response_model=list[WorkflowSchema])
async def list_workflows(db: AsyncSession = Depends(get_db)):
    """List workflow automation rule definitions."""
    service = WorkflowService(db)
    return await service.list_workflows()


@router.post("", response_model=WorkflowSchema, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    payload: WorkflowCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Create new workflow automation rule."""
    service = WorkflowService(db)
    return await service.create_workflow(payload)


@router.get("/tasks", response_model=list[TaskSchema])
async def list_tasks(
    lead_id: uuid.UUID | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List tasks across leads or filtered by status."""
    service = WorkflowService(db)
    return await service.list_tasks(lead_id=lead_id, status=status_filter, limit=limit)


@router.post("/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Create new task item."""
    try:
        service = WorkflowService(db)
        return await service.create_task(payload)
    except WorkflowException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/tasks/{task_id}/complete", response_model=TaskSchema)
async def complete_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Mark a task item as completed."""
    try:
        service = WorkflowService(db)
        return await service.complete_task(task_id)
    except WorkflowException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/followups", response_model=list[FollowUpSchema])
async def list_followups(
    lead_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    """List follow-up activities."""
    service = WorkflowService(db)
    return await service.list_followups(lead_id=lead_id)


@router.post("/followups", response_model=FollowUpSchema, status_code=status.HTTP_201_CREATED)
async def schedule_followup(
    payload: FollowUpCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Schedule follow-up communication activity (Call, WhatsApp, Email, Meeting)."""
    service = WorkflowService(db)
    return await service.schedule_followup(payload)


@router.post("/sla", response_model=SLASchema, status_code=status.HTTP_201_CREATED)
async def create_sla_target(
    lead_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Initialize SLA response and resolution targets for a lead."""
    service = WorkflowService(db)
    return await service.create_sla_target(lead_id)
