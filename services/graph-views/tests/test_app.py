import pytest
pytest.skip("legacy sync tests skipped", allow_module_level=True)


import os, sys, json
from datetime import datetime
import types

os.environ.setdefault("OTEL_SDK_DISABLED", "1")

sys.modules.setdefault(
    "opentelemetry.instrumentation.fastapi",
    types.SimpleNamespace(
        FastAPIInstrumentor=type("FastAPIInstrumentor", (), {"instrument_app": lambda self, app: app})
    ),
)
import app as app_module  # type: ignore
from app import app
from fastapi.testclient import TestClient


class MemoryDB:
    def __init__(self):
        self.data = {}
        self.next_id = 1


class FakeCursor:
    def __init__(self, db, fail_select1=False):
        self.db = db
        self.fail_select1 = fail_select1
        self.result = None

    def execute(self, sql, params=None):
        sql = sql.strip()
        if sql == "SELECT 1":
            if self.fail_select1:
                raise RuntimeError("boom")
            self.result = (1,)
        elif sql.startswith("INSERT INTO graph_views"):
            name, owner, nodes, edges, positions = params
            vid = self.db.next_id
            self.db.next_id += 1
            self.db.data[vid] = {
                "id": vid,
                "name": name,
                "owner": owner,
                "nodes": json.loads(nodes) if isinstance(nodes, str) else nodes,
                "edges": json.loads(edges) if isinstance(edges, str) else edges,
                "positions": json.loads(positions) if isinstance(positions, str) else positions,
                "is_public": False,
                "share_token": None,
                "created_at": datetime(2024, 1, 1),
                "updated_at": datetime(2024, 1, 1),
            }
            self.result = (vid,)
        elif sql.startswith("SELECT id,name,is_public,created_at,updated_at"):
            owner, limit = params
            rows = [v for v in self.db.data.values() if v["owner"] == owner][:limit]
            self.result = [
                (r["id"], r["name"], r["is_public"], r["created_at"], r["updated_at"]) for r in rows
            ]
        elif sql.startswith("SELECT owner,is_public,share_token,name,nodes,edges,positions"):
            vid = params[0]
            v = self.db.data.get(vid)
            self.result = (
                v["owner"],
                v["is_public"],
                v["share_token"],
                v["name"],
                v["nodes"],
                v["edges"],
                v["positions"],
            ) if v else None
        elif sql.startswith("SELECT owner FROM graph_views"):
            vid = params[0]
            v = self.db.data.get(vid)
            self.result = (v["owner"],) if v else None
        elif sql.startswith("UPDATE graph_views SET is_public=TRUE, share_token"):
            token, vid, user = params
            v = self.db.data.get(vid)
            if v and v["owner"] == user:
                v["is_public"] = True
                v["share_token"] = token
                self.result = (vid,)
            else:
                self.result = None
        elif sql.startswith("UPDATE graph_views SET"):
            set_part = sql.split("SET ")[1].split(", updated_at=now()")[0]
            fields = [p.split("=")[0] for p in set_part.split(", ")]
            values = params[:-1]
            vid = params[-1]
            v = self.db.data.get(vid)
            if v:
                for f, val in zip(fields, values):
                    if f in {"nodes", "edges", "positions"} and isinstance(val, str):
                        val = json.loads(val)
                    v[f] = val
                v["updated_at"] = datetime(2024, 1, 2)
            self.result = None
        elif sql.startswith("DELETE FROM graph_views"):
            vid, user = params
            v = self.db.data.get(vid)
            if v and v["owner"] == user:
                del self.db.data[vid]
                self.result = (vid,)
            else:
                self.result = None
        else:
            self.result = None

    def fetchone(self):
        return self.result

    def fetchall(self):
        return self.result

    def __enter__(self):
        return self

    def __exit__(self, *a):
        pass


class FakeConn:
    def __init__(self, db, fail_select1=False):
        self.db = db
        self.fail_select1 = fail_select1

    def cursor(self):
        return FakeCursor(self.db, self.fail_select1)


class FakePool:
    def __init__(self, db, fail_select1=False):
        self.db = db
        self.fail_select1 = fail_select1

    def getconn(self):
        return FakeConn(self.db, self.fail_select1)

    def putconn(self, conn):  # pragma: no cover - trivial
        pass

    def closeall(self):  # pragma: no cover - trivial
        pass


