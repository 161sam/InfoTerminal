#!/bin/bash

# run_all_tests.sh
# InfoTerminal v1.0.0 - Master Test Execution Script
# Orchestrates: Unit, Integration, Performance, Chaos Tests

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MASTER_LOG="${RESULTS_DIR}/master_test_${TIMESTAMP}.log"

# Test configuration
RUN_UNIT_TESTS="${IT_RUN_UNIT:-true}"
RUN_INTEGRATION_TESTS="${IT_RUN_INTEGRATION:-true}"
RUN_PERFORMANCE_TESTS="${IT_RUN_PERFORMANCE:-true}"
RUN_CHAOS_TESTS="${IT_RUN_CHAOS:-false}"
RUN_E2E_TESTS="${IT_RUN_E2E:-true}"

# Test timeouts
UNIT_TEST_TIMEOUT="${IT_UNIT_TIMEOUT:-300}"          # 5 minutes
INTEGRATION_TEST_TIMEOUT="${IT_INTEGRATION_TIMEOUT:-900}"  # 15 minutes
PERFORMANCE_TEST_TIMEOUT="${IT_PERFORMANCE_TIMEOUT:-1800}" # 30 minutes
CHAOS_TEST_TIMEOUT="${IT_CHAOS_TIMEOUT:-600}"       # 10 minutes

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test result tracking
declare -A TEST_RESULTS
declare -A TEST_DURATIONS
declare -A TEST_LOGS

# Logging functions
log() {
    echo -e "$1" | tee -a "$MASTER_LOG"
}

log_header() {
    echo ""
    echo "################################################################"
    log "${BLUE}$1${NC}"
    echo "################################################################"
    echo ""
}

log_section() {
    echo ""
    echo "================================================================"
    log "${CYAN}$1${NC}"
    echo "================================================================"
}

log_info() {
    log "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    log "${GREEN}✅ $1${NC}"
}

log_warn() {
    log "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    log "${RED}❌ $1${NC}"
}

# Initialize test environment
init_test_environment() {
    log_header "InfoTerminal v1.0.0 - Master Test Suite"
    log "Starting comprehensive testing at $(date)"
    log "Test configuration:"
    log "  Unit Tests: $RUN_UNIT_TESTS"
    log "  Integration Tests: $RUN_INTEGRATION_TESTS"
    log "  Performance Tests: $RUN_PERFORMANCE_TESTS"
    log "  Chaos Tests: $RUN_CHAOS_TESTS"
    log "  E2E Tests: $RUN_E2E_TESTS"
    log ""
    log "Results directory: $RESULTS_DIR"
    log "Master log: $MASTER_LOG"
    
    mkdir -p "$RESULTS_DIR"
    
    # Create test environment info
    cat > "${RESULTS_DIR}/test_environment.json" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo "unknown")",
  "git_branch": "$(git branch --show-current 2>/dev/null || echo "unknown")",
  "system_info": {
    "hostname": "$(hostname)",
    "os": "$(uname -s)",
    "architecture": "$(uname -m)",
    "cpu_cores": "$(nproc 2>/dev/null || echo "unknown")",
    "memory_gb": "$(free -g 2>/dev/null | awk '/^Mem:/ {print $2}' || echo "unknown")"
  },
  "test_configuration": {
    "unit_tests": $RUN_UNIT_TESTS,
    "integration_tests": $RUN_INTEGRATION_TESTS,
    "performance_tests": $RUN_PERFORMANCE_TESTS,
    "chaos_tests": $RUN_CHAOS_TESTS,
    "e2e_tests": $RUN_E2E_TESTS
  }
}
EOF
}

# Execute test with timeout and logging
run_test_with_timeout() {
    local test_name="$1"
    local test_command="$2"
    local timeout_seconds="$3"
    local log_file="${RESULTS_DIR}/${test_name}_${TIMESTAMP}.log"
    
    log_section "Running $test_name"
    log_info "Command: $test_command"
    log_info "Timeout: ${timeout_seconds}s"
    log_info "Log file: $log_file"
    
    local start_time=$(date +%s)
    local exit_code=0
    
    # Run test with timeout
    if timeout "${timeout_seconds}s" bash -c "$test_command" > "$log_file" 2>&1; then
        TEST_RESULTS["$test_name"]="PASS"
        log_success "$test_name completed successfully"
    else
        exit_code=$?
        if [[ $exit_code -eq 124 ]]; then
            TEST_RESULTS["$test_name"]="TIMEOUT"
            log_error "$test_name timed out after ${timeout_seconds}s"
        else
            TEST_RESULTS["$test_name"]="FAIL"
            log_error "$test_name failed with exit code $exit_code"
        fi
    fi
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    TEST_DURATIONS["$test_name"]=$duration
    TEST_LOGS["$test_name"]="$log_file"
    
    log_info "$test_name duration: ${duration}s"
    
    # Show last few lines of output for context
    if [[ -f "$log_file" ]]; then
        log_info "Last 5 lines of output:"
        tail -5 "$log_file" | while read -r line; do
            log "  $line"
        done
    fi
    
    return $exit_code
}

