from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "data" / "fixtures"
SEEDS_DIR = Path(__file__).resolve().parents[1] / "data" / "seeds"


def load_fixture(name: str) -> Any:
    path = FIXTURES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Fixture '{name}' not found at {path}")
    return json.loads(path.read_text())


def load_seed(name: str) -> Any:
    path = SEEDS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Seed '{name}' not found at {path}")
    return json.loads(path.read_text())


def _parse_timestamp(raw: str) -> datetime:
    cleaned = raw
    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1] + "+00:00"
    return datetime.fromisoformat(cleaned)


def _coerce_date(value: str) -> date:
    if "T" in value:
        return _parse_timestamp(value).date()
    return date.fromisoformat(value)


@dataclass
class SearchDocument:
    id: str
    title: str
    content: str
    source: str
    timestamp: datetime
    tags: List[str]
    relevance_score: float
    source_type: str

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SearchDocument":
        return cls(
            id=str(data["id"]),
            title=str(data.get("title", "")),
            content=str(data.get("content", "")),
            source=str(data.get("source", "")),
            timestamp=_parse_timestamp(str(data.get("timestamp"))),
            tags=list(data.get("tags", [])),
            relevance_score=float(data.get("relevance_score", 0.0)),
            source_type=str(data.get("source_type", "unknown")),
        )

    def contains_terms(self, terms: Iterable[str]) -> bool:
        tokens = [term.lower() for term in terms]
        haystack = f"{self.title} {self.content}".lower()
        matched = sum(1 for token in tokens if token in haystack)
        required = max(1, math.ceil(len(tokens) * 0.6)) if tokens else 0
        return matched >= required


class SearchEngine:
    """Minimal deterministic search facade for regression tests."""

    def __init__(self, documents: Iterable[Mapping[str, Any]]):
        self.index = [SearchDocument.from_dict(doc) for doc in documents]

    def query(self, query: str, filters: Optional[Mapping[str, Any]] = None) -> List[SearchDocument]:
        filters = filters or {}
        tokens = [token for token in query.lower().split() if token]
        results: List[SearchDocument] = []
        for doc in self.index:
            if not doc.contains_terms(tokens):
                continue
            if not self._matches_filters(doc, filters):
                continue
            results.append(doc)
        return sorted(results, key=lambda d: d.relevance_score, reverse=True)

    @staticmethod
    def _matches_filters(doc: SearchDocument, filters: Mapping[str, Any]) -> bool:
        for key, value in filters.items():
            if key == "source_type" and doc.source_type.lower() != str(value).lower():
                return False
            if key == "date_range":
                start_s, end_s = str(value).split(":")
                start = _coerce_date(start_s)
                end = _coerce_date(end_s)
                doc_date = doc.timestamp.date()
                if not (start <= doc_date <= end):
                    return False
        return True


@dataclass
class GraphData:
    nodes: Dict[str, Dict[str, Any]]
    relationships: List[Dict[str, Any]]

    @classmethod
    def from_fixture(cls, fixture: Mapping[str, Any]) -> "GraphData":
        nodes = {entity["name"]: dict(entity) for entity in fixture.get("entities", [])}
        relationships = [dict(rel) for rel in fixture.get("relationships", [])]
        return cls(nodes=nodes, relationships=relationships)

    @classmethod
    def from_entities(
        cls, entities: Iterable[Mapping[str, Any]], relationships: Iterable[Mapping[str, Any]]
    ) -> "GraphData":
        nodes = {entity["name"]: dict(entity) for entity in entities}
        rels = [dict(rel) for rel in relationships]
        return cls(nodes=nodes, relationships=rels)

    def degree(self, node_name: str) -> int:
        return sum(1 for rel in self.relationships if rel.get("from") == node_name or rel.get("to") == node_name)

    def filter_by_entity(self, entity_name: str, depth: int = 1) -> "GraphData":
        if entity_name not in self.nodes:
            return GraphData(nodes={}, relationships=[])
        included = {entity_name}
        rels: List[Dict[str, Any]] = []
        current = {entity_name}
        for _ in range(max(depth, 1)):
            next_level: set[str] = set()
            for rel in self.relationships:
                if rel.get("from") in current or rel.get("to") in current:
                    rels.append(rel)
                    next_level.update([rel.get("from"), rel.get("to")])
            current = next_level - included
            included.update(next_level)
        nodes = {name: self.nodes[name] for name in included if name in self.nodes}
        return GraphData(nodes=nodes, relationships=rels)

    def analytics(self) -> Dict[str, Any]:
        component_nodes = len(self.nodes)
        component_edges = len(self.relationships)
        return {
            "node_count": component_nodes,
            "relationship_count": component_edges,
            "degrees": {name: self.degree(name) for name in self.nodes},
        }


