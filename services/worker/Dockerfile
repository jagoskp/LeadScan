FROM python:3.14-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./
COPY packages/ /packages/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main

FROM python:3.14-slim AS runner

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY services/worker/ /app/services/worker/
COPY packages/ /app/packages/

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "services.worker.main"]