# Unit tests execution
run_unit_tests() {
    if [[ "$RUN_UNIT_TESTS" != "true" ]]; then
        log_info "Unit tests skipped"
        return 0
    fi
    
    log_section "Unit Tests Phase"
    
    # Backend unit tests (Python)
    run_test_with_timeout "unit_backend" \
        "cd '$PROJECT_ROOT' && make gv.test" \
        "$UNIT_TEST_TIMEOUT" || true
    
    # Frontend unit tests (Node.js)
    run_test_with_timeout "unit_frontend" \
        "cd '$PROJECT_ROOT' && CI=1 npm -w apps/frontend run test --silent -- --reporter=dot" \
        "$UNIT_TEST_TIMEOUT" || true
    
    # CLI tests
    if [[ -f "$PROJECT_ROOT/tests/test_cli_banner_and_version.py" ]]; then
        run_test_with_timeout "unit_cli" \
            "cd '$PROJECT_ROOT' && python -m pytest tests/test_cli_*.py -v" \
            "$UNIT_TEST_TIMEOUT" || true
    fi
}

# Integration tests execution
run_integration_tests() {
    if [[ "$RUN_INTEGRATION_TESTS" != "true" ]]; then
        log_info "Integration tests skipped"
        return 0
    fi
    
    log_section "Integration Tests Phase"
    
    # Ensure test data is available
    if [[ -f "$PROJECT_ROOT/tests/data/test_data_pipeline.sh" ]]; then
        log_info "Setting up test data..."
        run_test_with_timeout "setup_test_data" \
            "cd '$PROJECT_ROOT/tests/data' && chmod +x test_data_pipeline.sh && ./test_data_pipeline.sh init" \
            60 || true
    fi
    
    # Core workflow integration tests
    if [[ -f "$PROJECT_ROOT/tests/integration/integration_workflow_tests.sh" ]]; then
        run_test_with_timeout "integration_workflows" \
            "cd '$PROJECT_ROOT/tests/integration' && chmod +x integration_workflow_tests.sh && ./integration_workflow_tests.sh" \
            "$INTEGRATION_TEST_TIMEOUT" || true
    fi
    
    # NLP integration tests
    if [[ -f "$PROJECT_ROOT/tests/test_doc_entities_integration.py" ]]; then
        run_test_with_timeout "integration_nlp" \
            "cd '$PROJECT_ROOT' && python -m pytest tests/test_doc_entities_integration.py -v" \
            300 || true
    fi
}

# Performance tests execution
run_performance_tests() {
    if [[ "$RUN_PERFORMANCE_TESTS" != "true" ]]; then
        log_info "Performance tests skipped"
        return 0
    fi
    
    log_section "Performance Tests Phase"
    
    # Core workflow benchmarks
    if [[ -f "$PROJECT_ROOT/tests/performance/benchmark_core_workflows.sh" ]]; then
        run_test_with_timeout "performance_benchmarks" \
            "cd '$PROJECT_ROOT/tests/performance' && chmod +x benchmark_core_workflows.sh && ./benchmark_core_workflows.sh" \
            "$PERFORMANCE_TEST_TIMEOUT" || true
    fi
    
    # Load testing
    if [[ -f "$PROJECT_ROOT/tests/performance/load_testing.sh" ]]; then
        run_test_with_timeout "performance_load" \
            "cd '$PROJECT_ROOT/tests/performance' && chmod +x load_testing.sh && IT_LOAD_USERS=25 IT_TEST_DURATION=60 ./load_testing.sh" \
            "$PERFORMANCE_TEST_TIMEOUT" || true
    fi
}

