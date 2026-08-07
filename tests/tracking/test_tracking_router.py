import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from services.api.main import app
from services.api.src.tracking.router import get_tracking_service

client = TestClient(app)


def test_admin_dashboard_public_endpoint():
    mock_service = AsyncMock()
    mock_service.get_admin_dashboard.return_value = {
        "online_users_count": 5,
        "total_registered_users": 120,
        "total_registered_devices": 145,
        "subscriptions_breakdown": {"FREE": 80, "PRO": 35, "ENTERPRISE": 5},
        "usage_totals": {
            "total_app_opens": 1500,
            "total_login_count": 420,
            "total_scan_count": 890,
            "total_leads_created": 610,
            "total_backup_count": 130,
            "total_sheets_sync_count": 550,
        },
        "last_active_users": [
            {
                "user_id": "00000000-0000-0000-0000-000000000001",
                "email": "user1@leadscan.ai",
                "display_name": "User One",
                "last_active_at": "2026-08-06T15:00:00Z",
                "registered_devices_count": 2,
                "subscription_tier": "PRO",
            }
        ],
    }

    app.dependency_overrides[get_tracking_service] = lambda: mock_service

    try:
        response = client.get("/tracking/admin/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert data["online_users_count"] == 5
        assert data["total_registered_users"] == 120
        assert data["total_registered_devices"] == 145
        assert "usage_totals" in data
        assert len(data["last_active_users"]) == 1
    finally:
        app.dependency_overrides.clear()
