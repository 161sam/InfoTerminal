import importlib
import sys


class DummyApp:
    def __init__(self):
        self.middleware = []

    def add_middleware(self, mw):
        self.middleware.append(mw)


def _load_module():
    sys.modules.pop("obs.otel_boot", None)
    return importlib.import_module("obs.otel_boot")


def test_setup_otel_noop(monkeypatch):
    monkeypatch.delenv("IT_OTEL", raising=False)
    m = _load_module()
    app = DummyApp()
    m.setup_otel(app, service_name="graph-api")
    assert m.INSTRUMENTATION_ENABLED is False


def test_setup_otel_fail_open(monkeypatch):
    monkeypatch.setenv("IT_OTEL", "1")
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:1")
    m = _load_module()
    app = DummyApp()
    m.setup_otel(app, service_name="graph-api")
    assert m.INSTRUMENTATION_ENABLED is True
