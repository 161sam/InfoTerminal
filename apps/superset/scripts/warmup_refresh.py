#!/usr/bin/env python3
"""Trigger Superset cache warmup/refresh via REST API."""
import os
import requests

SUPERSET_URL = os.getenv("SUPERSET_URL", "http://superset.default.svc:8088")
SUPERSET_TOKEN = os.getenv("SUPERSET_TOKEN")
DASHBOARD_IDS = os.getenv("SUPERSET_DASHBOARD_IDS", "").split(",")

headers = {"Authorization": f"Bearer {SUPERSET_TOKEN}"} if SUPERSET_TOKEN else {}

for dash_id in DASHBOARD_IDS:
    dash_id = dash_id.strip()
    if not dash_id:
        continue
    try:
        requests.post(
            f"{SUPERSET_URL}/api/v1/dashboard/{dash_id}/refresh",
            headers=headers,
            timeout=30,
        )
    except Exception as exc:
        print("Dashboard refresh warn:", exc)

try:
    requests.get(f"{SUPERSET_URL}/health", headers=headers, timeout=10)
except Exception as exc:
    print("Warmup warn:", exc)
