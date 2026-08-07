import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any


class IMappingEngine(ABC):
    """Interface orchestrating DOM data mapping to target system configurations."""

    @abstractmethod
    async def execute_mapping(
        self, document_id: uuid.UUID, profile_id: uuid.UUID
    ) -> dict[str, Any]:
        """Convert document DOM nodes into custom target outputs."""
        pass


class ITransformer(ABC):
    """Interface declaring data transformation utilities."""

    @abstractmethod
    async def transform(
        self, value: str, rules: Sequence[dict[str, Any]]
    ) -> str:
        """Apply formatting manipulations to a target string."""
        pass


class IMappingValidator(ABC):
    """Interface executing validation constraints on mapped field values."""

    @abstractmethod
    async def validate_field(
        self, value: str, rules: Sequence[dict[str, Any]]
    ) -> list[str]:
        """Evaluate checks and report error log messages."""
        pass
