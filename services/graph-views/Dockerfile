# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System libs (PDF export via WeasyPrint) and curl for health
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi8 \
    shared-mime-info \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies (split for better caching)
COPY services/graph-views/requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip \
 && python -m pip install --no-cache-dir -r /tmp/requirements.txt \
 && python -m pip install --no-cache-dir neo4j

# Copy code & install package
COPY services/graph-views/ /app/
RUN python -m pip install --no-cache-dir .

# Non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Standardize container port (8000)
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=10s --timeout=3s --retries=30 CMD \
  curl -fsS http://localhost:8000/readyz || curl -fsS http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
