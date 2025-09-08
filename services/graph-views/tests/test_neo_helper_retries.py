import time

import neo


class FailThenSucceed:
    def __init__(self):
        self.calls = 0

    def run(self, stmt, **kwargs):
        self.calls += 1
        if self.calls < 3:
            raise neo.TransientError("tmp")
        return "ok"


def test_run_with_retries(monkeypatch):
    session = FailThenSucceed()
    sleeps = []
    monkeypatch.setattr(time, "sleep", lambda s: sleeps.append(s))
    res = neo.run_with_retries(session, "RETURN 1")
    assert res == "ok"
    assert session.calls == 3
    assert sleeps == [neo.exponential_backoff(0), neo.exponential_backoff(1)]
