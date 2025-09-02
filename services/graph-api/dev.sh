#!/usr/bin/env bash
set -e
export NEO4J_URI=${NEO4J_URI:-bolt://localhost:7687}
export NEO4J_USER=${NEO4J_USER:-neo4j}
export NEO4J_PASS=${NEO4J_PASS:-neo4jpass}
uvicorn app:app --host 127.0.0.1 --port 8002 --reload
