# NLP Service

FastAPI microservice providing Named Entity Recognition and text summarization.

## Endpoints
- `POST /ner` – extract entities using spaCy.
- `POST /summarize` – summarize text with a HuggingFace Transformers pipeline.
- `GET /healthz` – health check.

## Development
```
uvicorn app:app --host 0.0.0.0 --port 8003
```

## Docker
```
docker build -t nlp-service .
docker run -p 8003:8003 nlp-service
```

## Usage
```
curl -X POST localhost:8003/ner -H 'Content-Type: application/json' -d '{"text": "Barack Obama was born in Hawaii."}'
curl -X POST localhost:8003/summarize \
  -H 'Content-Type: application/json' \
  -d '{"text": "Text summarization condenses information."}'
```
