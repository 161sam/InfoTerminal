SHELL := /bin/bash
KIND_CLUSTER := infoterminal
K8S_CONTEXT := kind-$(KIND_CLUSTER)

.PHONY: dev-up dev-down apps-up apps-down seed-demo print-info

dev-up:
	@echo "→ Kind cluster"
	@kind get clusters | grep -q $(KIND_CLUSTER) || kind create cluster --name $(KIND_CLUSTER) --config infra/kind/kind.yaml
	@echo "→ Helm repos"
	@helm repo add bitnami https://charts.bitnami.com/bitnami >/dev/null
	@helm repo add opensearch https://opensearch-project.github.io/helm-charts/ >/dev/null
	@helm repo add traefik https://traefik.github.io/charts >/dev/null
	@helm repo update >/dev/null
	@echo "→ Helmfile apply"
	@helmfile -f infra/helmfile/helmfile.yaml apply

dev-down:
	@helmfile -f infra/helmfile/helmfile.yaml destroy || true
	@kind delete cluster --name $(KIND_CLUSTER) || true

apps-up:
	@uv run --python 3.11 -q --directory services/search-api ./dev.sh &
	@pnpm --dir apps/frontend dev &

apps-down:
	@pkill -f "uv run" || true
	@pkill -f "next" || true

seed-demo:
	@bash infra/scripts/seed-demo.sh

print-info:
	@echo "Kubernetes context: $(K8S_CONTEXT)"
	@kubectl --context $(K8S_CONTEXT) get pods -A
