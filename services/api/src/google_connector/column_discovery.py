import logging
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.google_connector.interfaces import IColumnDiscoveryService
from services.api.src.google_connector.models import (
    Spreadsheet,
    SpreadsheetColumn,
    Worksheet,
)
from services.api.src.google_connector.schemas import (
    ColumnDiscoveryResponse,
    SpreadsheetColumnSchema,
)
from services.api.src.google_connector.sheets import GoogleSheetsService

logger = logging.getLogger(__name__)


class ColumnDiscoveryService(IColumnDiscoveryService):
    """Dynamic Header Discovery Engine with database caching & drift tracking."""

    def __init__(self, db: AsyncSession, sheets_service: GoogleSheetsService):
        self.db = db
        self.sheets_service = sheets_service

    async def discover_columns(
        self, account_id: uuid.UUID, spreadsheet_id: str, worksheet_title: str, force_refresh: bool = False
    ) -> ColumnDiscoveryResponse:
        """Fetch headers from Google Sheets API and synchronize DB column records."""
        # Query DB worksheet record
        ws_stmt = (
            select(Worksheet)
            .join(Spreadsheet)
            .where(
                Spreadsheet.spreadsheet_id == spreadsheet_id,
                Worksheet.title == worksheet_title,
            )
        )
        result = await self.db.execute(ws_stmt)
        worksheet = result.scalars().first()

        # Fetch live headers from Google Sheets API
        headers = await self.sheets_service.get_worksheet_headers(
            account_id=account_id,
            spreadsheet_id=spreadsheet_id,
            worksheet_title=worksheet_title,
        )

        column_schemas: list[SpreadsheetColumnSchema] = []

        if worksheet:
            # Sync discovered columns to DB
            existing_cols_stmt = select(SpreadsheetColumn).where(
                SpreadsheetColumn.worksheet_id == worksheet.id
            )
            col_res = await self.db.execute(existing_cols_stmt)
            existing_cols = {col.name: col for col in col_res.scalars().all()}

            for idx, header_name in enumerate(headers):
                if header_name in existing_cols:
                    col_obj = existing_cols[header_name]
                    col_obj.index = idx
                else:
                    col_obj = SpreadsheetColumn(
                        id=uuid.uuid4(),
                        worksheet_id=worksheet.id,
                        name=header_name,
                        index=idx,
                        data_type="String",
                        is_hidden=False,
                        is_custom=False,
                    )
                    self.db.add(col_obj)
                
                column_schemas.append(
                    SpreadsheetColumnSchema(
                        id=col_obj.id,
                        worksheet_id=worksheet.id,
                        name=header_name,
                        index=idx,
                        data_type=col_obj.data_type,
                        is_hidden=col_obj.is_hidden,
                        is_custom=col_obj.is_custom,
                    )
                )

            await self.db.commit()

        else:
            # Transmit ephemeral column schemas if worksheet not saved in DB yet
            dummy_ws_id = uuid.uuid4()
            for idx, header_name in enumerate(headers):
                column_schemas.append(
                    SpreadsheetColumnSchema(
                        id=uuid.uuid4(),
                        worksheet_id=dummy_ws_id,
                        name=header_name,
                        index=idx,
                        data_type="String",
                        is_hidden=False,
                        is_custom=False,
                    )
                )

        return ColumnDiscoveryResponse(
            spreadsheet_id=spreadsheet_id,
            worksheet_title=worksheet_title,
            discovered_headers=headers,
            column_details=column_schemas,
            is_cache_hit=False,
        )
