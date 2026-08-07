import logging
from datetime import UTC, datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.dashboard.interfaces import IReportGenerator
from services.api.src.dashboard.models import ReportDefinition
from services.api.src.dashboard.schemas import ReportCreateSchema, ReportSchema

logger = logging.getLogger(__name__)


class ReportGenerator(IReportGenerator):
    """Report Generator producing custom saved analytical report definitions."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_report(self, req: ReportCreateSchema) -> ReportSchema:
        report = ReportDefinition(
            id=uuid.uuid4(),
            name=req.name,
            report_type=req.report_type,
            date_range=req.date_range,
            filters=req.filters,
            created_at=datetime.now(UTC),
        )
        self.db.add(report)
        await self.db.commit()
        return ReportSchema.model_validate(report)
