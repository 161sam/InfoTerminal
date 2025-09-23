# InfoTerminal v1.0.0 - Comprehensive Test Suite

🚀 **Production-Ready Testing Infrastructure for Enterprise OSINT Platform**

## Overview

This comprehensive test suite validates InfoTerminal's readiness for v1.0.0 production deployment through multi-layered testing including unit tests, integration workflows, performance benchmarks, chaos engineering, and end-to-end validation.

## 🎯 Test Coverage

### Core Test Categories

| Category | Purpose | Files | Coverage |
|----------|---------|-------|-----------|
| **Unit Tests** | Component-level validation | `Makefile`, existing test files | 95%+ code coverage |
| **Integration Tests** | Workflow data flows | `integration/integration_workflow_tests.sh` | 5 core workflows |
| **Performance Tests** | Benchmarks & load testing | `performance/benchmark_core_workflows.sh`, `performance/load_testing.sh` | P95 < 200ms APIs |
| **Chaos Engineering** | Resilience & recovery | `chaos/chaos_engineering_tests.sh` | Service failure scenarios |
| **E2E Tests** | Complete user scenarios | `test_infoterminal_v020_e2e.sh` | End-to-end workflows |
| **Regression Tests** | Change impact analysis | `regression_test_suite.sh` | Performance & API stability |

## 🏗️ Quick Start

### 1. Setup Test Environment

```bash
# Complete setup with dependencies and data
make test.setup

# Or step by step:
make test.deps           # Install system + Python test dependencies
make test.data.init      # Initialize test data
make test.validate       # Validate infrastructure
```

Python test dependencies are tracked in `tests/requirements.txt` (e.g. `httpx`, `numpy`, `typer`).

### 2. Run Test Categories

```bash
# Development workflow
make test.quick          # Unit + integration workflows (fast)
make test.smoke          # Basic health check

# Full test categories
make test.unit           # All unit tests
make test.integration    # Workflow integration tests
make test.performance    # Performance benchmarks + load tests
make test.chaos          # Chaos engineering (requires --enable)
make test.e2e           # End-to-end user scenarios

# Master execution
make test.all           # Complete comprehensive test suite
make test.production    # Production-ready (includes chaos)
make test.fast          # Fast execution mode
```

### 3. View Results

```bash
make test.results       # Show recent test results
make test.report        # Generate summary report
make test.clean         # Clean test artifacts
```

## 📊 Test Architecture

### Workflow Coverage

The test suite validates these core InfoTerminal workflows:

1. **Search Workflow**: Text Search → Ranking → Results → Export
2. **Graph Workflow**: Entity Creation → Relationship Building → Analytics → Visualization  
3. **NLP Workflow**: Document Ingestion → NER → Entity Resolution → Knowledge Graph Integration
4. **Verification Workflow**: Claim Extraction → Evidence Retrieval → Stance Classification → Credibility Scoring
5. **Security Workflow**: Incognito Mode → Secure Browsing → Data Wipe → Session Management

### Performance Targets

| Metric | Target | Test Coverage |
|--------|--------|---------------|
| API Response Time (P95) | < 200ms | ✅ All endpoints |
| Search Queries (P95) | < 500ms | ✅ Full-text search |
| Graph Queries (P95) | < 1000ms | ✅ Neo4j operations |
| NLP Processing (P95) | < 2000ms | ✅ Entity extraction |
| Throughput | > 100 RPS | ✅ Load testing |
| Error Rate | < 1% | ✅ All services |
| Service Recovery | < 30s | ✅ Chaos engineering |

## 🔧 Configuration

### Environment Variables

```bash
# Service URLs
export IT_FRONTEND_URL="http://localhost:3000"
export IT_GRAPH_API_URL="http://localhost:8403"
export IT_SEARCH_API_URL="http://localhost:8401"
export IT_DOC_ENTITIES_URL="http://localhost:8402"
export IT_VERIFICATION_URL="http://localhost:8617"
export IT_OPS_CONTROLLER_URL="http://localhost:8618"

# Database Connections
export IT_NEO4J_URI="bolt://localhost:7687"
export IT_NEO4J_USER="neo4j"
export IT_NEO4J_PASSWORD="testpassword"
export IT_OPENSEARCH_URL="http://localhost:9200"
export IT_POSTGRES_URL="postgresql://test:testpass@localhost:5432/infoterminal_test"

# Test Configuration
export IT_LOAD_USERS="100"           # Concurrent users for load testing
export IT_TEST_DURATION="120"        # Load test duration (seconds)
export IT_RUN_CHAOS="false"          # Enable chaos engineering tests
export IT_RUN_PERFORMANCE="true"     # Enable performance tests
export IT_BASELINE_COMMIT="HEAD~1"   # Baseline for regression testing
```

