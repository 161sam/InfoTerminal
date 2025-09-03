SHELL := /bin/bash
KIND_CLUSTER := infoterminal
K8S_CONTEXT := kind-$(KIND_CLUSTER)

.PHONY: dev-up dev-down apps-up apps-down seed-demo seed-graph print-info auth-up opa-up neo4j-up opa-test aleph-workers-up nifi-registry-up dbt-run etl-dbt-build etl-nifi-deploy etl-airflow-up etl-airflow-dag etl-superset-warmup nifi-template-import nifi-template-instantiate nifi-start nifi-stop dbt-all

auth-up:
		@bash infra/auth/keycloak_import.sh

opa-up:
	kubectl apply -f infra/k8s/opa/opa.yaml

neo4j-up:
        kubectl apply -f infra/k8s/neo4j/neo4j.yaml

apps-down:
	@pkill -f "uv run" || true
	@pkill -f "next" || true

seed-demo:
	@bash scripts/seed_demo.sh

seed-graph:
	@python3 services/graph-api/scripts/seed_graph.py

print-info:
	@echo "Kubernetes context: $(K8S_CONTEXT)"
	@kubectl --context $(K8S_CONTEXT) get pods -A



opa-test:
	@opa test -v policy

opa-bundle:
	@opa build -b policy -o dist/opa/bundle.tar.gz

bundle-server-up:
	@mkdir -p dist/opa
	@python3 -m http.server 8077 --directory dist/opa

aleph-workers-up:
	kubectl apply -f infra/k8s/aleph/aleph-workers.yaml

nifi-registry-up:
	kubectl apply -f infra/k8s/nifi/registry.yaml
	bash infra/nifi/scripts/connect-registry.sh

dbt-run:
	cd etl/dbt && dbt deps && dbt seed && dbt run && dbt test

dbt-all:
	@bash etl/dbt/dev_run_all.sh

etl-dbt-build:
	cd etl/dbt && dbt deps && dbt seed --full-refresh && dbt run && dbt test

etl-nifi-deploy:
	bash etl/nifi/scripts/deploy_aleph_ingest.sh

etl-airflow-up:
	docker compose -f etl/airflow/docker-compose.yml up -d  # falls vorhanden

etl-airflow-dag:
	airflow dags list | grep openbb_dbt_superset || true

etl-superset-warmup:
	python apps/superset/scripts/warmup_refresh.py


.PHONY: obs-down obs-reload
obs-down:
	docker compose rm -sf prometheus grafana

obs-reload:
	curl -X POST http://localhost:9090/-/reload || true

nifi-template-import:
	@bash scripts/nifi_template_import.sh

nifi-template-instantiate:
	@bash scripts/nifi_template_instantiate.sh

nifi-start:
	@bash scripts/nifi_start.sh

nifi-stop:
	@bash scripts/nifi_stop.sh

.PHONY: docs-lint docs-toc docs-open
docs-lint:
	npx markdownlint-cli2 README.md 'docs/**/*.md' -c .markdownlint.json || true
	npx lychee --accept 200,429 README.md docs/**/*.md || true

docs-toc:
	npx doctoc README.md docs --github --maxlevel 3

docs-open:
	python -m http.server --directory docs 8081
	# open http://localhost:8081 in browser

.PHONY: dev-up apps-up dev-down obs-up logs

# ==== Dev targets (idempotent) ====
dev-up:
        @bash scripts/dev_up.sh

apps-up: dev-up

dev-down:
        @pkill -f "uvicorn" 2>/dev/null || true
        @pkill -f "next dev" 2>/dev/null || true

obs-up:
	docker compose --profile observability up -d
logs:
	docker compose logs -f --tail=200
