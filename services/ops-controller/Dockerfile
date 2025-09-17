# Dockerfile for InfoTerminal Ops Controller Service
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for Docker client and security operations
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (needed for Docker operations)
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY services/ops-controller/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared libraries first (for better caching)
COPY services/_shared/ /app/_shared/

# Copy service files
COPY services/ops-controller/ .

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Set Python path to include shared modules
ENV PYTHONPATH="/app:$PYTHONPATH"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app:APP", "--host", "0.0.0.0", "--port", "8000", "--reload"]