# Chaos engineering tests execution
run_chaos_tests() {
    if [[ "$RUN_CHAOS_TESTS" != "true" ]]; then
        log_info "Chaos tests skipped"
        return 0
    fi
    
    log_section "Chaos Engineering Tests Phase"
    
    if [[ -f "$PROJECT_ROOT/tests/chaos/chaos_engineering_tests.sh" ]]; then
        run_test_with_timeout "chaos_engineering" \
            "cd '$PROJECT_ROOT/tests/chaos' && chmod +x chaos_engineering_tests.sh && ./chaos_engineering_tests.sh" \
            "$CHAOS_TEST_TIMEOUT" || true
    fi
}

# E2E tests execution
run_e2e_tests() {
    if [[ "$RUN_E2E_TESTS" != "true" ]]; then
        log_info "E2E tests skipped"
        return 0
    fi
    
    log_section "End-to-End Tests Phase"
    
    # Existing E2E test script
    if [[ -f "$PROJECT_ROOT/test_infoterminal_v020_e2e.sh" ]]; then
        run_test_with_timeout "e2e_comprehensive" \
            "cd '$PROJECT_ROOT' && chmod +x test_infoterminal_v020_e2e.sh && ./test_infoterminal_v020_e2e.sh" \
            600 || true
    fi
    
    # User testing scenarios
    if [[ -d "$PROJECT_ROOT/tests/user-testing" ]]; then
        run_test_with_timeout "e2e_user_scenarios" \
            "cd '$PROJECT_ROOT/tests/user-testing' && find . -name '*.py' -exec python {} \;" \
            300 || true
    fi
}

# Generate comprehensive test report
generate_master_report() {
    log_header "Test Execution Summary"
    
    local total_tests=0
    local passed_tests=0
    local failed_tests=0
    local timeout_tests=0
    local total_duration=0
    
    # Count results
    for test_name in "${!TEST_RESULTS[@]}"; do
        total_tests=$((total_tests + 1))
        case "${TEST_RESULTS[$test_name]}" in
            "PASS") passed_tests=$((passed_tests + 1)) ;;
            "FAIL") failed_tests=$((failed_tests + 1)) ;;
            "TIMEOUT") timeout_tests=$((timeout_tests + 1)) ;;
        esac
        total_duration=$((total_duration + TEST_DURATIONS[$test_name]))
    done
    
    # Calculate success rate
    local success_rate_int=0
    local success_rate="0"
    if [[ $total_tests -gt 0 ]]; then
        success_rate_int=$(( passed_tests * 100 / total_tests ))
        if command -v bc >/dev/null 2>&1; then
            success_rate=$(echo "scale=1; $passed_tests * 100 / $total_tests" | bc -l 2>/dev/null || echo "$success_rate_int")
        else
            success_rate="$success_rate_int"
        fi
    fi
    
    # Format duration
    local duration_formatted
    if [[ $total_duration -gt 3600 ]]; then
        duration_formatted="$((total_duration / 3600))h $((total_duration % 3600 / 60))m $((total_duration % 60))s"
    elif [[ $total_duration -gt 60 ]]; then
        duration_formatted="$((total_duration / 60))m $((total_duration % 60))s"
    else
        duration_formatted="${total_duration}s"
    fi
    
    # Create JSON report
    local json_report="${RESULTS_DIR}/master_test_report_${TIMESTAMP}.json"
    cat > "$json_report" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "total_duration_seconds": $total_duration,
  "summary": {
    "total_tests": $total_tests,
    "passed": $passed_tests,
    "failed": $failed_tests,
    "timeouts": $timeout_tests,
    "success_rate": $success_rate
  },
  "test_results": {
EOF
    
    # Add individual test results
    local first=true
    for test_name in "${!TEST_RESULTS[@]}"; do
        if [[ "$first" == "true" ]]; then
            first=false
        else
            echo "," >> "$json_report"
        fi
        cat >> "$json_report" << EOF
    "$test_name": {
      "status": "${TEST_RESULTS[$test_name]}",
      "duration_seconds": ${TEST_DURATIONS[$test_name]},
      "log_file": "${TEST_LOGS[$test_name]}"
    }
EOF
    done
    
    cat >> "$json_report" << EOF
  },
  "environment": $(cat "${RESULTS_DIR}/test_environment.json")
}
EOF
    
    # Generate markdown report
    local md_report="${RESULTS_DIR}/TEST_REPORT_${TIMESTAMP}.md"
    cat > "$md_report" << EOF
