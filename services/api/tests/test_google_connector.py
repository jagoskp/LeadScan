import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import UTC, datetime, timedelta

from services.api.src.google_connector.exceptions import (
    GoogleAuthException,
    MappingValidationException,
    SpreadsheetNotFoundException,
)
from services.api.src.google_connector.models import GoogleAccount, GoogleToken, SpreadsheetColumn, Worksheet
from services.api.src.google_connector.oauth import GoogleOAuthService
from services.api.src.google_connector.sheets import GoogleSheetsService
from services.api.src.google_connector.column_discovery import ColumnDiscoveryService
from services.api.src.google_connector.remapping_assistant import (
    AutoRemappingAssistant,
    calculate_similarity,
)
from services.api.src.google_connector.mapping_validator import PreSyncMappingValidator
from services.api.src.google_connector.sync import GoogleSyncEngine
from services.api.src.google_connector.schemas import SyncExecutionRequest


@pytest.fixture
def mock_db():
    db = AsyncMock()
    mock_token = GoogleToken(
        id=uuid.uuid4(),
        google_account_id=uuid.uuid4(),
        access_token_enc="mock_access_token_12345",
        refresh_token_enc="mock_refresh_token_12345",
        expires_at=datetime.now(UTC) + timedelta(hours=1),
        is_valid=True,
    )
    mock_account = GoogleAccount(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        account_email="test@google.com",
        is_active=True,
    )

    async def mock_execute(stmt, *args, **kwargs):
        res = MagicMock()
        stmt_str = str(stmt)
        if "google_tokens" in stmt_str:
            res.scalars.return_value.first.return_value = mock_token
            res.scalars.return_value.all.return_value = [mock_token]
        elif "google_accounts" in stmt_str:
            res.scalars.return_value.first.return_value = mock_account
            res.scalars.return_value.all.return_value = [mock_account]
        elif "google_spreadsheet_columns" in stmt_str:
            dummy_col = SpreadsheetColumn(
                id=uuid.uuid4(),
                worksheet_id=uuid.uuid4(),
                name="Business Name",
                index=0,
                data_type="String",
            )
            res.scalars.return_value.first.return_value = dummy_col
            res.scalars.return_value.all.return_value = [dummy_col]
        else:
            res.scalars.return_value.first.return_value = None
            res.scalars.return_value.all.return_value = []
        return res

    db.execute.side_effect = mock_execute
    return db


@pytest.mark.asyncio
async def test_oauth_auth_url(mock_db):
    user_id = uuid.uuid4()
    oauth_service = GoogleOAuthService(mock_db)

    auth_url_res = await oauth_service.get_authorization_url(user_id)
    assert "accounts.google.com" in auth_url_res.authorization_url
    assert auth_url_res.state.startswith("user_")


@pytest.mark.asyncio
async def test_oauth_callback_and_disconnect(mock_db):
    user_id = uuid.uuid4()
    oauth_service = GoogleOAuthService(mock_db)

    callback_res = await oauth_service.handle_oauth_callback(user_id, "mock_code_12345")
    assert callback_res["status"] == "connected"
    assert "account_id" in callback_res

    account_id = uuid.uuid4()
    token = await oauth_service.get_valid_access_token(account_id)
    assert token.startswith("mock_")


@pytest.mark.asyncio
async def test_auto_remapping_similarity():
    assistant = AutoRemappingAssistant()

    # Exact synonym test
    score_email = calculate_similarity("Email ID", "Email")
    assert score_email >= 0.9

    score_company = calculate_similarity("Company Name", "Business Name")
    assert score_company >= 0.9

    # Suggestions generation
    suggestions = assistant.generate_suggestions(
        missing_columns=["Email ID", "Company Name"],
        discovered_headers=["Business Name", "Email", "Phone"],
    )
    assert len(suggestions) == 2


@pytest.mark.asyncio
async def test_column_discovery_and_pre_sync_validator(mock_db):
    oauth_service = GoogleOAuthService(mock_db)
    sheets_service = GoogleSheetsService(oauth_service)
    discovery_service = ColumnDiscoveryService(mock_db, sheets_service)
    remapping_assistant = AutoRemappingAssistant()
    validator = PreSyncMappingValidator(mock_db, remapping_assistant)

    account_id = uuid.uuid4()

    # Column Discovery
    discovery_res = await discovery_service.discover_columns(
        account_id=account_id,
        spreadsheet_id="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
        worksheet_title="Leads",
    )
    assert len(discovery_res.discovered_headers) > 0
    assert "Business Name" in discovery_res.discovered_headers

    # Pre-sync check
    profile_id = uuid.uuid4()
    val_report = await validator.validate_mapping(
        profile_id=profile_id,
        spreadsheet_id="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
        worksheet_title="Leads",
        discovered_headers=discovery_res.discovered_headers,
    )
    assert val_report.status in ["Valid", "MissingColumns", "RenamedColumns"]


@pytest.mark.asyncio
async def test_sync_execution(mock_db):
    oauth_service = GoogleOAuthService(mock_db)
    sheets_service = GoogleSheetsService(oauth_service)
    discovery_service = ColumnDiscoveryService(mock_db, sheets_service)
    remapping_assistant = AutoRemappingAssistant()
    validator = PreSyncMappingValidator(mock_db, remapping_assistant)
    sync_engine = GoogleSyncEngine(mock_db, sheets_service, discovery_service, validator)

    account_id = uuid.uuid4()
    user_id = uuid.uuid4()
    profile_id = uuid.uuid4()

    sync_req = SyncExecutionRequest(
        profile_id=profile_id,
        spreadsheet_id="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
        worksheet_title="Leads",
        sync_mode="Manual",
        rows_data=[
            {"Business Name": "Acme Corp", "Email": "acme@example.com", "Phone Number": "123456"},
            {"Business Name": "Beta LLC", "Email": "beta@example.com", "Phone Number": "654321"},
        ],
        auto_apply_remapping=True,
    )

    job = await sync_engine.execute_sync_job(account_id, sync_req, user_id)
    assert job.status == "Completed"
    assert job.success_rows == 2
