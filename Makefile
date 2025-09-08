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
	@CI=1 npm -w apps/frontend run test --silent -- --reporter=dot --threads=false

test:
	@set -e; \
	$(MAKE) gv.test || gv=$$?; \
	CI=1 npm -w apps/frontend run test --silent -- --reporter=dot --threads=false || fe=$$?; \
	if [ -n "$$gv" ] || [ -n "$$fe" ]; then \
	  echo "Summary: gv=$${gv:-0} fe=$${fe:-0}"; \
	  exit $${gv:-$$fe}; \
	fi

.PHONY: smoke.gv
smoke.gv:
	@scripts/smoke_graph_views.sh
