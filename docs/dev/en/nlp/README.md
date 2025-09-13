# NLP Service

Provides basic NLP features for documents.

## Endpoints
- `POST /ner` — spaCy NER with models selected via environment variables.
- `POST /summary` — text summarization; uses transformers when `NLP_BACKEND=transformers` otherwise a simple heuristic.
- `POST /relations` — placeholder relation extraction returning an empty list.

## Environment
- `NLP_DEFAULT_LANG` (default `en`)
- `NLP_SPACY_MODEL_EN`, `NLP_SPACY_MODEL_DE`
- `NLP_BACKEND` (`spacy` or `transformers`)
