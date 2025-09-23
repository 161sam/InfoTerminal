.PHONY: gv.test gv.cov fe.test fe.dev fe.build test

# Build stabilization helpers
.PHONY: bs.ts-audit bs.validate bs.final

bs.ts-audit:
	@bash build-stabilization/typescript_audit.sh

bs.validate:
	@bash build-stabilization/build_validation.sh

bs.final:
	@bash build-stabilization/final_validation.sh

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

.PHONY: docs.analyze docs.consolidate docs.dedupe docs.all

docs.analyze:
	python3 scripts/docs_pipeline.py analyze

docs.consolidate:
	python3 scripts/docs_pipeline.py consolidate

docs.dedupe:
	python3 scripts/docs_pipeline.py dedupe

docs.all:
	python3 scripts/docs_pipeline.py analyze consolidate dedupe

.PHONY: kc.import kc.import.dry sso.smoke

# Import/Update Keycloak realm via kcadm (in Docker). Idempotent.
kc.import:
	bash scripts/keycloak_kcadm_import.sh

# Dry-run: print commands only
kc.import.dry:
	DRY_RUN=1 bash scripts/keycloak_kcadm_import.sh

# Smoke test oauth2-proxy SSO in front of Superset/Airflow
sso.smoke:
	bash scripts/sso_smoke.sh

.PHONY: rag.seed
rag.seed:
	bash scripts/seed_rag_laws.sh

# =============================================================================
# InfoTerminal v1.0.0 - Comprehensive Test Suite
# =============================================================================

# Test infrastructure validation
.PHONY: test.validate test.health
test.validate:
	@echo "🔍 Validating test infrastructure health..."
	@chmod +x tests/validate_test_health.sh
	@./tests/validate_test_health.sh

test.health: test.validate

# Test data management
.PHONY: test.data.init test.data.seed test.data.cleanup test.data.validate
test.data.init:
	@echo "📊 Initializing test data..."
	@chmod +x tests/data/test_data_pipeline.sh
	@cd tests/data && ./test_data_pipeline.sh init

test.data.seed:
	@echo "🌱 Seeding test databases..."
	@chmod +x tests/data/test_data_pipeline.sh
	@cd tests/data && ./test_data_pipeline.sh seed

test.data.cleanup:
	@echo "🧹 Cleaning up test data..."
	@chmod +x tests/data/test_data_pipeline.sh
	@cd tests/data && ./test_data_pipeline.sh cleanup

test.data.validate:
	@echo "✅ Validating test data integrity..."
	@chmod +x tests/data/test_data_pipeline.sh
	@cd tests/data && ./test_data_pipeline.sh validate

# Unit tests (existing + enhanced)
.PHONY: test.unit test.unit.backend test.unit.frontend test.unit.all
test.unit.backend: gv.test

test.unit.frontend: fe.test

test.unit.all: test.unit.backend test.unit.frontend

test.unit: test.unit.all

# Integration tests
.PHONY: test.integration test.integration.workflows test.integration.nlp
test.integration.workflows:
	@echo "🔗 Running workflow integration tests..."
	@chmod +x tests/integration/integration_workflow_tests.sh
	@./tests/integration/integration_workflow_tests.sh

test.integration.nlp:
	@echo "🧠 Running NLP integration tests..."
	@python -m pytest tests/test_doc_entities_integration.py -v

test.integration: test.integration.workflows test.integration.nlp

# Performance tests
.PHONY: test.performance test.benchmark test.load test.perf.all
test.benchmark:
	@echo "⚡ Running performance benchmarks..."
	@chmod +x tests/performance/benchmark_core_workflows.sh
	@./tests/performance/benchmark_core_workflows.sh

test.load:
	@echo "🚀 Running load tests..."
	@chmod +x tests/performance/load_testing.sh
	@./tests/performance/load_testing.sh

test.perf.all: test.benchmark test.load

test.performance: test.perf.all

