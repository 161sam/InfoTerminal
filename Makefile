SHELL := /bin/bash
KIND_CLUSTER := infoterminal
K8S_CONTEXT := kind-$(KIND_CLUSTER)

.PHONY: dev-up dev-down apps-up apps-down seed-demo seed-graph print-info auth-up opa-up neo4j-up opa-test aleph-workers-up nifi-registry-up dbt-run etl-dbt-build etl-nifi-deploy etl-airflow-up etl-airflow-dag etl-superset-warmup

auth-up:
	@bash infra/scripts/keycloak-import.sh

opa-up:
	kubectl apply -f infra/k8s/opa/opa.yaml

neo4j-up:
	kubectl apply -f infra/k8s/neo4j/neo4j.yaml

dev-up: ## (Erweitert) nach helmfile apply auch OPA & Neo4j
	@echo "→ Kind cluster"
	@kind get clusters | grep -q $(KIND_CLUSTER) || kind create cluster --name $(KIND_CLUSTER) --config infra/kind/kind.yaml
	@echo "→ Helm repos"
	@helm repo add bitnami https://charts.bitnami.com/bitnami >/dev/null
	@helm repo add opensearch https://opensearch-project.github.io/helm-charts/ >/dev/null
	@helm repo add traefik https://traefik.github.io/charts >/dev/null
	@helm repo update >/dev/null
	@echo "→ Helmfile apply"
	@helmfile -f infra/helmfile/helmfile.yaml apply
	@echo "→ Deploy OPA & Neo4j (manifests)"
	@kubectl apply -f infra/k8s/opa/opa.yaml
	@kubectl apply -f infra/k8s/neo4j/neo4j.yaml

dev-down:
	@helmfile -f infra/helmfile/helmfile.yaml destroy || true
	@kind delete cluster --name $(KIND_CLUSTER) || true

apps-up:
       @uv run --python 3.11 -q --directory services/search-api ./dev.sh &
       @uv run --python 3.11 -q --directory services/graph-api ./dev.sh &
       @uv run --python 3.11 -q --directory services/entity-resolution ./dev.sh &
       @uv run --python 3.11 -q --directory services/graph-views ./dev.sh &
       @uv run --python 3.11 -q --directory services/nlp ./dev.sh &
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
