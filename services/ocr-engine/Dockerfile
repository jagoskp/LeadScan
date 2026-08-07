FROM python:3.14-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./
COPY packages/ /packages/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main

FROM python:3.14-slim AS runner

WORKDIR /app

# Install runtime dependencies for OCR (Tesseract engine binaries and libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY services/ocr-engine/ /app/services/ocr-engine/
COPY packages/ /app/packages/

ENV PYTHONUNBUFFERED=1
ENV PORT=8002

EXPOSE 8002

CMD ["uvicorn", "services.ocr-engine.main:app", "--host", "0.0.0.0", "--port", "8002"]
