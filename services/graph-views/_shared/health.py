import os, asyncio, inspect
from typing import Callable, Iterable, Any, Awaitable, Optional
from fastapi.responses import JSONResponse

def _truthy(v: str | None) -> bool:
    return str(v or "0").lower() in ("1", "true", "yes", "on")

async def _maybe_await(x):
    if inspect.isawaitable(x):
        return await x
    return x

def make_healthz(*_args: Any, **_kwargs: Any):
    async def _healthz():
        try:
            return {"status": "ok"}
        except Exception as e:
            return JSONResponse({"status": "error", "error": repr(e)}, status_code=500)
    return _healthz

def _normalize_checks(args: tuple[Any, ...]) -> list[Callable[[], Awaitable[Any] | Any]]:
    if not args:
        return []
    if len(args) == 1 and isinstance(args[0], (list, tuple, set)):
        return list(args[0])
    return list(args)

def make_readyz(
    *checks: Callable[[], Awaitable[Any] | Any],
    ready_flag_env: str = "IT_FORCE_READY",
):
    checks = _normalize_checks(checks)

    async def _readyz():
        try:
            if _truthy(os.getenv(ready_flag_env, "0")):
                return {"status": "ready", "forced": True}

            for chk in checks:
                try:
                    res = await _maybe_await(chk())
                    if res is False:
                        return JSONResponse(
                            {"status": "not-ready", "reason": "check returned False"},
                            status_code=503,
                        )
                except Exception as ce:
                    return JSONResponse(
                        {"status": "not-ready", "error": repr(ce)},
                        status_code=503,
                    )
            return {"status": "ready"}
        except Exception as e:
            return JSONResponse({"status": "error", "error": repr(e)}, status_code=500)

    return _readyz
