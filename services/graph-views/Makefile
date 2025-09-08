test:
	pytest -q

cov:
	pytest --cov=services/graph-views --cov-report=term-missing

lint:
	@which ruff >/dev/null 2>&1 && ruff . || echo "ruff not installed"
