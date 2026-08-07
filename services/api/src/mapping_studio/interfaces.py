import uuid
from abc import ABC, abstractmethod
from typing import Any


class IRuleBuilder(ABC):
    """Interface parsing logical criteria (IF/ELSE, Starts With, Regex)."""

    @abstractmethod
    async def parse_rule(self, condition_json: dict[str, Any]) -> bool:
        """Evaluate if input conditions resolve to True/False."""
        pass


class IPreviewEngine(ABC):
    """Interface coordinating intermediate previews for mapping visual studios."""

    @abstractmethod
    async def generate_preview(
        self, document_id: uuid.UUID, profile_id: uuid.UUID
    ) -> dict[str, Any]:
        """Fetch live DOM attributes, apply rules, and summarize outcomes."""
        pass


class IProfileManager(ABC):
    """Interface handling profile duplications, exports, and favorites."""

    @abstractmethod
    async def duplicate_profile(self, profile_id: uuid.UUID) -> uuid.UUID:
        """Create a duplicate instance of a target profile."""
        pass

    @abstractmethod
    async def export_profile(self, profile_id: uuid.UUID) -> dict[str, Any]:
        """Export mapping profile rules into a portable JSON structure."""
        pass

    @abstractmethod
    async def import_profile(self, profile_json: dict[str, Any]) -> uuid.UUID:
        """Import a portable JSON profile configuration and save to DB."""
        pass

    @abstractmethod
    async def toggle_favorite(self, profile_id: uuid.UUID) -> bool:
        """Toggle favorite status flag of a profile."""
        pass
