SHELL := /bin/bash
KIND_CLUSTER := infoterminal
K8S_CONTEXT := kind-$(KIND_CLUSTER)

.PHONY: dev-up dev-down apps-up apps-down seed-demo seed-graph print-info auth-up opa-up neo4j-up opa-test

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
