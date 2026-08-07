import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import UTC, datetime

from services.api.src.dashboard.analytics import AnalyticsEngine
from services.api.src.dashboard.health import SystemHealthMonitor
from services.api.src.dashboard.reports import ReportGenerator
from services.api.src.dashboard.schemas import ReportCreateSchema
from services.api.src.dashboard.service import DashboardService
from services.api.src.dashboard.validators import validate_dashboard_type


def test_dashboard_type_validator():
    assert validate_dashboard_type("executive") == "executive"
    assert validate_dashboard_type("operations") == "operations"
    with pytest.raises(Exception):
        validate_dashboard_type("INVALID_TYPE")


@pytest.fixture
def mock_db():
    db = AsyncMock()
    now = datetime.now(UTC)

    async def mock_execute(stmt, *args, **kwargs):
        res = MagicMock()
        res.scalar.return_value = 100
        res.scalars.return_value.all.return_value = []
        return res

    db.execute.side_effect = mock_execute
    return db


@pytest.mark.asyncio
async def test_dashboard_telemetry_and_health(mock_db):
    service = DashboardService(mock_db)
    telemetry = await service.get_telemetry()

    assert telemetry.todays_scans == 142
    assert len(telemetry.kpi_cards) > 0
    assert len(telemetry.system_health) > 0


@pytest.mark.asyncio
async def test_analytics_and_report_generator(mock_db):
    service = DashboardService(mock_db)

    analytics = await service.get_analytics()
    assert analytics.conversion_rate == 80.0
    assert len(analytics.funnel) > 0

    req = ReportCreateSchema(name="Daily Conversion Summary", report_type="lead_summary", date_range="daily")
    report = await service.create_report(req)
    assert report.name == "Daily Conversion Summary"
