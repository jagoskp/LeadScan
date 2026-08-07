import uuid
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any


class Span:
    """Mock OpenTelemetry-ready Trace Span wrapper."""

    def __init__(self, name: str, trace_id: str, span_id: str) -> None:
        self.name = name
        self.trace_id = trace_id
        self.span_id = span_id
        self.attributes: dict[str, Any] = {}

    def set_attribute(self, key: str, value: Any) -> None:
        """Assign key/value attributes to the span context metadata."""
        self.attributes[key] = value

    def end(self) -> None:
        """Mark span execution as finished."""
        pass


class Tracer:
    """OpenTelemetry-ready Tracer implementation abstracting tracing backends."""

    def __init__(self, service_name: str) -> None:
        self.service_name = service_name

    @contextmanager
    def start_span(self, name: str) -> Generator[Span, None, None]:
        """Context manager creating and wrapping a new tracing span."""
        trace_id = generate_trace_id()
        span_id = generate_span_id()
        span = Span(name, trace_id, span_id)
        try:
            yield span
        finally:
            span.end()


def generate_trace_id() -> str:
    """Generate a mock standard trace identifier string."""
    return uuid.uuid4().hex


def generate_span_id() -> str:
    """Generate a mock standard span identifier string."""
    return uuid.uuid4().hex[16:]