# InfoTerminal v1.0.0 - Test Execution Report

**Date:** $(date)  
**Duration:** $duration_formatted  
**Success Rate:** ${success_rate}%  

## Summary

| Metric | Count |
|--------|-------|
| Total Tests | $total_tests |
| ✅ Passed | $passed_tests |
| ❌ Failed | $failed_tests |
| ⏰ Timeouts | $timeout_tests |

## Test Results

| Test Name | Status | Duration | Log File |
|-----------|--------|----------|----------|
EOF
    
    for test_name in "${!TEST_RESULTS[@]}"; do
        local status_icon
        case "${TEST_RESULTS[$test_name]}" in
            "PASS") status_icon="✅" ;;
            "FAIL") status_icon="❌" ;;
            "TIMEOUT") status_icon="⏰" ;;
            *) status_icon="❓" ;;
        esac
        
        echo "| $test_name | $status_icon ${TEST_RESULTS[$test_name]} | ${TEST_DURATIONS[$test_name]}s | $(basename "${TEST_LOGS[$test_name]}") |" >> "$md_report"
    done
    
    cat >> "$md_report" << 'EOF'

## Test Categories

### 🧪 Unit Tests
- Backend (Python): Service-level unit tests
- Frontend (TypeScript): Component and utility tests  
- CLI: Command-line interface tests

### 🔗 Integration Tests
- Workflow Tests: End-to-end data flows
- NLP Integration: Document processing pipelines
- API Integration: Service-to-service communication

### ⚡ Performance Tests
- Benchmark Tests: Core workflow performance
- Load Tests: Concurrent user simulation
- Resource Monitoring: CPU, memory, throughput

### 🔥 Chaos Engineering
- Service Failure Recovery
- Database Connection Loss
- Network Partition Handling
- Cascade Failure Prevention

### 🌐 End-to-End Tests
- Complete User Workflows
- Security Feature Testing
- Cross-browser Compatibility

EOF
    
    # Performance analysis section
    if [[ -f "$PROJECT_ROOT/tests/performance/results/benchmark_"*".json" ]]; then
        echo "## 📊 Performance Metrics" >> "$md_report"
        echo "" >> "$md_report"
        
        local latest_benchmark=$(ls -t "$PROJECT_ROOT/tests/performance/results/benchmark_"*".json" 2>/dev/null | head -1 || echo "")
        if [[ -n "$latest_benchmark" ]]; then
            local pass_rate=$(jq -r '.performance_summary.pass_rate // "N/A"' "$latest_benchmark" 2>/dev/null || echo "N/A")
            local total_workflows=$(jq -r '.performance_summary.total_workflows // 0' "$latest_benchmark" 2>/dev/null || echo "0")
            
            echo "- **Performance Pass Rate:** ${pass_rate}%" >> "$md_report"
            echo "- **Benchmarked Workflows:** $total_workflows" >> "$md_report"
            echo "" >> "$md_report"
        fi
    fi
    
    # Quality assessment
    echo "## 🎯 Quality Assessment" >> "$md_report"
    echo "" >> "$md_report"
    
    local quality_grade="POOR"
    if [[ $success_rate_int -ge 95 ]] && [[ $failed_tests -eq 0 ]]; then
        quality_grade="EXCELLENT"
    elif [[ $success_rate_int -ge 80 ]] && [[ $failed_tests -le 1 ]]; then
        quality_grade="GOOD"
    elif [[ $success_rate_int -ge 60 ]]; then
        quality_grade="ACCEPTABLE"
    fi
    
    case "$quality_grade" in
        "EXCELLENT") echo "🏆 **Grade: EXCELLENT** - Production ready!" >> "$md_report" ;;
        "GOOD") echo "🥉 **Grade: GOOD** - Minor issues to address" >> "$md_report" ;;
        "ACCEPTABLE") echo "⚠️ **Grade: ACCEPTABLE** - Several issues need resolution" >> "$md_report" ;;
        "POOR") echo "❌ **Grade: POOR** - Significant issues must be fixed" >> "$md_report" ;;
    esac
    
    # Console output
    log "📊 ${BLUE}Test Execution Results${NC}"
    log "   Total Tests: $total_tests"
    log "   Passed: ${GREEN}$passed_tests${NC}"
    log "   Failed: ${RED}$failed_tests${NC}"
    log "   Timeouts: ${YELLOW}$timeout_tests${NC}"
    log "   Success Rate: ${success_rate}%"
    log "   Total Duration: $duration_formatted"
    log ""
    log "📄 Reports generated:"
    log "   JSON: $json_report"
    log "   Markdown: $md_report"
    
    # Test breakdown by category
    log ""
    log "📋 Test Results by Category:"
    for test_name in "${!TEST_RESULTS[@]}"; do
        local status_color
        case "${TEST_RESULTS[$test_name]}" in
            "PASS") status_color="$GREEN" ;;
            "FAIL") status_color="$RED" ;;
            "TIMEOUT") status_color="$YELLOW" ;;
            *) status_color="$NC" ;;
        esac
        log "   ${status_color}${TEST_RESULTS[$test_name]}${NC} $test_name (${TEST_DURATIONS[$test_name]}s)"
    done
    
    # Final assessment
    log ""
    case "$quality_grade" in
        "EXCELLENT") log "${GREEN}🏆 Overall Assessment: EXCELLENT - InfoTerminal v1.0.0 is production ready!${NC}" ;;
        "GOOD") log "${GREEN}🥉 Overall Assessment: GOOD - Minor issues to address before production${NC}" ;;
        "ACCEPTABLE") log "${YELLOW}⚠️  Overall Assessment: ACCEPTABLE - Address issues before v1.0.0 release${NC}" ;;
        "POOR") log "${RED}❌ Overall Assessment: POOR - Significant work needed before production${NC}" ;;
    esac
    
    # Return appropriate exit code
    if [[ $failed_tests -eq 0 ]] && [[ $timeout_tests -eq 0 ]]; then
        return 0
    elif [[ $success_rate_int -ge 80 ]]; then
        return 1
    else
        return 2
    fi
}

