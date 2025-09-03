FROM python:3.11-slim
WORKDIR /app
# curl für Healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
# Abhängigkeiten
COPY pyproject.toml /app/
RUN pip install --no-cache-dir fastapi uvicorn httpx prometheus-client \
    opentelemetry-sdk opentelemetry-instrumentation-fastapi opentelemetry-exporter-otlp
# App
COPY app /app/app
EXPOSE 8080
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]

