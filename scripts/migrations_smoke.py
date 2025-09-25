#!/usr/bin/env python3
"""End-to-end smoke test for doc-entities migrations."""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import sqlalchemy as sa
from sqlalchemy.engine import Engine

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPO_ROOT / "services" / "doc-entities" / "migrations" / "runner.py"
TABLES = [
    "documents",
    "entities",
    "entity_resolutions",
    "relations",
    "relation_resolutions",
]
BASE_TABLES = ["documents", "entities", "entity_resolutions"]


def _load_runner_module():
    spec = importlib.util.spec_from_file_location("doc_entities_migration_runner", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load migration runner module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _prepare_database_url(explicit_url: Optional[str]) -> tuple[str, Optional[tempfile.TemporaryDirectory]]:
    if explicit_url:
        return explicit_url, None
    env_url = os.getenv("MIGRATIONS_SMOKE_DATABASE_URL") or os.getenv("DATABASE_URL")
    if env_url:
        return env_url, None
    tmpdir = tempfile.TemporaryDirectory()
    db_path = Path(tmpdir.name) / "doc_entities_smoke.db"
    return f"sqlite:///{db_path}", tmpdir


def _create_engine(database_url: str) -> Engine:
    return sa.create_engine(database_url, future=True)


def _seed_dataset(engine: Engine) -> None:
    doc_id = str(uuid.uuid4())
    entity_a = str(uuid.uuid4())
    entity_b = str(uuid.uuid4())
    relation_id = str(uuid.uuid4())

    with engine.begin() as conn:
        metadata = sa.MetaData()
        documents = sa.Table("documents", metadata, autoload_with=conn)
        entities = sa.Table("entities", metadata, autoload_with=conn)
        entity_resolutions = sa.Table("entity_resolutions", metadata, autoload_with=conn)
        relations = sa.Table("relations", metadata, autoload_with=conn)
        relation_resolutions = sa.Table("relation_resolutions", metadata, autoload_with=conn)

        conn.execute(
            documents.insert(),
            {
                "id": doc_id,
                "title": "Smoke Test Document",
                "source": "integration",
                "aleph_id": "SMOKE-001",
            },
        )
        conn.execute(
            entities.insert(),
            [
                {
                    "id": entity_a,
                    "doc_id": doc_id,
                    "label": "PERSON",
                    "value": "Jane Doe",
                    "span_start": 0,
                    "span_end": 8,
                    "confidence": 0.93,
                },
                {
                    "id": entity_b,
                    "doc_id": doc_id,
                    "label": "ORG",
                    "value": "Acme Corp",
                    "span_start": 15,
                    "span_end": 24,
                    "confidence": 0.88,
                },
            ],
        )
        conn.execute(
            entity_resolutions.insert(),
            {
                "entity_id": entity_a,
                "node_id": "neo4j://entity/123",
                "score": 0.97,
                "status": "resolved",
                "candidates": [{"id": "neo4j://entity/123", "score": 0.97}],
            },
        )
        conn.execute(
            relations.insert(),
            {
                "id": relation_id,
                "doc_id": doc_id,
                "subject_entity_id": entity_a,
                "object_entity_id": entity_b,
                "predicate": "EMPLOYED_AT",
                "predicate_text": "works at",
                "confidence": 0.81,
                "span_start": 30,
                "span_end": 38,
                "context": "Jane Doe works at Acme Corp.",
                "extraction_method": "rule",
                "metadata": {"model": "smoke-rel"},
            },
        )
        conn.execute(
            relation_resolutions.insert(),
            {
                "relation_id": relation_id,
                "graph_edge_id": "neo4j://edge/456",
                "status": "resolved",
                "score": 0.88,
                "metadata": {"method": "smoke"},
            },
        )

    return None


def _normalize_value(value):
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _snapshot(engine: Engine, table_names: List[str]) -> Dict[str, Optional[List[Dict]]]:
    snapshot: Dict[str, Optional[List[Dict]]] = {}
    with engine.begin() as conn:
        inspector = sa.inspect(conn)
        metadata = sa.MetaData()
        for table_name in table_names:
            if not inspector.has_table(table_name):
                snapshot[table_name] = None
                continue
            table = sa.Table(table_name, metadata, autoload_with=conn)
            rows = conn.execute(sa.select(table)).mappings().all()
            normalized = []
            for row in rows:
                normalized.append({key: _normalize_value(value) for key, value in row.items()})
            snapshot[table_name] = sorted(normalized, key=lambda item: tuple(sorted(item.items())))
    return snapshot


def _assert_same(label: str, left: Dict, right: Dict) -> None:
    if left != right:
        raise AssertionError(f"{label} mismatch:\nLEFT: {left}\nRIGHT: {right}")


def run_smoke(database_url: str) -> None:
    module = _load_runner_module()
    engine = _create_engine(database_url)
    runner = module.MigrationRunner(engine)

    print("⏫ Running upgrade to head with backfill…")
    runner.upgrade(run_backfill=True)

    print("🧪 Seeding mini dataset…")
    _seed_dataset(engine)
    initial_snapshot = _snapshot(engine, TABLES)

    print("⏬ Downgrading to revision 002…")
    runner.downgrade("002")
    downgraded_snapshot = _snapshot(engine, BASE_TABLES)
    _assert_same("Base tables after downgrade", {
        table: initial_snapshot[table] for table in BASE_TABLES
    }, downgraded_snapshot)

    print("⏫ Upgrading back to head…")
    runner.upgrade(run_backfill=True)
    final_snapshot = _snapshot(engine, TABLES)

    print("✅ Verifying data integrity…")
    _assert_same("Final snapshot", initial_snapshot, final_snapshot)

    with engine.begin() as conn:
        inspector = sa.inspect(conn)
        assert not inspector.has_table("doc_entities_relations_backup"), "Backup table should be cleaned up"
        assert not inspector.has_table(
            "doc_entities_relation_resolutions_backup"
        ), "Backup resolutions table should be cleaned up"

    print("🎉 Migrations smoke test passed for doc-entities")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-url", dest="database_url", help="Optional database URL override.")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    database_url, tmpdir = _prepare_database_url(args.database_url)
    try:
        run_smoke(database_url)
    finally:
        if tmpdir is not None:
            tmpdir.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
