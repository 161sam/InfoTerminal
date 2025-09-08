import importlib
import sys
import types
from pathlib import Path

SAMPLES_DIR = Path(__file__).resolve().parents[1] / "samples"
sys.path.insert(0, str(SAMPLES_DIR))
loader = importlib.import_module("load_csv")


def test_chunked():
    rows = [{"id": i} for i in range(5)]
    batches = list(loader.chunked(rows, 2))
    assert batches == [rows[0:2], rows[2:4], rows[4:5]]


def test_csv_loader_run(monkeypatch, tmp_path):
    csv_file = tmp_path / "people.csv"
    csv_file.write_text("id,name,knows_id\n1,Alice,2\n2,Bob,\n", encoding="utf-8")

    class FakeSession:
        def __init__(self):
            self.runs = []

        def run(self, stmt, **kwargs):
            self.runs.append((stmt, kwargs))
            summary = types.SimpleNamespace(
                counters=types.SimpleNamespace(nodes_created=0, relationships_created=0)
            )
            return types.SimpleNamespace(consume=lambda: summary)

        def close(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    class FakeDriver:
        def __init__(self):
            self.session_obj = FakeSession()

        def session(self, database=None):
            return self.session_obj

        def verify_connectivity(self):
            return True

        def close(self):
            pass

    fake = FakeDriver()
    monkeypatch.setattr(
        loader, "GraphDatabase", types.SimpleNamespace(driver=lambda *a, **k: fake)
    )
    monkeypatch.setattr(sys, "argv", [
        "load_csv.py",
        "--csv",
        str(csv_file),
        "--batch-size",
        "1",
    ])
    nodes, rels = loader.run()
    assert nodes == 0 and rels == 0
    stmts = [s for s, _ in fake.session_obj.runs]
    assert any("MERGE" in s for s in stmts)
