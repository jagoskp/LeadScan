from services.api.src.workflow.exceptions import WorkflowException

VALID_PRIORITIES = {"High", "Medium", "Low"}
VALID_STATUSES = {"Pending", "In Progress", "Completed", "Cancelled"}


def validate_task_priority(priority: str) -> str:
    if priority not in VALID_PRIORITIES:
        raise WorkflowException(f"Invalid task priority '{priority}'. Must be one of {VALID_PRIORITIES}")
    return priority
