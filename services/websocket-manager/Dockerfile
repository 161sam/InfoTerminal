FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential curl \
 && rm -rf /var/lib/apt/lists/*

COPY services/websocket-manager/requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip \
 && python -m pip install --no-cache-dir -r requirements.txt

COPY services/_shared/ /app/_shared/
COPY services/websocket-manager/ /app/

ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
