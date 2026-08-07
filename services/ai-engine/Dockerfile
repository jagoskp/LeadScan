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

COPY services/ai-engine/ /app/services/ai-engine/
COPY packages/ /app/packages/

ENV PYTHONUNBUFFERED=1
ENV PORT=8001

EXPOSE 8001

CMD ["uvicorn", "services.ai-engine.main:app", "--host", "0.0.0.0", "--port", "8001"]
