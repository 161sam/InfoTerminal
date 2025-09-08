from typing import Optional

def enable_prometheus_metrics(
    app,
    route: str = "/metrics",
    *,
    path: Optional[str] = None,
    registry=None,
    **_ignored,
) -> None:
    """
    Registriert eine Metrics-Route.
    - akzeptiert sowohl 'route' als auch 'path' (alias)
    - optionales 'registry' wird ignoriert, wenn nicht nutzbar
    - fällt robust auf Plaintext zurück, falls prometheus_client fehlt
    """
    endpoint = path or route

    try:
        from prometheus_client import REGISTRY, generate_latest, CONTENT_TYPE_LATEST
        from fastapi import Response

        # Falls eine Registry gereicht wurde, versuchen zu nutzen; sonst Default.
        reg = registry if registry is not None else REGISTRY

        @app.get(endpoint)
        async def _metrics():
            data = generate_latest(reg)
            return Response(content=data, media_type=CONTENT_TYPE_LATEST)

    except Exception:
        # Minimaler Fallback, damit die App nicht crasht.
        from fastapi.responses import PlainTextResponse

        @app.get(endpoint)
        async def _metrics():
            return PlainTextResponse("# prometheus_client not installed\n")
