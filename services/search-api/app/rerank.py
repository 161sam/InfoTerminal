import hashlib
import logging
import threading
from typing import List, Tuple

import numpy as np
from cachetools import TTLCache

from .config import Settings

logger = logging.getLogger(__name__)
settings = Settings()

# caches
query_cache = TTLCache(maxsize=1024, ttl=settings.rerank_cache_ttl_s)
doc_cache = TTLCache(maxsize=4096, ttl=settings.rerank_cache_ttl_s)
cache_stats = {"q_hits": 0, "q_miss": 0, "d_hits": 0, "d_miss": 0}


def _hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


class EmbeddingProvider:
    """Lazy loading sentence-transformer provider (singleton)."""

    _lock = threading.Lock()
    _instance: "EmbeddingProvider | None" = None

    def __new__(cls, model_name: str):
        if cls._instance is None or cls._instance.model_name != model_name:
            with cls._lock:
                if cls._instance is None or cls._instance.model_name != model_name:  # pragma: no cover (race)
                    cls._instance = super().__new__(cls)
                    cls._instance.model_name = model_name
                    cls._instance._model = None
        return cls._instance

    def _load(self):
        if self._model is None:
            with self._lock:
                if self._model is None:  # pragma: no cover (double-check)
                    try:
                        from sentence_transformers import SentenceTransformer
                    except ImportError as e:  # pragma: no cover
                        raise RuntimeError("sentence-transformers not installed") from e
                    logger.info("loading embedding model %s", self.model_name)
                    self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed(self, texts: List[str]) -> np.ndarray:
        model = self._load()
        return np.asarray(
            model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        )


def embed_texts(provider: EmbeddingProvider, texts: List[str]) -> np.ndarray:
    return provider.embed(texts)


def get_query_embedding(provider: EmbeddingProvider, text: str) -> np.ndarray:
    key = "qe:" + _hash(text)
    vec = query_cache.get(key)
    if vec is None:
        vec = provider.embed([text])[0]
        query_cache[key] = vec
        cache_stats["q_miss"] += 1
    else:
        cache_stats["q_hits"] += 1
    return vec


def get_doc_embedding(provider: EmbeddingProvider, doc_id: str, text: str) -> np.ndarray:
    key = f"de:{doc_id}:{_hash(text)}"
    vec = doc_cache.get(key)
    if vec is None:
        vec = provider.embed([text])[0]
        doc_cache[key] = vec
        cache_stats["d_miss"] += 1
    else:
        cache_stats["d_hits"] += 1
    return vec


def cosine_rank(query_vec: np.ndarray, doc_vecs: np.ndarray) -> List[Tuple[int, float]]:
    if doc_vecs.size == 0:
        return []
    q = query_vec / (np.linalg.norm(query_vec) + 1e-9)
    docs = doc_vecs / (np.linalg.norm(doc_vecs, axis=1, keepdims=True) + 1e-9)
    scores = docs.dot(q)
    return sorted(list(enumerate(scores)), key=lambda x: x[1], reverse=True)


def normalize(scores: List[float]) -> List[float]:
    if not scores:
        return scores
    mn, mx = min(scores), max(scores)
    if mx - mn < 1e-9:
        return [0.0 for _ in scores]
    return [(s - mn) / (mx - mn) for s in scores]
