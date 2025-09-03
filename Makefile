SHELL := /bin/bash
KIND_CLUSTER := infoterminal
K8S_CONTEXT := kind-$(KIND_CLUSTER)

.PHONY: dev-up dev-down apps-up apps-down seed-demo seed-graph print-info auth-up opa-up neo4j-up opa-test aleph-workers-up nifi-registry-up dbt-run etl-dbt-build etl-nifi-deploy etl-airflow-up etl-airflow-dag etl-superset-warmup nifi-template-import nifi-template-instantiate nifi-start nifi-stop

auth-up:
	@bash infra/scripts/keycloak-import.sh

opa-up:
	kubectl apply -f infra/k8s/opa/opa.yaml

neo4j-up:
	kubectl apply -f infra/k8s/neo4j/neo4j.yaml
apps-up:
	@uv run --python 3.11 -q --directory services/search-api ./dev.sh &
	@uv run --python 3.11 -q --directory services/graph-api ./dev.sh &
	@uv run --python 3.11 -q --directory services/entity-resolution ./dev.sh &
	@uv run --python 3.11 -q --directory services/graph-views ./dev.sh &
	@uv run --python 3.11 -q --directory services/nlp-service uvicorn app:app --host 0.0.0.0 --port 8405 &
	@uv run --python 3.11 -q --directory services/doc-entities ./dev.sh &
	@pnpm --dir apps/frontend dev &

apps-down:
	@pkill -f "uv run" || true
	@pkill -f "next" || true

seed-demo:
	@bash infra/scripts/seed-demo.sh

seed-graph:
	@python3 infra/scripts/seed-neo4j.py

print-info:
	@echo "Kubernetes context: $(K8S_CONTEXT)"
	@kubectl --context $(K8S_CONTEXT) get pods -A



opa-test:
	@docker run --rm -v $(PWD)/infra/k8s/opa:/pol -w /pol openpolicyagent/opa:0.64.0 test -v .

opa-bundle:
	@docker run --rm -v $(PWD)/infra/k8s/opa/policies:/pol -v $(PWD)/infra/k8s/opa/bundle:/out openpolicyagent/opa:0.64.0 build -b /pol -o /out/policy-bundle.tar.gz

bundle-server-up:
	kubectl -n policy delete configmap opa-bundle --ignore-not-found
	kubectl -n policy create configmap opa-bundle --from-file=policy-bundle.tar.gz=infra/k8s/opa/bundle/policy-bundle.tar.gz
	kubectl apply -f infra/k8s/opa/bundle-server.yaml

aleph-workers-up:
	kubectl apply -f infra/k8s/aleph/aleph-workers.yaml

nifi-registry-up:
	kubectl apply -f infra/k8s/nifi/registry.yaml
	bash infra/nifi/scripts/connect-registry.sh

dbt-run:
	cd etl/dbt && dbt deps && dbt seed && dbt run && dbt test

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

.PHONY: dev-up dev-down obs-up logs

dev-up:
	docker compose up -d

dev-down:
	docker compose down -v

obs-up:
	docker compose --profile observability up -d
logs:
	docker compose logs -f --tail=200
