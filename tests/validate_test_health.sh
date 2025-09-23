#!/bin/bash

# validate_test_health.sh
# InfoTerminal v1.0.0 - Test Infrastructure Health Validation
# Validates: Test Scripts, Dependencies, Services, Data

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VALIDATION_LOG="${SCRIPT_DIR}/results/validation_$(date +%Y%m%d_%H%M%S).log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Validation counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Logging functions
log() {
    echo -e "$1" | tee -a "$VALIDATION_LOG"
}

log_check() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    log "${BLUE}[CHECK $TOTAL_CHECKS] $1${NC}"
}

log_pass() {
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
    log "${GREEN}✅ PASS: $1${NC}"
}

log_fail() {
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
    log "${RED}❌ FAIL: $1${NC}"
}

log_warn() {
    WARNING_CHECKS=$((WARNING_CHECKS + 1))
    log "${YELLOW}⚠️  WARN: $1${NC}"
}

log_info() {
    log "${BLUE}ℹ️  $1${NC}"
}

# Initialize validation
init_validation() {
    mkdir -p "$(dirname "$VALIDATION_LOG")"
    log "=================================================================="
    log "${BLUE}InfoTerminal Test Infrastructure Health Validation${NC}"
    log "=================================================================="
    log "Starting validation at $(date)"
    log "Project root: $PROJECT_ROOT"
    log "Validation log: $VALIDATION_LOG"
    log ""
}

