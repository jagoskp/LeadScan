class WorkflowException(Exception):
    """Base exception for Enterprise Workflow & Automation Engine errors."""

    def __init__(self, message: str, code: str = "WORKFLOW_ERROR", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class TaskNotFoundException(WorkflowException):
    """Raised when a task item is not found."""

    def __init__(self, task_id: str):
        super().__init__(f"Task '{task_id}' not found", code="TASK_NOT_FOUND", status_code=404)


class WorkflowNotFoundException(WorkflowException):
    """Raised when a workflow definition is not found."""

    def __init__(self, workflow_id: str):
        super().__init__(f"Workflow '{workflow_id}' not found", code="WORKFLOW_NOT_FOUND", status_code=404)


class SLABreachException(WorkflowException):
    """Raised when SLA target has breached."""

    def __init__(self, detail: str):
        super().__init__(f"SLA Breach: {detail}", code="SLA_BREACH", status_code=422)
