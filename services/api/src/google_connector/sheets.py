import asyncio
import logging
from typing import Any, Callable, Coroutine, TypeVar, cast
import uuid

import httpx

from services.api.src.google_connector.exceptions import (
    GooglePermissionDeniedException,
    GoogleRateLimitException,
    SpreadsheetNotFoundException,
    WorksheetNotFoundException,
)
from services.api.src.google_connector.interfaces import ISheetsService
from services.api.src.google_connector.oauth import GoogleOAuthService

logger = logging.getLogger(__name__)

GOOGLE_SHEETS_BASE_URL = "https://sheets.googleapis.com/v4/spreadsheets"

T = TypeVar("T")


class GoogleSheetsService(ISheetsService):
    """Production client for interacting with Google Sheets API v4 with retry & backoff."""

    def __init__(self, oauth_service: GoogleOAuthService):
        self.oauth_service = oauth_service

    async def _execute_with_retry(
        self, func: Callable[[], Coroutine[Any, Any, T]], max_retries: int = 3, base_delay: float = 1.0
    ) -> T:
        attempt = 0
        while True:
            try:
                return await func()
            except GoogleRateLimitException as e:
                attempt += 1
                if attempt > max_retries:
                    raise e
                delay = base_delay * (2 ** (attempt - 1))
                logger.warning(f"Rate limit hit. Retrying attempt {attempt}/{max_retries} in {delay}s...")
                await asyncio.sleep(delay)
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                if status in (429, 503):
                    attempt += 1
                    if attempt > max_retries:
                        raise GoogleRateLimitException(f"Google API error ({status}): {exc.response.text}")
                    delay = base_delay * (2 ** (attempt - 1))
                    await asyncio.sleep(delay)
                elif status == 404:
                    raise SpreadsheetNotFoundException("Resource not found")
                elif status in (401, 403):
                    raise GooglePermissionDeniedException(f"Permission denied: {exc.response.text}")
                else:
                    raise exc

    async def get_spreadsheet_metadata(self, account_id: uuid.UUID, spreadsheet_id: str) -> dict[str, Any]:
        """Fetch metadata including title and list of worksheets."""
        access_token = await self.oauth_service.get_valid_access_token(account_id)

        if access_token.startswith("mock_"):
            return {
                "spreadsheetId": spreadsheet_id,
                "properties": {"title": "Mock Enterprise Spreadsheet"},
                "sheets": [
                    {
                        "properties": {
                            "sheetId": 0,
                            "title": "Sheet1",
                            "index": 0,
                            "gridProperties": {"rowCount": 1000, "columnCount": 26},
                        }
                    },
                    {
                        "properties": {
                            "sheetId": 1,
                            "title": "Leads",
                            "index": 1,
                            "gridProperties": {"rowCount": 5000, "columnCount": 30},
                        }
                    },
                ],
            }

        async def _call() -> dict[str, Any]:
            async with httpx.AsyncClient() as client:
                url = f"{GOOGLE_SHEETS_BASE_URL}/{spreadsheet_id}"
                resp = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
                resp.raise_for_status()
                return cast(dict[str, Any], resp.json())

        return await self._execute_with_retry(_call)

    async def get_worksheet_headers(self, account_id: uuid.UUID, spreadsheet_id: str, worksheet_title: str) -> list[str]:
        """Fetch header row (Row 1) of specified worksheet."""
        access_token = await self.oauth_service.get_valid_access_token(account_id)

        if access_token.startswith("mock_"):
            # Return realistic default headers for mock environment
            if worksheet_title == "Leads":
                return ["Business Name", "Email", "Phone Number", "Contact Person", "Status", "Notes"]
            return ["Column A", "Column B", "Column C"]

        range_name = f"'{worksheet_title}'!1:1"

        async def _call() -> list[str]:
            async with httpx.AsyncClient() as client:
                url = f"{GOOGLE_SHEETS_BASE_URL}/{spreadsheet_id}/values/{range_name}"
                resp = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
                resp.raise_for_status()
                data = resp.json()
                values = data.get("values", [])
                if not values or not values[0]:
                    return []
                return [str(col).strip() for col in values[0]]

        return await self._execute_with_retry(_call)

    async def append_rows(
        self, account_id: uuid.UUID, spreadsheet_id: str, worksheet_title: str, values: list[list[Any]]
    ) -> dict[str, Any]:
        """Append rows to specified worksheet."""
        access_token = await self.oauth_service.get_valid_access_token(account_id)

        if access_token.startswith("mock_"):
            return {
                "spreadsheetId": spreadsheet_id,
                "tableRange": f"'{worksheet_title}'!A1:F1",
                "updates": {
                    "updatedRange": f"'{worksheet_title}'!A2:F{len(values) + 1}",
                    "updatedRows": len(values),
                    "updatedColumns": len(values[0]) if values else 0,
                    "updatedCells": len(values) * (len(values[0]) if values else 0),
                },
            }

        range_name = f"'{worksheet_title}'!A1"

        async def _call() -> dict[str, Any]:
            async with httpx.AsyncClient() as client:
                url = (
                    f"{GOOGLE_SHEETS_BASE_URL}/{spreadsheet_id}/values/{range_name}:append?"
                    f"valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS"
                )
                payload = {"values": values}
                resp = await client.post(
                    url,
                    json=payload,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                resp.raise_for_status()
                return cast(dict[str, Any], resp.json())

        return await self._execute_with_retry(_call)

    async def update_rows(
        self, account_id: uuid.UUID, spreadsheet_id: str, range_name: str, values: list[list[Any]]
    ) -> dict[str, Any]:
        """Update specific cell ranges in sheet."""
        access_token = await self.oauth_service.get_valid_access_token(account_id)

        if access_token.startswith("mock_"):
            return {
                "spreadsheetId": spreadsheet_id,
                "updatedRange": range_name,
                "updatedRows": len(values),
                "updatedCells": len(values) * (len(values[0]) if values else 0),
            }

        async def _call() -> dict[str, Any]:
            async with httpx.AsyncClient() as client:
                url = f"{GOOGLE_SHEETS_BASE_URL}/{spreadsheet_id}/values/{range_name}?valueInputOption=USER_ENTERED"
                payload = {"values": values}
                resp = await client.put(
                    url,
                    json=payload,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                resp.raise_for_status()
                return cast(dict[str, Any], resp.json())

        return await self._execute_with_retry(_call)