# Validate test script existence and permissions
validate_test_scripts() {
    log_check "Test script availability and permissions"
    
    local test_scripts=(
        "tests/run_all_tests.sh"
        "tests/performance/benchmark_core_workflows.sh"
        "tests/integration/integration_workflow_tests.sh"
        "tests/performance/load_testing.sh"
        "tests/chaos/chaos_engineering_tests.sh"
        "tests/data/test_data_pipeline.sh"
        "tests/regression_test_suite.sh"
        "tests/validate_test_health.sh"
        "test_infoterminal_v020_e2e.sh"
    )
    
    local missing_scripts=()
    local non_executable=()
    
    for script in "${test_scripts[@]}"; do
        local full_path="$PROJECT_ROOT/$script"
        if [[ ! -f "$full_path" ]]; then
            missing_scripts+=("$script")
        elif [[ ! -x "$full_path" ]]; then
            # Attempt to auto-fix permissions
            if chmod +x "$full_path" 2>/dev/null; then
                log_info "Fixed executable permission: $script"
            else
                non_executable+=("$script")
            fi
        fi
    done
    
    if [[ ${#missing_scripts[@]} -eq 0 ]] && [[ ${#non_executable[@]} -eq 0 ]]; then
        log_pass "All test scripts present and executable"
    else
        if [[ ${#missing_scripts[@]} -gt 0 ]]; then
            log_fail "Missing test scripts: ${missing_scripts[*]}"
        fi
        if [[ ${#non_executable[@]} -gt 0 ]]; then
            log_fail "Non-executable test scripts: ${non_executable[*]}"
        fi
    fi
}

# Validate system dependencies
validate_dependencies() {
    log_check "System dependencies"
    
    local required_commands=(
        "jq:JSON processing"
        "bc:Mathematical calculations" 
        "curl:HTTP requests"
        "timeout:Command timeouts"
        "docker:Container management"
        "git:Version control"
    )
    
    local missing_deps=()
    local available_deps=()
    
    for dep in "${required_commands[@]}"; do
        local cmd="${dep%%:*}"
        local desc="${dep#*:}"
        
        if command -v "$cmd" >/dev/null 2>&1; then
            available_deps+=("$cmd")
        else
            missing_deps+=("$cmd ($desc)")
        fi
    done
    
    if [[ ${#missing_deps[@]} -eq 0 ]]; then
        log_pass "All required dependencies available (${#available_deps[@]} commands)"
    else
        log_fail "Missing dependencies: ${missing_deps[*]}"
    fi
    
    # Check optional dependencies
    local optional_commands=(
        "cypher-shell:Neo4j testing"
        "psql:PostgreSQL testing"
        "ab:Load testing alternative"
        "locust:Advanced load testing"
    )
    
    local optional_available=()
    for dep in "${optional_commands[@]}"; do
        local cmd="${dep%%:*}"
        if command -v "$cmd" >/dev/null 2>&1; then
            optional_available+=("$cmd")
        fi
    done
    
    if [[ ${#optional_available[@]} -gt 0 ]]; then
        log_info "Optional dependencies available: ${optional_available[*]}"
    fi
}

# Validate Docker environment
validate_docker_environment() {
    log_check "Docker environment"
    
    if ! command -v docker >/dev/null; then
        log_fail "Docker not installed"
        return
    fi
    
    if ! docker info >/dev/null 2>&1; then
        log_fail "Docker daemon not running"
        return
    fi
    
    # Check for InfoTerminal images
    local expected_images=(
        "infoterminal-frontend"
        "infoterminal-graph-views" 
        "infoterminal-doc-entities"
    )
    
    local available_images=()
    local missing_images=()
    
    for image in "${expected_images[@]}"; do
        if docker images --format "table {{.Repository}}" | grep -q "^$image$"; then
            available_images+=("$image")
        else
            missing_images+=("$image")
        fi
    done
    
    if [[ ${#missing_images[@]} -eq 0 ]]; then
        log_pass "All InfoTerminal Docker images available"
    else
        log_warn "Missing Docker images (can be built): ${missing_images[*]}"
    fi
    
    # Check Docker Compose
    if command -v docker-compose >/dev/null || docker compose version >/dev/null 2>&1; then
        log_info "Docker Compose available"
        
        # Check for compose files
        local compose_files=(
            "docker-compose.yml"
            "docker-compose.neo.yml"
            "docker-compose.graph-views.yml"
        )
        
        local available_compose=()
        for compose_file in "${compose_files[@]}"; do
            if [[ -f "$PROJECT_ROOT/$compose_file" ]]; then
                available_compose+=("$compose_file")
            fi
        done
        
        if [[ ${#available_compose[@]} -gt 0 ]]; then
            log_info "Docker Compose files: ${available_compose[*]}"
        fi
    else
        log_warn "Docker Compose not available"
    fi
}

# Validate service availability  
validate_service_availability() {
    log_check "Service availability for testing"
    
    local services=(
        "Frontend:${IT_FRONTEND_URL:-http://localhost:3000}:/api/health"
        "Graph API:${IT_GRAPH_API_URL:-http://localhost:8403}:/health"
        "Search API:${IT_SEARCH_API_URL:-http://localhost:8401}:/health"
        "Doc Entities:${IT_DOC_ENTITIES_URL:-http://localhost:8402}:/health"
        "Verification:${IT_VERIFICATION_URL:-http://localhost:8617}:/health"
        "Ops Controller:${IT_OPS_CONTROLLER_URL:-http://localhost:8618}:/health"
    )
    
    local available_services=()
    local unavailable_services=()
    
    for service in "${services[@]}"; do
        local name="${service%%:*}"
        local url_path="${service#*:}"
        local base_url="${url_path%%:*}"
        local health_path="${url_path#*:}"
        local full_url="$base_url$health_path"
        
        if curl -s --max-time 5 "$full_url" >/dev/null 2>&1 || \
           curl -s --max-time 5 "$base_url" >/dev/null 2>&1; then
            available_services+=("$name")
        else
            unavailable_services+=("$name")
        fi
    done
    
    if [[ ${#available_services[@]} -gt 0 ]]; then
        log_pass "Available services: ${available_services[*]}"
    fi
    
    if [[ ${#unavailable_services[@]} -gt 0 ]]; then
        log_warn "Unavailable services (tests may be limited): ${unavailable_services[*]}"
        log_info "Start services with: docker-compose up -d"
    fi
    
    if [[ ${#available_services[@]} -eq 0 ]]; then
        log_fail "No services available for testing"
    fi
}

# Validate database connectivity
validate_database_connectivity() {
    log_check "Database connectivity"
    
    local databases_tested=0
    local databases_available=0
    
    # Neo4j
    local neo4j_uri="${IT_NEO4J_URI:-bolt://localhost:7687}"
    local neo4j_user="${IT_NEO4J_USER:-neo4j}"
    local neo4j_password="${IT_NEO4J_PASSWORD:-testpassword}"
    
    if command -v cypher-shell >/dev/null; then
        databases_tested=$((databases_tested + 1))
        if cypher-shell -a "$neo4j_uri" -u "$neo4j_user" -p "$neo4j_password" "RETURN 1" >/dev/null 2>&1; then
            databases_available=$((databases_available + 1))
            log_info "✓ Neo4j available at $neo4j_uri"
        else
            log_info "✗ Neo4j not available at $neo4j_uri"
        fi
    fi
    
    # OpenSearch
    local opensearch_url="${IT_OPENSEARCH_URL:-http://localhost:9200}"
    databases_tested=$((databases_tested + 1))
    if curl -s --max-time 5 "$opensearch_url" >/dev/null 2>&1; then
        databases_available=$((databases_available + 1))
        log_info "✓ OpenSearch available at $opensearch_url"
    else
        log_info "✗ OpenSearch not available at $opensearch_url"
    fi
    
    # PostgreSQL
    local postgres_url="${IT_POSTGRES_URL:-postgresql://test:testpass@localhost:5432/infoterminal_test}"
    if command -v psql >/dev/null; then
        databases_tested=$((databases_tested + 1))
        if psql "$postgres_url" -c "SELECT 1" >/dev/null 2>&1; then
            databases_available=$((databases_available + 1))
            log_info "✓ PostgreSQL available"
        else
            log_info "✗ PostgreSQL not available"
        fi
    fi
    
    if [[ $databases_available -eq $databases_tested ]] && [[ $databases_tested -gt 0 ]]; then
        log_pass "All tested databases available ($databases_available/$databases_tested)"
    elif [[ $databases_available -gt 0 ]]; then
        log_warn "Partial database availability ($databases_available/$databases_tested)"
    else
        log_warn "No databases available for testing"
    fi
}

# Validate test data integrity
validate_test_data() {
    log_check "Test data integrity"
    
    local data_dir="$PROJECT_ROOT/tests/data"
    
    if [[ ! -d "$data_dir" ]]; then
        log_fail "Test data directory not found: $data_dir"
        return
    fi
    
    # Check for test data pipeline script
    if [[ -f "$data_dir/test_data_pipeline.sh" ]]; then
        log_info "✓ Test data pipeline available"
        
        # Run data validation
        if cd "$data_dir" && ./test_data_pipeline.sh validate >/dev/null 2>&1; then
            log_pass "Test data validation successful"
        else
            log_warn "Test data validation failed - run './test_data_pipeline.sh init' to regenerate"
        fi
    else
        log_fail "Test data pipeline script not found"
    fi
    
    # Check for seed data files
    local seed_files=(
        "seeds/entities.json"
        "seeds/documents.json" 
        "seeds/claims.json"
        "seeds/search_data.json"
    )
    
    local available_seeds=()
    for seed_file in "${seed_files[@]}"; do
        if [[ -f "$data_dir/$seed_file" ]]; then
            available_seeds+=("$seed_file")
        fi
    done
    
    if [[ ${#available_seeds[@]} -eq ${#seed_files[@]} ]]; then
        log_info "✓ All seed data files present"
    else
        log_warn "Missing seed data files - run test data pipeline init"
    fi
}

# Validate CI/CD configuration
validate_cicd_configuration() {
    log_check "CI/CD pipeline configuration"
    
    local workflow_dir="$PROJECT_ROOT/.github/workflows"
    
    if [[ ! -d "$workflow_dir" ]]; then
        log_fail "GitHub workflows directory not found"
        return
    fi
    
    local workflow_files=(
        "ci.yml:Basic CI pipeline"
        "integration-performance.yml:Integration and performance tests"
        "codeql.yml:Security analysis"
    )
    
    local available_workflows=()
    local missing_workflows=()
    
    for workflow in "${workflow_files[@]}"; do
        local file="${workflow%%:*}"
        local desc="${workflow#*:}"
        
        if [[ -f "$workflow_dir/$file" ]]; then
            available_workflows+=("$file")
        else
            missing_workflows+=("$file ($desc)")
        fi
    done
    
    if [[ ${#available_workflows[@]} -gt 0 ]]; then
        log_pass "GitHub workflows available: ${available_workflows[*]}"
    fi
    
    if [[ ${#missing_workflows[@]} -gt 0 ]]; then
        log_warn "Missing workflows: ${missing_workflows[*]}"
    fi
    
    # Validate workflow syntax
    for workflow in "${available_workflows[@]}"; do
        local workflow_path="$workflow_dir/$workflow"
        if command -v yamllint >/dev/null; then
            if yamllint -d relaxed "$workflow_path" >/dev/null 2>&1; then
                log_info "✓ $workflow syntax valid"
            else
                log_warn "✗ $workflow syntax issues detected"
            fi
        fi
    done
}

# Validate performance monitoring setup
validate_monitoring_setup() {
    log_check "Performance monitoring configuration"
    
    local monitoring_dir="$PROJECT_ROOT/monitoring"
    
    if [[ ! -d "$monitoring_dir" ]]; then
        log_warn "Monitoring directory not found - performance monitoring not configured"
        return
    fi
    
    # Check for Grafana dashboards
    if [[ -d "$monitoring_dir/dashboards" ]]; then
        local dashboard_count=$(find "$monitoring_dir/dashboards" -name "*.json" | wc -l)
        if [[ $dashboard_count -gt 0 ]]; then
            log_info "✓ $dashboard_count Grafana dashboard(s) configured"
        else
            log_warn "No Grafana dashboards found"
        fi
    fi
    
    # Check for Prometheus alerts
    if [[ -d "$monitoring_dir/alerts" ]]; then
        local alert_count=$(find "$monitoring_dir/alerts" -name "*.yml" | wc -l)
        if [[ $alert_count -gt 0 ]]; then
            log_info "✓ $alert_count Prometheus alert file(s) configured"
        else
            log_warn "No Prometheus alert rules found"
        fi
    fi
    
    # Check for monitoring services
    local monitoring_services=(
        "prometheus:9090"
        "grafana:3001"
    )
    
    local available_monitoring=()
    for service in "${monitoring_services[@]}"; do
        local name="${service%%:*}"
        local port="${service#*:}"
        
        if curl -s --max-time 3 "http://localhost:$port" >/dev/null 2>&1; then
            available_monitoring+=("$name")
        fi
    done
    
    if [[ ${#available_monitoring[@]} -gt 0 ]]; then
        log_pass "Monitoring services available: ${available_monitoring[*]}"
    else
        log_warn "No monitoring services detected (Prometheus/Grafana)"
    fi
}

# Validate build system integration
validate_build_integration() {
    log_check "Build system integration"
    
    # Check Makefile
    if [[ -f "$PROJECT_ROOT/Makefile" ]]; then
        log_info "✓ Makefile present"
        
        # Check for test targets
        local test_targets=()
        while IFS= read -r line; do
            if [[ "$line" =~ ^[a-zA-Z0-9_.-]+:.*test ]]; then
                test_targets+=("$(echo "$line" | cut -d: -f1)")
            fi
        done < "$PROJECT_ROOT/Makefile"
        
        if [[ ${#test_targets[@]} -gt 0 ]]; then
            log_info "✓ Test targets in Makefile: ${test_targets[*]}"
        else
            log_warn "No test targets found in Makefile"
        fi
    else
        log_warn "Makefile not found"
    fi
    
    # Check package.json
    if [[ -f "$PROJECT_ROOT/package.json" ]]; then
        log_info "✓ package.json present"
        
        # Check for test scripts
        local test_scripts=$(jq -r '.scripts | to_entries[] | select(.key | test("test")) | .key' "$PROJECT_ROOT/package.json" 2>/dev/null || echo "")
        if [[ -n "$test_scripts" ]]; then
            log_info "✓ npm test scripts: $(echo "$test_scripts" | tr '\n' ' ')"
        else
            log_warn "No npm test scripts found"
        fi
    fi
    
    # Check for test results directory structure
    local test_results_dir="$PROJECT_ROOT/tests/results"
    if [[ -d "$test_results_dir" ]]; then
        log_info "✓ Test results directory exists"
    else
        log_info "Test results directory will be created automatically"
    fi
}

# Run a quick smoke test
run_smoke_test() {
    log_check "Quick smoke test execution"
    
    local smoke_test_script="$PROJECT_ROOT/tests/run_all_tests.sh"
    
    if [[ ! -f "$smoke_test_script" ]]; then
        log_fail "Master test script not found"
        return
    fi
    
    # Run with minimal configuration for validation
    local temp_log="${SCRIPT_DIR}/results/smoke_test.log"
    
    if cd "$PROJECT_ROOT" && \
       IT_RUN_INTEGRATION=false \
       IT_RUN_PERFORMANCE=false \
       IT_RUN_CHAOS=false \
       IT_RUN_E2E=false \
       timeout 60 bash ./tests/run_all_tests.sh --unit-only > "$temp_log" 2>&1; then
        log_pass "Smoke test completed successfully"
    else
        local exit_code=$?
        if [[ $exit_code -eq 124 ]]; then
            log_warn "Smoke test timed out (60s) - may indicate slow test execution"
        else
            log_warn "Smoke test failed - check test configuration"
        fi
        
        if [[ -f "$temp_log" ]]; then
            log_info "Last 5 lines of smoke test output:"
            tail -5 "$temp_log" | while read -r line; do
                log "  $line"
            done
        fi
    fi
}

# Generate validation report
generate_validation_report() {
    log ""
    log "=================================================================="
    log "${BLUE}Test Infrastructure Health Validation Report${NC}"
    log "=================================================================="
    
    local pass_rate_str="0"
    local pass_rate_int=0
    if [[ $TOTAL_CHECKS -gt 0 ]]; then
        pass_rate_int=$(( PASSED_CHECKS * 100 / TOTAL_CHECKS ))
        if command -v bc >/dev/null 2>&1; then
            pass_rate_str=$(echo "scale=1; $PASSED_CHECKS * 100 / $TOTAL_CHECKS" | bc -l 2>/dev/null || echo "$pass_rate_int")
        else
            pass_rate_str="$pass_rate_int"
        fi
    fi
    
    log "📊 Validation Summary:"
    log "   Total Checks: $TOTAL_CHECKS"
    log "   Passed: ${GREEN}$PASSED_CHECKS${NC}"
    log "   Failed: ${RED}$FAILED_CHECKS${NC}"
    log "   Warnings: ${YELLOW}$WARNING_CHECKS${NC}"
    log "   Pass Rate: ${pass_rate_str}%"
    log ""
    
    # Health grade
    local health_grade="POOR"
    if [[ $FAILED_CHECKS -eq 0 ]] && [[ $pass_rate_int -ge 90 ]]; then
        health_grade="EXCELLENT"
    elif [[ $FAILED_CHECKS -le 1 ]] && [[ $pass_rate_int -ge 70 ]]; then
        health_grade="GOOD"
    elif [[ $FAILED_CHECKS -le 3 ]] && [[ $pass_rate_int -ge 50 ]]; then
        health_grade="ACCEPTABLE"
    fi
    
    case "$health_grade" in
        "EXCELLENT") log "${GREEN}🏆 Test Infrastructure Health: EXCELLENT${NC}" ;;
        "GOOD") log "${GREEN}🥉 Test Infrastructure Health: GOOD${NC}" ;;
        "ACCEPTABLE") log "${YELLOW}⚠️  Test Infrastructure Health: ACCEPTABLE${NC}" ;;
        "POOR") log "${RED}❌ Test Infrastructure Health: POOR${NC}" ;;
    esac
    
    log ""
    log "📄 Detailed validation log: $VALIDATION_LOG"
    
    # Recommendations
    log ""
    log "📋 Recommendations:"
    if [[ $FAILED_CHECKS -gt 0 ]]; then
        log "   • Address failed checks before running comprehensive tests"
    fi
    if [[ $WARNING_CHECKS -gt 0 ]]; then
        log "   • Review warnings to improve test coverage and reliability"
    fi
    if [[ $health_grade == "EXCELLENT" ]]; then
        log "   • Test infrastructure is ready for production validation"
        log "   • Consider running full test suite: ./tests/run_all_tests.sh"
    fi
    
    # Return appropriate exit code
    if [[ $FAILED_CHECKS -eq 0 ]]; then
        return 0
    else
        return 1
    fi
}

# Main execution
main() {
    init_validation
    
    validate_test_scripts
    validate_dependencies
    validate_docker_environment
    validate_service_availability
    validate_database_connectivity
    validate_test_data
    validate_cicd_configuration
    validate_monitoring_setup
    validate_build_integration
    run_smoke_test
    
    generate_validation_report
}

# Run validation
main "$@"
