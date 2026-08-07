import logging
import time
from datetime import UTC, datetime
from typing import Any
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.google_connector.column_discovery import ColumnDiscoveryService
from services.api.src.google_connector.exceptions import MappingValidationException
from services.api.src.google_connector.mapping_validator import PreSyncMappingValidator
from services.api.src.google_connector.models import GoogleSyncHistory, GoogleSyncJob
from services.api.src.google_connector.schemas import SyncExecutionRequest, SyncJobSchema
from services.api.src.google_connector.sheets import GoogleSheetsService

logger = logging.getLogger(__name__)


class GoogleSyncEngine:
    """Core Sync Engine handling Append, Update, Upsert, and Batch sync operations to Google Sheets."""

    def __init__(
        self,
        db: AsyncSession,
        sheets_service: GoogleSheetsService,
        column_discovery: ColumnDiscoveryService,
        mapping_validator: PreSyncMappingValidator,
    ):
        self.db = db
        self.sheets_service = sheets_service
        self.column_discovery = column_discovery
        self.mapping_validator = mapping_validator

    async def execute_sync_job(
        self,
        account_id: uuid.UUID,
        request: SyncExecutionRequest,
        user_id: uuid.UUID | None = None,
    ) -> SyncJobSchema:
        """Run pre-sync check, format data based on dynamic headers, execute sheet write, and log history."""
        start_time = time.perf_counter()

        # Step 1: Discover Headers
        discovery_res = await self.column_discovery.discover_columns(
            account_id=account_id,
            spreadsheet_id=request.spreadsheet_id,
            worksheet_title=request.worksheet_title,
            force_refresh=True,
        )
        headers = discovery_res.discovered_headers

        # Step 2: Validate Schema
        validation_report = await self.mapping_validator.validate_mapping(
            profile_id=request.profile_id,
            spreadsheet_id=request.spreadsheet_id,
            worksheet_title=request.worksheet_title,
            discovered_headers=headers,
        )

        if validation_report.status == "MissingColumns" and not request.auto_apply_remapping:
            raise MappingValidationException(
                "Cannot synchronize: Mapped columns missing in Google Sheet.",
                report_details=validation_report.model_dump(),
            )

        now = datetime.now(UTC)
        # Step 3: Create SyncJob DB Record
        job = GoogleSyncJob(
            id=uuid.uuid4(),
            profile_id=request.profile_id,
            spreadsheet_id=request.spreadsheet_id,
            worksheet_id=request.worksheet_title,
            sync_mode=request.sync_mode,
            status="Running",
            total_rows=len(request.rows_data),
            processed_rows=0,
            success_rows=0,
            failed_rows=0,
            retry_count=0,
            max_retries=3,
            created_at=now,
        )
        self.db.add(job)
        await self.db.commit()

        try:
            # Map input dictionaries dynamically to header ordered 2D array
            rows_to_insert: list[list[Any]] = []
            for row in request.rows_data:
                formatted_row = []
                for header in headers:
                    val = row.get(header)
                    if val is None:
                        # Try case-insensitive lookup
                        for k, v in row.items():
                            if k.lower() == header.lower():
                                val = v
                                break
                    formatted_row.append(str(val) if val is not None else "")
                rows_to_insert.append(formatted_row)

            # Step 4: Perform Write to Google Sheets API
            if request.sync_mode in ("Batch", "Manual", "Realtime", "Scheduled"):
                res = await self.sheets_service.append_rows(
                    account_id=account_id,
                    spreadsheet_id=request.spreadsheet_id,
                    worksheet_title=request.worksheet_title,
                    values=rows_to_insert,
                )

            # Step 5: Update Job Outcome
            job.status = "Completed"
            job.processed_rows = len(request.rows_data)
            job.success_rows = len(request.rows_data)
            job.failed_rows = 0

            duration_ms = int((time.perf_counter() - start_time) * 1000)

            # Record Sync History Log
            history = GoogleSyncHistory(
                id=uuid.uuid4(),
                job_id=job.id,
                user_id=user_id,
                spreadsheet_id=request.spreadsheet_id,
                worksheet_id=request.worksheet_title,
                rows_processed=len(request.rows_data),
                duration_ms=duration_ms,
                retries=0,
                status="Success",
                error_message=None,
                validation_result=validation_report.model_dump(),
                created_at=now,
            )
            self.db.add(history)
            await self.db.commit()

        except Exception as exc:
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            job.status = "Failed"
            job.failed_rows = len(request.rows_data)

            history = GoogleSyncHistory(
                id=uuid.uuid4(),
                job_id=job.id,
                user_id=user_id,
                spreadsheet_id=request.spreadsheet_id,
                worksheet_id=request.worksheet_title,
                rows_processed=0,
                duration_ms=duration_ms,
                retries=0,
                status="Failed",
                error_message=str(exc),
                validation_result=validation_report.model_dump(),
                created_at=now,
            )
            self.db.add(history)
            await self.db.commit()
            raise exc

        return SyncJobSchema.model_validate(job)