@pytest.fixture
def client(monkeypatch):
    db = MemoryDB()
    pool = FakePool(db)
    monkeypatch.setattr(app_module, "setup_pool", lambda: pool)
    monkeypatch.setenv("INIT_DB_ON_STARTUP", "0")
    with TestClient(app) as c:
        yield c, db


def test_conn_without_pool():
    app_module.pool = None
    with pytest.raises(RuntimeError):
        with app_module.conn():
            pass


def test_user_from_header():
    assert app_module.user_from_header(None) == "dev"
    assert app_module.user_from_header("alice") == "alice"


def test_lifespan_success(monkeypatch):
    db = MemoryDB()
    pool = FakePool(db)
    monkeypatch.setattr(app_module, "setup_pool", lambda: pool)
    monkeypatch.setenv("INIT_DB_ON_STARTUP", "1")
    with TestClient(app) as c:
        assert c.app.state.pool is pool
    assert app.state.pool is None
    assert app_module.pool is pool


def test_lifespan_failure(monkeypatch):
    def broken():
        raise RuntimeError("no db")

    monkeypatch.setattr(app_module, "setup_pool", broken)
    with TestClient(app) as c:
        assert c.app.state.pool is None
    assert app_module.pool is None


def test_crud_flow(client):
    c, db = client
    r = c.post("/views", json={}, headers={"x-user": "alice"})
    vid = r.json()["id"]
    db.data[vid]["share_token"] = "abc"
    r = c.get(f"/views/{vid}", headers={"x-user": "bob"}, params={"token": "abc"})
    assert r.status_code == 200
    r = c.get("/views", headers={"x-user": "alice"})
    assert r.json()[0]["name"] == "Untitled"
    r = c.get(f"/views/{vid}", headers={"x-user": "alice"})
    assert r.status_code == 200
    r = c.put(
        f"/views/{vid}",
        json={"name": "n", "nodes": [1], "edges": [], "positions": {}, "is_public": False},
        headers={"x-user": "alice"},
    )
    assert r.json()["updated"] == 1
    r = c.post(f"/views/{vid}/share", headers={"x-user": "alice"})
    assert r.status_code == 200
    r = c.get(f"/views/{vid}", headers={"x-user": "carol"})
    assert r.status_code == 200
    r = c.delete(f"/views/{vid}", headers={"x-user": "alice"})
    assert r.json()["deleted"] == 1
    r = c.get("/views", headers={"x-user": "alice"})
    assert r.json() == []


def test_get_view_errors(client):
    c, db = client
    vid = c.post("/views", json={}, headers={"x-user": "alice"}).json()["id"]
    with pytest.raises(app_module.HTTPException) as e:
        app_module.get_view(999, x_user="alice")
    assert e.value.status_code == 404
    with pytest.raises(app_module.HTTPException) as e:
        app_module.get_view(vid, x_user="bob")
    assert e.value.status_code == 403


def test_update_view_errors(client):
    c, db = client
    vid = c.post("/views", json={}, headers={"x-user": "alice"}).json()["id"]
    assert app_module.update_view(vid, {}, x_user="alice")["updated"] == 0
    with pytest.raises(app_module.HTTPException) as e:
        app_module.update_view(999, {"name": "x"}, x_user="alice")
    assert e.value.status_code == 404
    with pytest.raises(app_module.HTTPException) as e:
        app_module.update_view(vid, {"name": "x"}, x_user="bob")
    assert e.value.status_code == 403


def test_share_delete_forbidden(client):
    c, db = client
    vid = c.post("/views", json={}, headers={"x-user": "alice"}).json()["id"]
    with pytest.raises(app_module.HTTPException) as e:
        app_module.share_view(vid, x_user="bob")
    assert e.value.status_code == 403
    with pytest.raises(app_module.HTTPException) as e:
        app_module.delete_view(vid, x_user="bob")
    assert e.value.status_code == 403


def test_pg_env_and_setup_pool(monkeypatch):
    import builtins, importlib

    class DummySCP:
        def __init__(self, *a, **k):
            self.kw = k

    monkeypatch.setenv("PG_HOST", "dbhost")
    monkeypatch.setitem(sys.modules, "psycopg2.pool", types.SimpleNamespace(SimpleConnectionPool=DummySCP))

    real_import = builtins.__import__

    def fake_import(name, *a, **k):
        if name == "_shared.obs.otel_boot":
            raise ImportError("missing")
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    mod = importlib.reload(app_module)
    pool = mod.setup_pool()
    assert isinstance(pool, DummySCP)
    assert mod.PG["host"] == "dbhost"
    importlib.reload(mod)
