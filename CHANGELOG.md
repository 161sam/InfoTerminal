# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]
- fix: add PyYAML dependency to CLI to prevent ModuleNotFoundError for 'yaml'

## [0.1.9.1]
- Documented port policy and hardened `patch_ports.sh`
- Enforced 92% coverage gate via `pytest`
- Updated CI workflow and Quickstart docs

## [0.1.9]
- Added frontend toggle for Gateway proxy
- Compose profile for observability stack

## [0.1.8]
- Introduced `IT_ENABLE_METRICS` and `IT_OTEL` flags
- CLI gains stack inspection commands

## [0.1.7]
- Health matrix UI refinements
- `pipx` installation flow for CLI

## [0.1.6]
- Integrated Prometheus, Grafana, Loki, and Tempo
- Docker Compose profiles added

## [0.1.5]
- Frontend settings for API endpoints
- Graph-views service scaffold

## [0.1.4]
- Gateway service for unified API access
- Search and graph APIs wired through gateway

## [0.1.3]
- Developer Quickstart documentation
- CI pipeline for Python and frontend

## [0.1.2]
- CLI packaging and release automation
- Seed data and demo templates

## [0.1.1]
- Baseline project structure and services
- Standard health and readiness endpoints

## [0.1.0] – MVP
- doc-entities liefert Entitäten inklusive Kontext
- Demo-Daten Seeds und NiFi "ingest-demo" Template
- Release-Dokumentation und Roadmap aktualisiert
- search-api: standardisierte /healthz & /readyz Endpoints mit Tests