### Test Data Management

```bash
# Initialize test data (realistic OSINT datasets)
make test.data.init

# Seed databases with test data
make test.data.seed

# Validate data integrity
make test.data.validate

# Clean up test data
make test.data.cleanup
```

## 📈 Performance Monitoring

### Grafana Dashboard

The test suite includes a comprehensive performance dashboard:

```bash
# Import dashboard
curl -X POST http://admin:admin@localhost:3001/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @monitoring/dashboards/performance-dashboard.json
```

Dashboard includes:
- API Response Times (P95, P99)
- Request Throughput (RPS)
- Error Rates
- System Resources (CPU, Memory)
- Service Availability
- Real-time Test Results

### Prometheus Alerts

Performance alerts are configured in `monitoring/alerts/performance-alerts.yml`:

- High API Response Time (> 200ms)
- Critical Response Time (> 1s)
- High Error Rate (> 5%)
- Service Down
- Resource Usage (CPU > 80%, Memory > 85%)
- Database Connection Failures

## 🔥 Chaos Engineering

Chaos engineering tests validate system resilience:

```bash
# Enable and run chaos tests
IT_RUN_CHAOS=true make test.chaos

# Or specifically:
make test.chaos-only
```

**Chaos Scenarios**:
- Service failure recovery
- Database connection loss
- Network partition handling
- High load degradation
- Cascade failure prevention

**Recovery Targets**:
- Service recovery: < 30 seconds
- Database reconnection: < 45 seconds
- Graceful degradation under load
- No cascade failures

## 🔄 CI/CD Integration

### GitHub Actions

The enhanced CI/CD pipeline (`/.github/workflows/integration-performance.yml`) includes:

- **Parallel Test Execution**: Unit, integration, performance tests run concurrently
- **Quality Gates**: Performance regression detection, API breaking change analysis
- **Artifact Management**: Test results, performance reports, Docker images
- **Conditional Execution**: Chaos tests on main branch, performance tests on schedule
- **PR Comments**: Automated performance feedback on pull requests

### Pipeline Stages

1. **Pre-flight Checks**: Validate test requirements
2. **Build Services**: Parallel Docker image builds
3. **Integration Tests**: Workflow validation by category
4. **Performance Tests**: Benchmarks and load testing
5. **Chaos Tests**: Resilience validation (main branch only)
6. **Quality Gates**: Regression analysis and reporting

### Quality Gates

| Gate | Threshold | Action |
|------|-----------|--------|
| Unit Test Coverage | > 90% | Block deployment |
| Integration Success Rate | > 95% | Block deployment |
| Performance Regression | > 20% | Block deployment |
| API Breaking Changes | Any | Block deployment |
| Chaos Test Success Rate | > 80% | Warning |

## 📋 Test Commands Reference

### Setup & Validation
```bash
make test.setup          # Complete environment setup
make test.validate       # Infrastructure health check
make test.deps          # Install dependencies
make test.env           # Show environment configuration
```

### Test Data
```bash
make test.data.init     # Initialize test datasets
make test.data.seed     # Seed databases
make test.data.cleanup  # Clean test data
make test.data.validate # Validate data integrity
```

### Test Categories
```bash
make test.unit          # Unit tests (backend + frontend)
make test.integration   # Integration workflow tests
make test.performance   # Performance benchmarks + load tests
make test.chaos         # Chaos engineering tests
make test.e2e          # End-to-end tests
make test.regression    # Regression analysis
```

### Master Execution
```bash
make test.all          # Complete comprehensive suite
make test.fast         # Fast execution (reduced scope)
make test.production   # Production-ready (includes chaos)
make test.ci           # CI pipeline tests
```

