from typing import Dict, Any
from opensearchpy import OpenSearch, helpers
import hashlib
from typing import List


class OSClient:
    def __init__(self, url: str, index: str):
        self.index = index
        self.client = OpenSearch(hosts=[url], http_compress=True)
        self.use_knn = bool(int(os.getenv('OS_KNN', os.getenv('RAG_OS_KNN', '0'))))
        self._ensure_index()

    def ping(self) -> Dict[str, Any]:
        try:
            ok = self.client.ping()
            return {"status": "ok" if ok else "fail"}
        except Exception as e:
            return {"status": "fail", "error": str(e)}

    def _ensure_index(self):
        if not self.client.indices.exists(self.index):
            body = {
                "settings": {"index": {"number_of_shards": 1}},
                "mappings": {
                    "properties": {
                        "id": {"type": "keyword"},
                        "title": {"type": "text"},
                        "paragraph": {"type": "text"},
                        "text": {"type": "text"},
                        "domain": {"type": "keyword"},
                        "source": {"type": "keyword"},
                        "effective_date": {"type": "date", "ignore_malformed": True},
                        "vector": self._vector_mapping()
                    }
                },
            }
            self.client.indices.create(self.index, body=body)
        else:
            # Best-effort: ensure vector field exists
            try:
                m = self.client.indices.get_mapping(self.index)
                props = m[self.index]['mappings'].get('properties', {})
                if 'vector' not in props:
                    self.client.indices.put_mapping(index=self.index, body={
                        'properties': { 'vector': self._vector_mapping() }
                    })
            except Exception:
                pass

    def _vector_mapping(self):
        if self.use_knn:
            return {"type": "knn_vector", "dimension": 64}
        return {"type": "dense_vector", "dims": 64}

    def _embed(self, text: str, dims: int = 64) -> List[float]:
        """Deterministic bag-of-words hash embedding (placeholder)."""
        vec = [0.0] * dims
        if not text:
            return vec
        for tok in text.lower().split():
            h = int(hashlib.md5(tok.encode()).hexdigest(), 16)
            idx = h % dims
            vec[idx] += 1.0
        # L2 normalize
        import math
        norm = math.sqrt(sum(v*v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def search(self, q: str, top_k: int = 10) -> Dict[str, Any]:
        query = {"multi_match": {"query": q, "fields": ["title^3", "paragraph^2", "text"]}}
        resp = self.client.search(index=self.index, body={"query": query, "size": top_k})
        hits = resp.get("hits", {}).get("hits", [])
        items = [
            {
                "id": h.get("_source", {}).get("id"),
                "title": h.get("_source", {}).get("title"),
                "paragraph": h.get("_source", {}).get("paragraph"),
                "text": h.get("_source", {}).get("text", "")[:500],
                "score": h.get("_score"),
                "vector": h.get("_source", {}).get("vector"),
            }
            for h in hits
        ]
        total = resp.get("hits", {}).get("total", {}).get("value", len(items))
        return {"total": total, "items": items}

    def knn_search(self, q: str, k: int = 10) -> Dict[str, Any]:
        if not self.use_knn:
            # fallback to text + embedding rerank client-side at API
            return self.search(q, top_k=k)
        qvec = self._embed(q)
        body = {
            "size": k,
            "query": {
                "knn": {"vector": {"vector": qvec, "k": k}}
            }
        }
        resp = self.client.search(index=self.index, body=body)
        hits = resp.get("hits", {}).get("hits", [])
        items = [
            {
                "id": h.get("_source", {}).get("id"),
                "title": h.get("_source", {}).get("title"),
                "paragraph": h.get("_source", {}).get("paragraph"),
                "text": h.get("_source", {}).get("text", "")[:500],
                "score": h.get("_score"),
            }
            for h in hits
        ]
        total = resp.get("hits", {}).get("total", {}).get("value", len(items))
        return {"total": total, "items": items}

    def index_doc(self, doc: Dict[str, Any]) -> bool:
        body = dict(doc)
        # add vector embedding
        text = f"{body.get('title','')} {body.get('paragraph','')} {body.get('text','')}"
        body['vector'] = self._embed(text)
        self.client.index(index=self.index, id=body.get("id"), body=body, refresh=True)
        return True
