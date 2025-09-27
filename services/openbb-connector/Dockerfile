FROM python:3.11-slim
WORKDIR /app
COPY services/openbb-connector/pyproject.toml /app/
RUN pip install -q --no-cache-dir uv && \
    uv pip install --system pandas requests psycopg2-binary yfinance python-dotenv
COPY services/openbb-connector/main.py /app/
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
CMD ["python","/app/main.py"]