# Chaos engineering tests
.PHONY: test.chaos test.resilience
test.chaos:
	@echo "🔥 Running chaos engineering tests..."
	@chmod +x tests/chaos/chaos_engineering_tests.sh
	@./tests/chaos/chaos_engineering_tests.sh

test.resilience: test.chaos

# End-to-end tests
.PHONY: test.e2e test.e2e.comprehensive test.e2e.user
test.e2e.comprehensive:
	@echo "🌐 Running comprehensive E2E tests..."
	@chmod +x test_infoterminal_v020_e2e.sh
	@./test_infoterminal_v020_e2e.sh

test.e2e.user:
	@echo "👤 Running user scenario tests..."
	@find tests/user-testing -name '*.py' -exec python {} \;

test.e2e: test.e2e.comprehensive test.e2e.user

# Regression testing
.PHONY: test.regression test.regression.run test.regression.baseline
test.regression.run:
	@echo "🔍 Running regression analysis..."
	@chmod +x tests/regression_test_suite.sh
	@./tests/regression_test_suite.sh run

test.regression.baseline:
	@echo "📊 Updating performance baselines..."
	@chmod +x tests/regression_test_suite.sh
	@./tests/regression_test_suite.sh update-baselines

test.regression: test.regression.run

# Master test execution
.PHONY: test.all test.fast test.production test.ci
test.all:
	@echo "🚀 Running complete test suite..."
	@chmod +x tests/run_all_tests.sh
	@./tests/run_all_tests.sh

test.fast:
	@echo "⚡ Running fast test suite..."
	@chmod +x tests/run_all_tests.sh
	@./tests/run_all_tests.sh --fast

test.production:
	@echo "🏭 Running production-ready test suite..."
	@chmod +x tests/run_all_tests.sh
	@IT_RUN_CHAOS=true ./tests/run_all_tests.sh

test.ci: test.validate test.unit test.integration

# Test categories for selective execution
.PHONY: test.unit-only test.integration-only test.performance-only test.chaos-only test.e2e-only
test.unit-only:
	@chmod +x tests/run_all_tests.sh
	@./tests/run_all_tests.sh --unit-only

test.integration-only:
	@chmod +x tests/run_all_tests.sh
	@./tests/run_all_tests.sh --integration-only

test.performance-only:
	@chmod +x tests/run_all_tests.sh
	@./tests/run_all_tests.sh --performance-only

test.chaos-only:
	@chmod +x tests/run_all_tests.sh
	@./tests/run_all_tests.sh --chaos-only

test.e2e-only:
	@chmod +x tests/run_all_tests.sh
	@./tests/run_all_tests.sh --e2e-only

# Test results and reporting
.PHONY: test.results test.report test.clean
test.results:
	@echo "📊 Displaying latest test results..."
	@find tests/results -name "*.log" -o -name "*.json" -o -name "*.md" | sort -r | head -10

test.report:
	@echo "📄 Generating test summary report..."
	@if [ -f tests/results/master_test_*.json ]; then \
		echo "Latest master test results:"; \
		jq '.summary' $(ls -t tests/results/master_test_*.json | head -1); \
	else \
		echo "No test results found. Run 'make test.all' first."; \
	fi

