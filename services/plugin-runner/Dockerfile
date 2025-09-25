FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY services/plugin-runner/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared modules and service code
COPY services/_shared/ /app/_shared/
COPY services/common/ /app/common/
COPY services/plugin-runner/ ./

# Create directories for runtime artifacts
RUN mkdir -p /app/plugins /app/results

# Copy bundled plugins
COPY plugins/ /app/plugins/

# Ensure shared modules are importable
ENV PYTHONPATH="/app:$PYTHONPATH"

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
