FROM python:3.11-slim

# Install system dependencies for Tor and networking
RUN apt-get update && apt-get install -y \
    tor \
    curl \
    netcat-openbsd \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create tor data directory with proper permissions
RUN mkdir -p /var/lib/tor && \
    chown -R debian-tor:debian-tor /var/lib/tor && \
    chmod 700 /var/lib/tor

# Copy Tor configuration
COPY config/tor.conf /etc/tor/torrc

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose ports
EXPOSE 8615

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -fsS http://localhost:8615/healthz || exit 1

# Start script that handles Tor and the app
CMD ["python", "app.py"]
