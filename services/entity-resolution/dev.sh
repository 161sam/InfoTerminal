#!/usr/bin/env bash
set -e
uvicorn app:app --host 127.0.0.1 --port 8003 --reload