### Selective Testing
```bash
make test.unit-only    # Only unit tests
make test.integration-only # Only integration tests
make test.performance-only # Only performance tests
make test.chaos-only   # Only chaos engineering
make test.e2e-only     # Only end-to-end tests
```

### Development Helpers
```bash
make test.quick        # Fast development validation
make test.smoke        # Basic health check
make test.dev          # Development test suite
```

### Results & Reporting
```bash
make test.results      # Show recent test results
make test.report       # Generate test summary
make test.clean        # Clean test artifacts
make test.help         # Show all commands
```

## 🗂️ File Structure

```
tests/
├── run_all_tests.sh                 # Master test orchestrator
├── validate_test_health.sh          # Infrastructure validation
├── regression_test_suite.sh         # Regression testing
├── data/
│   ├── test_data_pipeline.sh       # Test data management
│   ├── seeds/                       # Realistic test datasets
│   │   ├── entities.json           # Graph entities
│   │   ├── documents.json          # NLP documents
│   │   ├── claims.json             # Verification claims
│   │   └── search_data.json        # Search index data
│   └── fixtures/                    # Test fixtures
├── integration/
│   └── integration_workflow_tests.sh # Workflow integration tests
├── performance/
│   ├── benchmark_core_workflows.sh  # Performance benchmarks
│   └── load_testing.sh             # Concurrent load testing
├── chaos/
│   └── chaos_engineering_tests.sh   # Chaos engineering tests
├── results/                         # Test execution results
└── README.md                        # This documentation

monitoring/
├── dashboards/
│   └── performance-dashboard.json   # Grafana dashboard
└── alerts/
    └── performance-alerts.yml       # Prometheus alerts

.github/workflows/
└── integration-performance.yml      # Enhanced CI/CD pipeline
```

## 🎯 Success Criteria for v1.0.0

### Test Quality Gates

- **✅ Unit Test Coverage**: > 95% across all components
- **✅ Integration Success Rate**: > 95% for all core workflows
- **✅ Performance Targets**: All APIs < 200ms P95, search < 500ms P95
- **✅ Load Testing**: Handle 100+ concurrent users
- **✅ Chaos Resilience**: < 30s recovery time for service failures
- **✅ Zero Regressions**: No performance or functionality degradation
- **✅ API Stability**: No breaking changes without versioning

### Deployment Readiness

The system is considered **production-ready** when:

1. All test categories pass with target thresholds
2. No critical performance regressions detected
3. Chaos engineering tests validate resilience
4. Monitoring and alerting systems operational
5. CI/CD pipeline validates all changes automatically

### Monitoring in Production

Post-deployment monitoring includes:
- Real-time performance dashboards
- Automated alerting on SLA violations
- Daily performance regression checks
- Weekly chaos engineering validation
- Monthly baseline updates

## 🛠️ Troubleshooting

### Common Issues

**Services Not Available**
```bash
# Check service status
make test.validate

# Start services
docker-compose up -d

# Check specific service
curl http://localhost:3000/api/health
```

**Test Data Issues**
```bash
# Reinitialize test data
make test.data.cleanup
make test.data.init

# Validate data integrity
make test.data.validate
```

**Performance Test Failures**
```bash
# Check system resources
htop
df -h

# Run minimal load test
IT_LOAD_USERS=10 IT_TEST_DURATION=30 make test.load
```

**Dependencies Missing**
```bash
# Install required dependencies
make test.deps

# Manual installation
sudo apt-get update
sudo apt-get install -y jq bc curl
```

### Getting Help

```bash
# Show all available commands
make test.help

# Validate test infrastructure
make test.validate

# Run smoke test for quick validation
make test.smoke
```

## 📚 Additional Resources

- **Build Stabilization**: [build-stabilization/README.md](../build-stabilization/README.md)
- **Service Documentation**: [docs/](../docs/)
- **Performance Baselines**: [tests/performance/results/](./performance/results/)
- **Monitoring Setup**: [monitoring/README.md](../monitoring/README.md)
- **CI/CD Documentation**: [.github/workflows/README.md](../.github/workflows/README.md)

---

**InfoTerminal v1.0.0 Test Suite** - Enterprise-grade validation for production OSINT platform
