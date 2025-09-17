FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY app.py .
COPY registry.py .

# Copy shared modules if available
COPY ../../services/_shared /app/_shared 2>/dev/null || true
COPY ../../services/common /app/common 2>/dev/null || true

# Create directories
RUN mkdir -p /app/plugins /app/results

# Copy plugins directory
COPY ../../plugins /app/plugins 2>/dev/null || true

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