# Cleanup function
cleanup() {
    log_info "Cleaning up test processes and temporary data..."
    
    # Clean up test data
    if [[ -f "$PROJECT_ROOT/tests/data/test_data_pipeline.sh" ]]; then
        cd "$PROJECT_ROOT/tests/data"
        ./test_data_pipeline.sh cleanup >/dev/null 2>&1 || true
    fi
    
    # Kill any remaining background processes
    jobs -p | xargs -r kill 2>/dev/null || true
    
    log_info "Cleanup completed"
}

# Pre-flight checks
run_preflight_checks() {
    log_section "Pre-flight Checks"
    
    # Check dependencies
    local missing_deps=()
    
    for cmd in jq bc curl timeout; do
        if ! command -v "$cmd" >/dev/null; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies before running tests"
        exit 1
    fi
    
    # Check if we're in the right directory
    if [[ ! -f "$PROJECT_ROOT/package.json" ]] || [[ ! -f "$PROJECT_ROOT/Makefile" ]]; then
        log_error "Not in InfoTerminal project root directory"
        log_info "Please run this script from the InfoTerminal project root"
        exit 1
    fi
    
    # Check Docker availability for integration tests
    if [[ "$RUN_INTEGRATION_TESTS" == "true" ]] || [[ "$RUN_PERFORMANCE_TESTS" == "true" ]]; then
        if ! command -v docker >/dev/null; then
            log_warn "Docker not available - some integration/performance tests may fail"
        elif ! docker info >/dev/null 2>&1; then
            log_warn "Docker daemon not running - some integration/performance tests may fail"
        else
            log_success "Docker available for containerized tests"
        fi
    fi
    
    # Check service availability for integration tests
    if [[ "$RUN_INTEGRATION_TESTS" == "true" ]] || [[ "$RUN_PERFORMANCE_TESTS" == "true" ]]; then
        local services_needed=("http://localhost:3000" "http://localhost:8403")
        local services_available=0
        
        for service_url in "${services_needed[@]}"; do
            if curl -s --max-time 5 "$service_url" >/dev/null 2>&1 || \
               curl -s --max-time 5 "$service_url/health" >/dev/null 2>&1 || \
               curl -s --max-time 5 "$service_url/api/health" >/dev/null 2>&1; then
                services_available=$((services_available + 1))
                log_info "✓ Service available: $service_url"
            else
                log_warn "✗ Service not available: $service_url"
            fi
        done
        
        if [[ $services_available -eq 0 ]]; then
            log_warn "No services detected - integration/performance tests may fail"
            log_info "Consider starting services with: docker-compose up -d"
        else
            log_success "$services_available/${#services_needed[@]} services available"
        fi
    fi
    
    log_success "Pre-flight checks completed"
}

