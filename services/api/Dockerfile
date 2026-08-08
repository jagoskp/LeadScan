# Multi-stage production Dockerfile for LeadScan API

FROM python:3.14-slim AS builder

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

# Keep the API project in its real repository location
COPY services/api/pyproject.toml services/api/poetry.lock ./services/api/

# Local workspace dependencies
COPY packages/ ./packages/

WORKDIR /app/services/api

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main


FROM python:3.14-slim AS runner

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Application
COPY services/ ./services/
COPY packages/ ./packages/

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]