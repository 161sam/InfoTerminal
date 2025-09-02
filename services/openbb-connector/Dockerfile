FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install -q --no-cache-dir uv && \
    uv pip install --system pandas requests psycopg2-binary yfinance python-dotenv
COPY main.py /app/
CMD ["python","/app/main.py"]
