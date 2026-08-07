class DashboardException(Exception):
    """Base exception for Enterprise Command Center errors."""

    def __init__(self, message: str, code: str = "DASHBOARD_ERROR", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class WidgetNotFoundException(DashboardException):
    """Raised when a dashboard widget is not found."""

    def __init__(self, widget_id: str):
        super().__init__(f"Widget '{widget_id}' not found", code="WIDGET_NOT_FOUND", status_code=404)


class ReportGenerationException(DashboardException):
    """Raised when custom report execution fails."""

    def __init__(self, detail: str):
        super().__init__(f"Report generation error: {detail}", code="REPORT_GENERATION_FAILED", status_code=422)