class DossierBuilder:
    """Compose lightweight dossier artefacts from search and graph data."""

    def build(
        self,
        focus: str,
        search_results: List[SearchDocument],
        graph: GraphData,
        summary_points: int = 3,
    ) -> Dict[str, Any]:
        top = search_results[0]
        analytics = graph.analytics()
        entity_highlights = [f"{name} ({node.get('type', 'unknown')})" for name, node in graph.nodes.items()]
        summary_lines = [
            f"Top document: {top.title} ({top.timestamp.date()})",
            f"Total entities: {analytics['node_count']}",
            f"Relationships: {analytics['relationship_count']}",
        ]
        summary_lines.append(f"Key excerpt: {top.content}")
        markdown = [f"# Dossier: {focus}", "", "## Key Insight", f"- {summary_lines[0]}"]
        markdown.append("\n## Entity Highlights")
        for highlight in entity_highlights[:summary_points]:
            markdown.append(f"- {highlight}")
        markdown.append("\n## Connected Relationships")
        for rel in graph.relationships[:summary_points]:
            markdown.append(
                f"- {rel.get('from')} → {rel.get('to')} ({rel.get('type')})"
            )
        return {
            "focus": focus,
            "summary": "; ".join(summary_lines),
            "graph": analytics,
            "sections": {
                "entities": entity_highlights,
                "relationships": [
                    {
                        "from": rel.get("from"),
                        "to": rel.get("to"),
                        "type": rel.get("type"),
                    }
                    for rel in graph.relationships
                ],
            },
            "markdown": "\n".join(markdown),
        }


class NlpExtractor:
    """Deterministic entity and relation extraction for regression data."""

    def extract(self, document: Mapping[str, Any]) -> Dict[str, Any]:
        text = str(document.get("text", ""))
        entities = []
        for entity in document.get("expected_entities", []):
            token = entity["text"]
            if token not in text:
                raise AssertionError(f"Expected entity '{token}' missing from document")
            enriched = dict(entity)
            enriched.setdefault("confidence", 0.98)
            entities.append(enriched)
        relationships = []
        for rel in document.get("expected_relationships", []):
            if rel["source"] not in {e["text"] for e in entities}:
                raise AssertionError(f"Source '{rel['source']}' not extracted")
            if rel["target"] not in {e["text"] for e in entities}:
                raise AssertionError(f"Target '{rel['target']}' not extracted")
            enriched_rel = dict(rel)
            enriched_rel.setdefault("confidence", 0.95)
            relationships.append(enriched_rel)
        return {"entities": entities, "relationships": relationships}


class MapProjector:
    """Project graph entities onto a minimal GeoJSON feature collection."""

    DEFAULT_COORDINATES = {
        "Washington D.C.": {"lat": 38.9072, "lon": -77.0369},
        "Global": {"lat": 0.0, "lon": 0.0},
        "United States": {"lat": 38.0, "lon": -97.0},
    }

    def __init__(self, coordinates: Optional[Mapping[str, Mapping[str, float]]] = None):
        self.coordinates = {**self.DEFAULT_COORDINATES, **(coordinates or {})}

    def project(self, entities: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
        features = []
        for entity in entities:
            if str(entity.get("type", "")).upper() not in {"LOCATION", "PLACE"}:
                continue
            name = entity.get("text") or entity.get("name")
            coords = self.coordinates.get(str(name))
            if not coords:
                continue
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [coords["lon"], coords["lat"]],
                    },
                    "properties": {
                        "name": name,
                        "confidence": entity.get("confidence", 0.0),
                    },
                }
            )
        return {"type": "FeatureCollection", "features": features}


