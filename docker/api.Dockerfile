# Stage 1: Dependency compilation builder
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || \
    pip install fastapi uvicorn sqlalchemy pydantic redis celery pydantic-settings

# Stage 2: Final runner runtime image
FROM python:3.12-slim AS runner

WORKDIR /app

# Copy virtual env dependencies from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Run as non-root user for security compliance
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

# Copy source directories
COPY . .
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# Native Python healthcheck avoiding curl/wget dependencies
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')" || exit 1

CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
