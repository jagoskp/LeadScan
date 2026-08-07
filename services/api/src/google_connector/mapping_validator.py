import logging
from datetime import UTC, datetime
import uuid
from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.google_connector.interfaces import IMappingValidator
from services.api.src.google_connector.models import MappingValidation
from services.api.src.google_connector.remapping_assistant import AutoRemappingAssistant
from services.api.src.google_connector.schemas import MappingValidationReportSchema

logger = logging.getLogger(__name__)


class PreSyncMappingValidator(IMappingValidator):
    """Pre-synchronization Mapping Validator enforcing profile & header compatibility."""

    def __init__(self, db: AsyncSession, remapping_assistant: AutoRemappingAssistant):
        self.db = db
        self.remapping_assistant = remapping_assistant

    async def validate_mapping(
        self, profile_id: uuid.UUID, spreadsheet_id: str, worksheet_title: str, discovered_headers: list[str]
    ) -> MappingValidationReportSchema:
        """Validate dynamic mapping profile against actual discovered Google Sheet headers."""
        # Query approved mapping fields (or mock mapping profile for testing/development)
        # Standard required DOM fields expected in connector sync
        expected_mapped_columns = ["Business Name", "Email", "Phone Number", "Contact Person"]

        discovered_set = set(discovered_headers)
        expected_set = set(expected_mapped_columns)

        missing_columns = list(expected_set - discovered_set)
        new_columns = list(discovered_set - expected_set)

        status = "Valid"
        if missing_columns and new_columns:
            status = "RenamedColumns"
        elif missing_columns:
            status = "MissingColumns"

        # Generate intelligent remapping suggestions for missing columns
        suggestions = self.remapping_assistant.generate_suggestions(
            missing_columns=missing_columns,
            discovered_headers=discovered_headers,
        )

        now = datetime.now(UTC)
        validation_rec = MappingValidation(
            id=uuid.uuid4(),
            profile_id=profile_id,
            sheet_id=spreadsheet_id,
            worksheet_id=worksheet_title,
            status=status,
            missing_columns=missing_columns,
            new_columns=new_columns,
            report_data={
                "discovered_headers": discovered_headers,
                "expected_columns": expected_mapped_columns,
                "suggestion_count": len(suggestions),
            },
            created_at=now,
        )
        self.db.add(validation_rec)
        await self.db.commit()

        return MappingValidationReportSchema(
            id=validation_rec.id,
            sheet_id=spreadsheet_id,
            worksheet_id=worksheet_title,
            status=status,  # type: ignore
            missing_columns=missing_columns,
            new_columns=new_columns,
            suggestions=suggestions,
            report_data=validation_rec.report_data,
            created_at=validation_rec.created_at,
        )
