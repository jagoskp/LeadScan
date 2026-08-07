from abc import ABC, abstractmethod
from typing import Any


class ITaskHandler(ABC):
    """Abstract Base Class interface contract that all task handlers must implement."""

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Run the core asynchronous background task logic."""
        pass
