# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# kleine Basis
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Code & Metadaten
COPY services/graph-views/ /app/
RUN python -m pip install --upgrade pip \
 && python -m pip install --no-cache-dir . \
 && python -m pip install --no-cache-dir neo4j

# Non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8403

# Healthcheck
HEALTHCHECK --interval=10s --timeout=3s --retries=30 CMD \
  curl -fsS http://localhost:8403/readyz || curl -fsS http://localhost:8403/healthz || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8403"]

