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
