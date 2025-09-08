.PHONY: gv.test gv.cov

gv.test:
@PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH="$(PWD)/services/graph-views" \
services/graph-views/.venv/bin/pytest -q -c services/graph-views/pytest.ini

gv.cov:
@PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH="$(PWD)/services/graph-views" \
services/graph-views/.venv/bin/pytest -c services/graph-views/pytest.ini \
-p pytest_cov --cov="services/graph-views" --cov-report=term-missing -q
