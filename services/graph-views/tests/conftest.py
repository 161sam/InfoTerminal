import base64
import os
import sys
import types

import pytest
from fastapi.testclient import TestClient

# ensure predictable environment
os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("IT_JSON_LOGS", "1")
os.environ.setdefault("IT_ENV", "test")
os.environ.setdefault("IT_LOG_SAMPLING", "")
os.environ.setdefault("IT_OTEL", "1")
os.environ.setdefault("TESTING_OTEL_BOOT", "1")

# provide a minimal asyncpg stub so db modules can be imported without dependency
sys.modules.setdefault(
    "asyncpg",
    types.SimpleNamespace(Pool=object, create_pool=lambda *a, **k: None),
)

import neo as neo_module  # noqa: E402


class FakeRecord(dict):
    def data(self):
        return self


class FakeResult:
    def __init__(self, records=None, nodes_created=0, rels_created=0):
        self.records = records or []
        counters = types.SimpleNamespace(
            nodes_created=nodes_created, relationships_created=rels_created
        )
        self._summary = types.SimpleNamespace(counters=counters)

    def consume(self):
        return self._summary

    def data(self):  # pragma: no cover - compatibility
        return self.records

    def __iter__(self):
        return iter(self.records)


class FakeSession:
    def __init__(self):
        self.runs = []

    def run(self, stmt, **kwargs):
        self.runs.append((stmt, kwargs))
        low = stmt.lower()
        if "return n" in low:
            return FakeResult([
                FakeRecord(
                    {
                        "n": {
                            "__type": "node",
                            "id": "alice",
                            "labels": ["Person"],
                            "properties": {"id": "alice"},
                        }
                    }
                )
            ])
        if "shortestpath" in low:
            return FakeResult(
                [
                    FakeRecord(
                        {
                            "p": {
                                "__type": "path",
                                "nodes": [
                                    {
                                        "__type": "node",
                                    "id": "alice",
                                    "labels": ["Person"],
                                    "properties": {},
                                },
                                {
                                    "__type": "node",
                                    "id": "bob",
                                    "labels": ["Person"],
                                    "properties": {},
                                },
                            ],
                            "relationships": [
                                {
                                    "__type": "relationship",
                                    "id": "r1",
                                    "type": "KNOWS",
                                    "start": "alice",
                                    "end": "bob",
                                    "properties": {},
                                }
                            ],
                            "length": 1,
                            }
                        }
                    )
                ]
            )
        if "collect(p)" in low:
            return FakeResult(
                [
                    FakeRecord(
                        {
                            "n": {
                                "__type": "node",
                                "id": "alice",
                                "labels": ["Person"],
                                "properties": {"id": "alice"},
                            },
                            "paths": [
                                {
                                    "__type": "path",
                                    "nodes": [
                                        {
                                            "__type": "node",
                                            "id": "alice",
                                            "labels": ["Person"],
                                            "properties": {"id": "alice"},
                                        },
                                        {
                                            "__type": "node",
                                            "id": "bob",
                                            "labels": ["Person"],
                                            "properties": {"id": "bob"},
                                        },
                                    ],
                                    "relationships": [
                                        {
                                            "__type": "relationship",
                                            "id": "r1",
                                            "type": "KNOWS",
                                            "start": "alice",
                                            "end": "bob",
                                            "properties": {},
                                        }
                                    ],
                                    "length": 1,
                                }
                            ],
                        }
                    )
                ]
            )
        return FakeResult([])

    def close(self):
        pass


class FakeDriver:
    def __init__(self):
        self.session_obj = FakeSession()

    def session(self, database=None):
        return self.session_obj

    def close(self):  # pragma: no cover - nothing to close
        pass

    def verify_connectivity(self):  # pragma: no cover - always ok
        return True


@pytest.fixture
def mock_driver(monkeypatch):
    drv = FakeDriver()
    monkeypatch.setattr(neo_module, "get_driver", lambda: drv)
    return drv.session_obj


@pytest.fixture
def app_client(mock_driver):
    from app import app

    with TestClient(app) as client:
        yield client


def basic_auth_header(user: str, pwd: str) -> dict[str, str]:
    token = base64.b64encode(f"{user}:{pwd}".encode()).decode()
    return {"Authorization": f"Basic {token}"}
