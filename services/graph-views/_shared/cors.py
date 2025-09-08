import os
from typing import Any, Dict, List
from fastapi.middleware.cors import CORSMiddleware

def get_cors_settings_from_env() -> Dict[str, Any]:
    origins_env = os.getenv("CORS_ORIGINS", "*").strip()
    if origins_env == "*" or not origins_env:
        origins: List[str] = ["*"]
    else:
        origins = [o.strip() for o in origins_env.split(",") if o.strip()]
    allow_methods_env = os.getenv("CORS_ALLOW_METHODS", "*")
    allow_headers_env = os.getenv("CORS_ALLOW_HEADERS", "*")
    allow_credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() not in ("0", "false", "no")

    return {
        "allow_origins": origins,
        "allow_methods": ["*"] if allow_methods_env == "*" else [m.strip() for m in allow_methods_env.split(",")],
        "allow_headers": ["*"] if allow_headers_env == "*" else [h.strip() for h in allow_headers_env.split(",")],
        "allow_credentials": allow_credentials,
    }

def apply_cors(app, settings: Dict[str, Any] | None = None):
    s = settings or get_cors_settings_from_env()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=s["allow_origins"],
        allow_credentials=s.get("allow_credentials", True),
        allow_methods=s.get("allow_methods", ["*"]),
        allow_headers=s.get("allow_headers", ["*"]),
    )
    return app
