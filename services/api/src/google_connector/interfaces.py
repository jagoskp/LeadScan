from abc import ABC, abstractmethod
from typing import Any
import uuid

from services.api.src.google_connector.schemas import (
    ColumnDiscoveryResponse,
    MappingValidationReportSchema,
    OAuthAuthUrlResponse,
    RemappingSuggestionSchema,
)


class IOAuthService(ABC):
    """Abstract interface for Google OAuth authentication and token lifecycle."""

    @abstractmethod
    async def get_authorization_url(self, user_id: uuid.UUID) -> OAuthAuthUrlResponse:
        pass

    @abstractmethod
    async def handle_oauth_callback(
        self, user_id: uuid.UUID, code: str, redirect_uri: str | None = None
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def get_valid_access_token(self, account_id: uuid.UUID) -> str:
        pass

    @abstractmethod
    async def disconnect_account(self, account_id: uuid.UUID) -> bool:
        pass


class ISheetsService(ABC):
    """Abstract interface for Google Sheets API communication."""

    @abstractmethod
    async def get_spreadsheet_metadata(self, account_id: uuid.UUID, spreadsheet_id: str) -> dict[str, Any]:
        pass

    @abstractmethod
    async def get_worksheet_headers(self, account_id: uuid.UUID, spreadsheet_id: str, worksheet_title: str) -> list[str]:
        pass

    @abstractmethod
    async def append_rows(
        self, account_id: uuid.UUID, spreadsheet_id: str, worksheet_title: str, values: list[list[Any]]
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def update_rows(
        self, account_id: uuid.UUID, spreadsheet_id: str, range_name: str, values: list[list[Any]]
    ) -> dict[str, Any]:
        pass


class IColumnDiscoveryService(ABC):
    """Abstract interface for discovering Google Sheets column headers."""

    @abstractmethod
    async def discover_columns(
        self, account_id: uuid.UUID, spreadsheet_id: str, worksheet_title: str, force_refresh: bool = False
    ) -> ColumnDiscoveryResponse:
        pass


class IMappingValidator(ABC):
    """Abstract interface for pre-sync schema comparison against approved mapping profiles."""

    @abstractmethod
    async def validate_mapping(
        self, profile_id: uuid.UUID, spreadsheet_id: str, worksheet_title: str, discovered_headers: list[str]
    ) -> MappingValidationReportSchema:
        pass


class IRemappingAssistant(ABC):
    """Abstract interface for intelligent column remapping suggestions."""

    @abstractmethod
    def generate_suggestions(
        self, missing_columns: list[str], discovered_headers: list[str]
    ) -> list[RemappingSuggestionSchema]:
        pass
