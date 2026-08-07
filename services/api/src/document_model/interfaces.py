import uuid
from abc import ABC, abstractmethod


class IDOMBuilder(ABC):
    """Interface orchestrating semantic AI results conversion into DOM models."""

    @abstractmethod
    async def build_dom(self, understanding_job_id: uuid.UUID) -> uuid.UUID:
        """Parse AI job results and write normalized DOM structures to database."""
        pass


class IDOMNormalizer(ABC):
    """Interface defining standard formatting patterns for core fields."""

    @abstractmethod
    async def normalize_phone(self, raw_value: str) -> str:
        """Standardize phone format details."""
        pass

    @abstractmethod
    async def normalize_email(self, raw_value: str) -> str:
        """Sanitize email string content."""
        pass

    @abstractmethod
    async def normalize_website(self, raw_value: str) -> str:
        """Verify and format website URL protocols."""
        pass

    @abstractmethod
    async def normalize_gst(self, raw_value: str) -> str:
        """Format GST tax identification number boundaries."""
        pass

    @abstractmethod
    async def normalize_pan(self, raw_value: str) -> str:
        """Format PAN taxation identification card strings."""
        pass

    @abstractmethod
    async def normalize_address(self, raw_value: str) -> str:
        """Refine street address notations."""
        pass

    @abstractmethod
    async def normalize_date(self, raw_value: str) -> str:
        """Resolve varying date formats into standard YYYY-MM-DD."""
        pass

    @abstractmethod
    async def normalize_currency(self, raw_value: str) -> str:
        """Convert currency strings to standard ISO notation."""
        pass


class IDOMValidator(ABC):
    """Interface validating structural consistency and values of a DOM."""

    @abstractmethod
    async def validate_dom(self, document_id: uuid.UUID) -> bool:
        """Scan document nodes asserting formats and relational loops."""
        pass
