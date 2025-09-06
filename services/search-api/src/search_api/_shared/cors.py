import os
from typing import Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

DEFAULT_ORIGINS = ["http://localhost:3411", "http://127.0.0.1:3411"]


def get_cors_settings_from_env() -> Dict[str, object]:
    origins_env = os.getenv("IT_CORS_ORIGINS")
    if origins_env:
        origins: List[str] = [o.strip() for o in origins_env.split(",") if o.strip()]
    else:
        origins = DEFAULT_ORIGINS

    allow_credentials = os.getenv("IT_CORS_CREDENTIALS", "0") == "1"
    max_age = int(os.getenv("IT_CORS_MAX_AGE", "600"))

    return {
        "allow_origins": origins,
        "allow_credentials": allow_credentials,
        "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": [
            "Authorization",
            "Content-Type",
            "X-Request-Id",
            "X-CSRF-Token",
        ],
        "expose_headers": ["X-Request-Id"],
        "max_age": max_age,
    }


def apply_cors(app: FastAPI, settings: Dict[str, object] | None = None) -> None:
    if settings is None:
        settings = get_cors_settings_from_env()
    app.add_middleware(CORSMiddleware, **settings)
