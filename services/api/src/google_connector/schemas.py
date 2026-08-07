import uuid
from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# OAuth Schemas
class OAuthAuthUrlResponse(BaseModel):
    authorization_url: str
    state: str


class OAuthCallbackRequest(BaseModel):
    code: str
    state: str | None = None
    redirect_uri: str | None = None


class GoogleAccountSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    account_email: str
    account_label: str | None = None
    is_default: bool = False
    is_active: bool = True
    created_at: datetime


# Spreadsheet & Worksheet Schemas
class SpreadsheetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    google_account_id: uuid.UUID
    spreadsheet_id: str
    title: str
    is_favorite: bool = False
    created_at: datetime


class WorksheetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    spreadsheet_id: uuid.UUID
    worksheet_id: str
    title: str
    index: int = 0
    row_count: int = 0
    column_count: int = 0
    is_favorite: bool = False


class SpreadsheetColumnSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    worksheet_id: uuid.UUID
    name: str
    index: int
    data_type: str = "String"
    is_hidden: bool = False
    is_custom: bool = False


# Discovery Request / Response
class ColumnDiscoveryResponse(BaseModel):
    spreadsheet_id: str
    worksheet_title: str
    discovered_headers: list[str]
    column_details: list[SpreadsheetColumnSchema]
    is_cache_hit: bool = False


# Validation & Remapping Schemas
class RemappingSuggestionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source_column: str
    target_entity_field: str
    similarity_score: float
    suggestion_reason: str
    status: Literal["Pending", "Accepted", "Rejected"] = "Pending"


class MappingValidationReportSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sheet_id: str
    worksheet_id: str
    status: Literal["Valid", "MissingColumns", "RenamedColumns", "Invalid"] = "Valid"
    missing_columns: list[str] = []
    new_columns: list[str] = []
    suggestions: list[RemappingSuggestionSchema] = []
    report_data: dict[str, Any] = {}
    created_at: datetime


class PreSyncCheckRequest(BaseModel):
    profile_id: uuid.UUID
    spreadsheet_id: str
    worksheet_title: str


# Sync Schemas
class SyncExecutionRequest(BaseModel):
    profile_id: uuid.UUID
    spreadsheet_id: str
    worksheet_title: str
    sync_mode: Literal["Realtime", "Manual", "Scheduled", "Batch", "Retry"] = "Manual"
    rows_data: list[dict[str, Any]]
    auto_apply_remapping: bool = True


class SyncJobSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    profile_id: uuid.UUID | None = None
    spreadsheet_id: str
    worksheet_id: str
    sync_mode: str
    status: str
    total_rows: int = 0
    processed_rows: int = 0
    success_rows: int = 0
    failed_rows: int = 0
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime


class SyncHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    job_id: uuid.UUID
    spreadsheet_id: str
    worksheet_id: str
    rows_processed: int
    duration_ms: int
    retries: int
    status: str
    error_message: str | None = None
    validation_result: dict[str, Any] | None = None
    created_at: datetime
