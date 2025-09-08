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
	@npm -w apps/frontend run test --silent -- --reporter=dot

test:
	@$(MAKE) gv.test
	@$(MAKE) fe.test