class ToolRegistry:
    """Minimal orchestrator registry used by agent regression tests."""

    def __init__(self, search_engine: SearchEngine, graph: GraphData, dossier: DossierBuilder):
        self.search_engine = search_engine
        self.graph = graph
        self.dossier = dossier

    def dispatch(
        self,
        tool: str,
        payload: MutableMapping[str, Any],
        context: Mapping[str, Any] | None = None,
    ) -> Dict[str, Any]:
        context = context or {}
        if tool == "search.news":
            results = self.search_engine.query(payload["query"], payload.get("filters"))[: payload.get("limit", 3)]
            payload_result = [doc.__dict__ for doc in results]
            return {"results": payload_result}
        if tool == "graph.expand":
            focus = payload["entity"]
            subgraph = self.graph.filter_by_entity(focus, depth=payload.get("depth", 1))
            return {
                "nodes": subgraph.nodes,
                "relationships": subgraph.relationships,
                "analytics": subgraph.analytics(),
            }
        if tool == "dossier.build":
            focus = payload["focus"]
            search_key = payload.get("search_key", "search_results")
            graph_key = payload.get("graph_key", "subgraph")
            search_payload = context.get(search_key, {}).get("results") or []
            documents = [SearchDocument.from_dict(doc) for doc in search_payload]
            if not documents:
                raise ValueError("dossier.build requires search results in context")
            graph_payload = context.get(graph_key, {})
            subgraph = GraphData.from_entities(
                graph_payload.get("nodes", {}).values(),
                graph_payload.get("relationships", []),
            )
            artefact = self.dossier.build(focus, documents, subgraph, summary_points=payload.get("summary_points", 3))
            return artefact
        raise KeyError(f"Unknown tool '{tool}'")

    def final_answer(self, prompt: str, context: Mapping[str, Any]) -> str:
        dossier = context.get("dossier", {})
        summary = dossier.get("summary", "")
        key_entities = ", ".join(dossier.get("sections", {}).get("entities", [])[:3])
        return (
            f"Prompt: {prompt}\n"
            f"Summary: {summary}\n"
            f"Key entities: {key_entities}"
        )


def ingest_feed(entries: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize raw feed entries into a deterministic structure."""
    normalized = []
    for entry in entries:
        published_at = datetime.fromisoformat(str(entry.get("published_at")))
        normalized.append(
            {
                "id": entry.get("id"),
                "title": entry.get("title"),
                "published_at": published_at,
                "source": entry.get("source"),
                "region": entry.get("region"),
                "topics": list(entry.get("topics", [])),
                "sentiment": float(entry.get("sentiment", 0.0)),
            }
        )
    return normalized


def build_dashboard_metrics(feeds: Iterable[List[Dict[str, Any]]]) -> Dict[str, Any]:
    all_entries = [entry for feed in feeds for entry in feed]
    total_items = len(all_entries)
    topic_counter: Counter[str] = Counter()
    region_counter: Counter[str] = Counter()
    sentiment_total = 0.0
    for entry in all_entries:
        topic_counter.update(entry.get("topics", []))
        region_counter.update([entry.get("region")])
        sentiment_total += entry.get("sentiment", 0.0)
    average_sentiment = round(sentiment_total / total_items, 4) if total_items else 0.0
    return {
        "total_items": total_items,
        "top_topics": dict(topic_counter),
        "regional_breakdown": dict(region_counter),
        "average_sentiment": average_sentiment,
    }
