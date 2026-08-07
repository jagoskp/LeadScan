import json
import logging
from contextvars import ContextVar

# Context variables storing tracing data across async request boundaries
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")
correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id", default="")
trace_id_ctx: ContextVar[str] = ContextVar("trace_id", default="")


class StructuredJSONFormatter(logging.Formatter):
    """Logging formatter converting LogRecords into structured JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id_ctx.get(),
            "correlation_id": correlation_id_ctx.get(),
            "trace_id": trace_id_ctx.get(),
        }

        # Include traceback strings if exception occurred
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_payload)


def setup_json_logging(log_level: str = "INFO") -> None:
    """Centralize and apply structured JSON logging across the app."""
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove pre-existing standard console handlers
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StructuredJSONFormatter())
    root_logger.addHandler(console_handler)
