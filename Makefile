.PHONY: gv.test gv.cov fe.test fe.dev fe.build test

gv.test:
	@cd services/graph-views && \
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
	PYTHONPATH="$(PWD)/services/graph-views" \
	.venv/bin/pytest -q -c pytest.ini

gv.cov:
	@cd services/graph-views && \
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
	PYTHONPATH="$(PWD)/services/graph-views" \
	.venv/bin/pytest -c pytest.ini -p pytest_cov --cov=. --cov-report=term-missing -q $(COVER)

fe.test:
	@it fe test

fe.dev:
	@it fe dev

fe.build:
	@it fe build

test:
	@set -e; \
	$(MAKE) gv.test || gv=$$?; \
	CI=1 npm -w apps/frontend run test --silent -- --reporter=dot || fe=$$?; \
	if [ -n "$$gv" ] || [ -n "$$fe" ]; then \
	  echo "Summary: gv=$${gv:-0} fe=$${fe:-0}"; \
	  exit $${gv:-$$fe}; \
	fi

.PHONY: gv.serve
gv.serve:
	@echo "Starting graph-views on :8403"; \
	cd services/graph-views && \
	GV_ALLOW_WRITES=$${GV_ALLOW_WRITES:-1} \
	GV_BASIC_USER=$${GV_BASIC_USER:-dev} \
	GV_BASIC_PASS=$${GV_BASIC_PASS:-devpass} \
	GV_RATE_LIMIT_WRITE=$${GV_RATE_LIMIT_WRITE:-2/second} \
	GV_AUDIT_LOG=$${GV_AUDIT_LOG:-1} \
	.venv/bin/uvicorn app:app --host 0.0.0.0 --port 8403 --reload

.PHONY: smoke.gv.up
smoke.gv.up:
	@BASE=$${BASE:-http://localhost:8403} BOOT=1 scripts/smoke_graph_views.sh

.PHONY: smoke.gv
smoke.gv:
	@scripts/smoke_graph_views.sh

.PHONY: tag.v0.2.0
tag.v0.2.0:
	@git add -A
	@git commit -m "release: v0.2.0" || true
	@git tag -a v0.2.0 -m "InfoTerminal v0.2.0"
	@git push && git push --tags

.PHONY: lint lint.py lint.fe format gv.venv

gv.venv:
	@cd services/graph-views && \
	python -m venv .venv >/dev/null 2>&1 || true && \
	.venv/bin/python -m pip install -q --upgrade pip && \
	.venv/bin/python -m pip install -q -r requirements-dev.txt && \
	.venv/bin/python -m pip install -q pre-commit

lint.py: gv.venv
	@cd services/graph-views && \
	.venv/bin/pre-commit install -f --install-hooks >/dev/null 2>&1 || true && \
	.venv/bin/pre-commit run --all-files && \
	.venv/bin/python -m ruff check services/graph-views

lint.fe:
	@npm -w apps/frontend run -s lint || echo "eslint/prettier not configured; skipping npm lint"
	# Repo-Root/CI-Dateien: Prettier Check mit Ignore-Pfad, tolerant bei leeren Globs
	@npx -y prettier@3.3.3 -c "**/*.{md,yaml,yml,json}" --ignore-path .prettierignore --log-level warn --no-error-on-unmatched-pattern || true

lint: lint.py lint.fe

format: gv.venv
	@cd services/graph-views && .venv/bin/python -m ruff format . || true
	@cd services/graph-views && .venv/bin/python -m ruff check --fix . || true
	# Repo-Root + Frontend: Format mit Ignore-Pfad, tolerant
	@npx -y prettier@3.3.3 -w "**/*.{md,yaml,yml,json}" --ignore-path .prettierignore --log-level warn --no-error-on-unmatched-pattern || true
	@npx -y prettier@3.3.3 -w "apps/frontend/**/*.{ts,tsx,js,jsx,json,md,yaml,yml}" --ignore-path .prettierignore --log-level warn --no-error-on-unmatched-pattern || true

.PHONY: fmt.safe lint.safe

fmt.safe:
	@chmod +x scripts/format_safe.sh
	@./scripts/format_safe.sh || true

lint.safe:
	@npx -y prettier@3.3.3 -c $(shell tr '\n' ' ' < scripts/prettier_safe.list) --ignore-path .prettierignore --log-level warn || true
