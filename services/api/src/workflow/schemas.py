import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class WorkflowRuleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workflow_id: uuid.UUID
    condition_field: str
    operator: str
    condition_value: str
    action_type: str


class WorkflowSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    trigger_type: str
    is_active: bool
    created_at: datetime
    rules: list[WorkflowRuleSchema] = []


class WorkflowCreateSchema(BaseModel):
    name: str
    trigger_type: str = "lead_created"
    is_active: bool = True


class TaskCreateSchema(BaseModel):
    title: str
    lead_id: uuid.UUID | None = None
    description: str | None = None
    priority: str = "Medium"  # High, Medium, Low
    due_date: datetime | None = None
    assignee_id: uuid.UUID | None = None


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lead_id: uuid.UUID | None = None
    title: str
    description: str | None = None
    priority: str
    status: str
    due_date: datetime | None = None
    assignee_id: uuid.UUID | None = None
    created_at: datetime


class FollowUpCreateSchema(BaseModel):
    lead_id: uuid.UUID
    follow_up_type: str  # phone_call, whatsapp, email, meeting, proposal
    summary: str
    notes: str | None = None
    scheduled_at: datetime


class FollowUpSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lead_id: uuid.UUID
    follow_up_type: str
    summary: str
    notes: str | None = None
    scheduled_at: datetime
    completed_at: datetime | None = None
    is_completed: bool
    created_at: datetime


class ReminderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    task_id: uuid.UUID | None = None
    reminder_time: datetime
    is_triggered: bool
    is_snoozed: bool
    snooze_until: datetime | None = None


class SLASchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lead_id: uuid.UUID
    response_due_at: datetime
    resolution_due_at: datetime
    is_response_breached: bool
    is_resolution_breached: bool


class NotificationQueueSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    channel: str
    recipient: str
    message: str
    status: str
    created_at: datetime
