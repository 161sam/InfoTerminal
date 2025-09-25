FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY ./services/verification/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm || echo "spaCy model download failed, will use fallback"

# Copy shared libraries first (for better caching)
COPY ./services/_shared/ /app/_shared/
COPY ./services/common/ /app/common/

# Copy application code
COPY ./services/verification/ .

# Set Python path to include shared modules
ENV PYTHONPATH="/app:$PYTHONPATH"

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8617

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -fsS http://localhost:8617/healthz || exit 1

# Start the service with uvicorn
CMD ["uvicorn", "app_v1:app", "--host", "0.0.0.0", "--port", "8617"]
