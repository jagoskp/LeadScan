from abc import ABC, abstractmethod
from typing import Any

from services.api.src.dashboard.schemas import (
    AnalyticsResponse,
    CommandCenterTelemetryResponse,
    ReportCreateSchema,
    ReportSchema,
    SystemHealthItem,
)


class IAnalyticsEngine(ABC):

    @abstractmethod
    async def compute_analytics(self) -> AnalyticsResponse:
        pass


class IHealthMonitor(ABC):

    @abstractmethod
    async def get_system_health(self) -> list[SystemHealthItem]:
        pass


class IReportGenerator(ABC):

    @abstractmethod
    async def generate_report(self, req: ReportCreateSchema) -> ReportSchema:
        pass