test.clean:
	@echo "🧹 Cleaning test artifacts..."
	@rm -rf tests/results/* || true
	@rm -rf tests/*/results/* || true
	@rm -rf tests/data/temp/* || true
	@echo "Test artifacts cleaned"

# Development helpers
.PHONY: test.setup test.deps test.env
test.setup: test.deps test.data.init test.validate
	@echo "✅ Test environment setup complete"

test.deps:
	@echo "📦 Installing test dependencies..."
	@command -v jq >/dev/null || (echo "Installing jq..." && sudo apt-get update && sudo apt-get install -y jq)
	@command -v bc >/dev/null || (echo "Installing bc..." && sudo apt-get install -y bc)
	@command -v timeout >/dev/null || echo "timeout command available"
	@command -v python3 >/dev/null && python3 -m pip install -r tests/requirements.txt >/dev/null 2>&1 || true
	@echo "Dependencies verified"

test.env:
	@echo "🔧 Test environment configuration:"
	@echo "  Frontend URL: ${IT_FRONTEND_URL:-http://localhost:3000}"
	@echo "  Graph API URL: ${IT_GRAPH_API_URL:-http://localhost:8403}"
	@echo "  Load Users: ${IT_LOAD_USERS:-100}"
	@echo "  Test Duration: ${IT_TEST_DURATION:-120}s"

# Quick test commands for development
.PHONY: test.quick test.smoke test.dev
test.quick: test.unit test.integration.workflows
	@echo "⚡ Quick development tests completed"

test.smoke:
	@echo "💨 Running smoke tests..."
	@$(MAKE) test.validate
	@$(MAKE) test.unit.backend
	@echo "💨 Smoke tests completed"

test.dev: test.smoke
	@echo "👨‍💻 Development test suite completed"

# Legacy compatibility
.PHONY: gv.test fe.test test
# (existing targets remain unchanged)

# Help target
.PHONY: test.help
test.help:
	@echo "InfoTerminal v1.0.0 Test Suite Commands:"
	@echo ""
	@echo "🏗️  Setup & Validation:"
	@echo "  make test.setup          - Complete test environment setup"
	@echo "  make test.validate       - Validate test infrastructure"
	@echo "  make test.deps          - Install test dependencies"
	@echo ""
	@echo "📊 Test Data Management:"
	@echo "  make test.data.init     - Initialize test data"
	@echo "  make test.data.seed     - Seed test databases"
	@echo "  make test.data.cleanup  - Clean test data"
	@echo ""
	@echo "🧪 Test Categories:"
	@echo "  make test.unit          - Unit tests (backend + frontend)"
	@echo "  make test.integration   - Integration workflow tests"
	@echo "  make test.performance   - Performance benchmarks + load tests"
	@echo "  make test.chaos         - Chaos engineering tests"
	@echo "  make test.e2e          - End-to-end tests"
	@echo "  make test.regression    - Regression analysis"
	@echo ""
	@echo "🚀 Master Test Execution:"
	@echo "  make test.all          - Complete comprehensive test suite"
	@echo "  make test.fast         - Fast test execution (reduced scope)"
	@echo "  make test.production   - Production-ready tests (includes chaos)"
	@echo "  make test.ci           - CI pipeline tests"
	@echo ""
	@echo "⚡ Quick Commands:"
	@echo "  make test.quick        - Unit + integration workflows"
	@echo "  make test.smoke        - Basic health check"
	@echo "  make test.dev          - Development test suite"
	@echo ""
	@echo "📈 Results & Reporting:"
	@echo "  make test.results      - Show recent test results"
	@echo "  make test.report       - Generate test summary"
	@echo "  make test.clean        - Clean test artifacts"
	@echo ""
	@echo "🎯 Selective Execution:"
	@echo "  make test.unit-only    - Only unit tests"
	@echo "  make test.integration-only - Only integration tests"
	@echo "  make test.performance-only - Only performance tests"
	@echo "  make test.chaos-only   - Only chaos engineering"
	@echo "  make test.e2e-only     - Only end-to-end tests"
	@echo ""
	@echo "💡 Environment Variables:"
	@echo "  IT_FRONTEND_URL        - Frontend service URL"
	@echo "  IT_GRAPH_API_URL       - Graph API service URL"
	@echo "  IT_LOAD_USERS          - Load test concurrent users"
	@echo "  IT_TEST_DURATION       - Load test duration (seconds)"
	@echo "  IT_RUN_CHAOS           - Enable chaos tests (true/false)"
	@echo ""
	@echo "📖 For detailed documentation, see: tests/README.md"
