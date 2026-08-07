from enum import StrEnum


class ConnectorType(StrEnum):
    """Supported third-party integration connectors."""

    GOOGLE_SHEETS = "Google Sheets"
    EXCEL = "Excel"
    CSV = "CSV"
    REST_API = "REST API"
    WEBHOOK = "Webhook"
    AIRTABLE = "Airtable"
    HUBSPOT = "HubSpot"
    ZOHO_CRM = "Zoho CRM"
    SALESFORCE = "Salesforce"
    NOTION = "Notion"


class SyncMode(StrEnum):
    """Synchronization modes configurations."""

    REALTIME = "Realtime"
    MANUAL = "Manual"
    SCHEDULED = "Scheduled"
    BATCH = "Batch"
    RETRY = "Retry"


class SyncJobStatus(StrEnum):
    """Synchronization queue processing states."""

    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    RETRYING = "Retrying"