# Usage information
usage() {
    cat << 'EOF'
InfoTerminal v1.0.0 - Master Test Execution Script

Usage: ./run_all_tests.sh [OPTIONS]

Options:
  --unit-only          Run only unit tests
  --integration-only   Run only integration tests  
  --performance-only   Run only performance tests
  --chaos-only         Run only chaos engineering tests
  --e2e-only          Run only end-to-end tests
  --skip-unit         Skip unit tests
  --skip-integration  Skip integration tests
  --skip-performance  Skip performance tests
  --skip-chaos        Skip chaos engineering tests
  --skip-e2e          Skip end-to-end tests
  --fast              Fast mode (reduced timeouts and test scope)
  --help              Show this help message

Environment Variables:
  IT_RUN_UNIT         Enable/disable unit tests (default: true)
  IT_RUN_INTEGRATION  Enable/disable integration tests (default: true)
  IT_RUN_PERFORMANCE  Enable/disable performance tests (default: true)
  IT_RUN_CHAOS        Enable/disable chaos tests (default: false)
  IT_RUN_E2E          Enable/disable E2E tests (default: true)

Examples:
  ./run_all_tests.sh                    # Run all enabled tests
  ./run_all_tests.sh --unit-only        # Run only unit tests
  ./run_all_tests.sh --skip-chaos       # Skip chaos engineering tests
  ./run_all_tests.sh --fast             # Fast execution mode
EOF
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --unit-only)
                RUN_UNIT_TESTS="true"
                RUN_INTEGRATION_TESTS="false"
                RUN_PERFORMANCE_TESTS="false"
                RUN_CHAOS_TESTS="false"
                RUN_E2E_TESTS="false"
                shift
                ;;
            --integration-only)
                RUN_UNIT_TESTS="false"
                RUN_INTEGRATION_TESTS="true"
                RUN_PERFORMANCE_TESTS="false"
                RUN_CHAOS_TESTS="false"
                RUN_E2E_TESTS="false"
                shift
                ;;
            --performance-only)
                RUN_UNIT_TESTS="false"
                RUN_INTEGRATION_TESTS="false"
                RUN_PERFORMANCE_TESTS="true"
                RUN_CHAOS_TESTS="false"
                RUN_E2E_TESTS="false"
                shift
                ;;
            --chaos-only)
                RUN_UNIT_TESTS="false"
                RUN_INTEGRATION_TESTS="false"
                RUN_PERFORMANCE_TESTS="false"
                RUN_CHAOS_TESTS="true"
                RUN_E2E_TESTS="false"
                shift
                ;;
            --e2e-only)
                RUN_UNIT_TESTS="false"
                RUN_INTEGRATION_TESTS="false"
                RUN_PERFORMANCE_TESTS="false"
                RUN_CHAOS_TESTS="false"
                RUN_E2E_TESTS="true"
                shift
                ;;
            --skip-unit)
                RUN_UNIT_TESTS="false"
                shift
                ;;
            --skip-integration)
                RUN_INTEGRATION_TESTS="false"
                shift
                ;;
            --skip-performance)
                RUN_PERFORMANCE_TESTS="false"
                shift
                ;;
            --skip-chaos)
                RUN_CHAOS_TESTS="false"
                shift
                ;;
            --skip-e2e)
                RUN_E2E_TESTS="false"
                shift
                ;;
            --fast)
                UNIT_TEST_TIMEOUT=120
                INTEGRATION_TEST_TIMEOUT=300
                PERFORMANCE_TEST_TIMEOUT=600
                CHAOS_TEST_TIMEOUT=180
                export IT_LOAD_USERS=10
                export IT_TEST_DURATION=30
                shift
                ;;
            --help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
}

# Main execution
main() {
    # Parse arguments
    parse_arguments "$@"
    
    # Initialize
    init_test_environment
    
    # Pre-flight checks
    run_preflight_checks
    
    # Execute test phases
    run_unit_tests
    run_integration_tests
    run_performance_tests
    run_chaos_tests
    run_e2e_tests
    
    # Generate final report
    generate_master_report
}

# Handle interruption
trap cleanup EXIT

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Script is being executed directly
    main "$@"
fi
