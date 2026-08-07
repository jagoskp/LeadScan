import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any


class IOCRPipeline(ABC):
    """Interface orchestrating document ingestion down to the Scanner."""

    @abstractmethod
    async def execute_ocr(self, job_id: uuid.UUID) -> Any:
        """Run preprocessing, provider execution, layout parsing, and dispatch."""
        pass


class IOCRProvider(ABC):
    """Interface specifying standard third-party engine stubs."""

    @abstractmethod
    async def extract_text(
        self, image_data: bytes, languages: Sequence[str]
    ) -> dict[str, Any]:
        """Perform text detection and return coordinate mappings."""
        pass


class IImagePreprocessor(ABC):
    """Interface defining image modifications prior to character execution."""

    @abstractmethod
    async def preprocess(
        self, image_data: bytes, operations: Sequence[str]
    ) -> bytes:
        """Apply filters (resize, denoise, deskew) and return modified bytes."""
        pass


class ILayoutDetector(ABC):
    """Interface handling layout hierarchy construction."""

    @abstractmethod
    async def detect_layout(
        self, raw_ocr_data: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Organize OCR detections into structured block, line, and word nodes."""
        pass
