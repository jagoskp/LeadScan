from enum import Enum


class LeadStatusEnum(str, Enum):
    NEW = "New"
    CONTACTED = "Contacted"
    QUALIFIED = "Qualified"
    INTERESTED = "Interested"
    PROPOSAL = "Proposal"
    WON = "Won"
    LOST = "Lost"
    ARCHIVED = "Archived"


class LeadPriorityEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"


class TimelineEventTypeEnum(str, Enum):
    CREATED = "Created"
    UPDATED = "Updated"
    SCANNED = "Scanned"
    REVIEWED = "Reviewed"
    SYNCED = "Synced"
    EDITED = "Edited"
    MERGED = "Merged"
    ARCHIVED = "Archived"
    RESTORED = "Restored"


class LeadSourceEnum(str, Enum):
    CAMERA = "Camera Scan"
    DOCUMENT = "Document Upload"
    BULK_IMPORT = "Bulk Import"
    MANUAL = "Manual Entry"
    API = "API Integration"
