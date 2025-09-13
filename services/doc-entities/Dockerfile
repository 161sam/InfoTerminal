FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV IT_ENABLE_METRICS=0
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
