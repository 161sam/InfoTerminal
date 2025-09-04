import httpx
import opa


def _client_factory(resp=None, exc=None):
    class DummyClient:
        def __init__(self, timeout):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def post(self, url, json):
            if exc:
                raise exc
            return resp

    return DummyClient


class DummyResp:
    def __init__(self, data, status=200):
        self.data = data
        self.status = status

    def json(self):
        return self.data

    def raise_for_status(self):
        if self.status >= 400:
            raise httpx.HTTPStatusError("err", request=None, response=None)


def test_allow_true(monkeypatch):
    resp = DummyResp({"result": True})
    monkeypatch.setattr(opa.httpx, "Client", _client_factory(resp=resp))
    assert opa.allow({}, "read", {}) is True


def test_allow_false(monkeypatch):
    resp = DummyResp({"result": False})
    monkeypatch.setattr(opa.httpx, "Client", _client_factory(resp=resp))
    assert opa.allow({}, "read", {}) is False


def test_allow_exception(monkeypatch):
    monkeypatch.setattr(opa.httpx, "Client", _client_factory(exc=RuntimeError("boom")))
    assert opa.allow({}, "read", {}) is True

