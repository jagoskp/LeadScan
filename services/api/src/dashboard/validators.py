from services.api.src.dashboard.exceptions import DashboardException

VALID_DASHBOARD_TYPES = {"executive", "operations", "lead", "workflow", "google_sheets", "search", "asset", "identity", "system"}


def validate_dashboard_type(dashboard_type: str) -> str:
    if dashboard_type not in VALID_DASHBOARD_TYPES:
        raise DashboardException(f"Invalid dashboard type '{dashboard_type}'. Must be one of {VALID_DASHBOARD_TYPES}")
    return dashboard_type
