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
COPY ./services/egress-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared libraries and service code
COPY ./services/_shared/ /app/_shared/
COPY ./services/common/ /app/common/
COPY ./services/egress-gateway/ /app/

# Create tor data directory with proper permissions
RUN mkdir -p /var/lib/tor && \
    chown -R debian-tor:debian-tor /var/lib/tor && \
    chmod 700 /var/lib/tor

# Copy Tor configuration
COPY ./services/egress-gateway/config/tor.conf /etc/tor/torrc

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

# Start the compatibility app; health endpoints now answer 200 with deprecation headers
CMD ["python", "app.py"]
