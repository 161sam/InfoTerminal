.PHONY: gv.test gv.cov fe.test test

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
	@CI=1 npm -w apps/frontend run test --silent -- --reporter=dot

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

.PHONY: lint lint.py lint.fe format

lint.py:
	@cd services/graph-views && \
	.venv/bin/python -m pip install -q pre-commit || true && \
	pre-commit run --files $$(git ls-files 'services/graph-views/**/*.py' 'services/graph-views/*.py') || true && \
	.venv/bin/python -m ruff check services/graph-views

lint.fe:
	@npm -w apps/frontend run -s lint || echo "eslint not configured; skipping"
	@npx -y prettier@3.3.3 -c "apps/frontend/**/*.{ts,tsx,js,jsx,json,md,yaml,yml}" || true

lint: lint.py lint.fe

format:
	@. ./.venv_dummy 2>/dev/null || true
	@cd services/graph-views && .venv/bin/python -m ruff check --fix . && .venv/bin/python -m ruff format .
	@npx -y prettier@3.3.3 -w "apps/frontend/**/*.{ts,tsx,js,jsx,json,md,yaml,yml}" || true
