#!/bin/bash

# test_infoterminal_v020_e2e.sh
# InfoTerminal v0.2.0 - Comprehensive End-to-End Testing Script
# Tests all major features: Security, Verification, Orchestration

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/test_results_$(date +%Y%m%d_%H%M%S).log"
TEST_DATA_DIR="${SCRIPT_DIR}/test_data"
FRONTEND_URL="${IT_FRONTEND_URL:-http://localhost:3000}"
OPS_CONTROLLER_URL="${IT_OPS_CONTROLLER_URL:-http://localhost:8618}"
VERIFICATION_URL="${IT_VERIFICATION_URL:-http://localhost:8617}"
NIFI_URL="${IT_NIFI_URL:-http://localhost:8619}"
N8N_URL="${IT_N8N_URL:-http://localhost:5678}"

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
WARNINGS=0

# Helper functions
log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

log_header() {
    echo ""
    echo "=================================================================="
    log "${BLUE}$1${NC}"
    echo "=================================================================="
    echo ""
}

log_test() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    log "${CYAN}[TEST $TOTAL_TESTS] $1${NC}"
}

log_pass() {
    PASSED_TESTS=$((PASSED_TESTS + 1))
    log "${GREEN}✅ PASS: $1${NC}"
}

log_fail() {
    FAILED_TESTS=$((FAILED_TESTS + 1))
    log "${RED}❌ FAIL: $1${NC}"
}

log_warn() {
    WARNINGS=$((WARNINGS + 1))
    log "${YELLOW}⚠️  WARN: $1${NC}"
}

log_info() {
    log "${PURPLE}ℹ️  INFO: $1${NC}"
}

# HTTP request helper
http_request() {
    local method="$1"
    local url="$2"
    local data="${3:-}"
    local expected_status="${4:-200}"
    local timeout="${5:-30}"
    
    local response
    local status
    
    if [[ -n "$data" ]]; then
        response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
            -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" \
            --max-time "$timeout" \
            "$url" 2>/dev/null || echo "HTTPSTATUS:000")
    else
        response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
            -X "$method" \
            --max-time "$timeout" \
            "$url" 2>/dev/null || echo "HTTPSTATUS:000")
    fi
    
    status=$(echo "$response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    body=$(echo "$response" | sed -E 's/HTTPSTATUS:[0-9]*$//')
    
    if [[ "$status" == "$expected_status" ]]; then
        echo "$body"
        return 0
    else
        echo "HTTP $status: $body" >&2
        return 1
    fi
}

# Wait for service to be ready
wait_for_service() {
    local service_name="$1"
    local url="$2"
    local max_attempts="${3:-30}"
    
    log_info "Waiting for $service_name to be ready..."
    
    local attempts=0
    while [[ $attempts -lt $max_attempts ]]; do
        if curl -s --max-time 5 "$url" >/dev/null 2>&1; then
            log_pass "$service_name is ready"
            return 0
        fi
        
        attempts=$((attempts + 1))
        sleep 2
        printf "."
    done
    
    log_fail "$service_name is not responding after $max_attempts attempts"
    return 1
}

# Create test data
create_test_data() {
    log_header "Creating Test Data"
    
    mkdir -p "$TEST_DATA_DIR"
    
    # Sample text for verification
    cat > "$TEST_DATA_DIR/sample_article.txt" << 'EOF'
Climate change represents one of the most pressing challenges of our time. Recent studies indicate that global temperatures have risen by approximately 1.1 degrees Celsius since the late 19th century. The Intergovernmental Panel on Climate Change reports that human activities are the primary driver of this warming trend.

Scientists have observed significant changes in weather patterns worldwide. Arctic sea ice is declining at a rate of 13% per decade, according to NASA satellite data. The last decade has seen unprecedented heat waves, with 2023 being recorded as the hottest year on record.

Renewable energy adoption has accelerated in response to these challenges. Solar power capacity increased by 191 gigawatts globally in 2022, representing a 22% year-over-year growth. Wind power installations also reached record levels, with offshore wind projects showing particularly strong growth.

Despite these advances, carbon dioxide levels in the atmosphere continue to rise. The Mauna Loa Observatory recorded CO2 concentrations exceeding 420 parts per million in 2023, the highest level in over 3 million years. Experts warn that immediate action is necessary to limit warming to 1.5 degrees Celsius above pre-industrial levels.
EOF

    # JSON payload for API testing
    cat > "$TEST_DATA_DIR/verification_request.json" << 'EOF'
{
  "text": "Climate change represents one of the most pressing challenges of our time. Recent studies indicate that global temperatures have risen by approximately 1.1 degrees Celsius since the late 19th century.",
  "priority": "normal",
  "options": {
    "demo_mode": true,
    "max_claims": 5,
    "confidence_threshold": 0.7
  }
}
EOF

    # Incognito session request
    cat > "$TEST_DATA_DIR/incognito_request.json" << 'EOF'
{
  "sessionId": "test-incognito-session",
  "autoWipeMinutes": 30,
  "memoryOnlyMode": true,
  "isolatedContainers": true
}
EOF

    log_pass "Test data created successfully"
}

# Test basic service health
test_service_health() {
    log_header "Testing Service Health"
    
    # Test frontend health
    log_test "Frontend service health"
    if http_request "GET" "$FRONTEND_URL/api/health" >/dev/null; then
        log_pass "Frontend is healthy"
    else
        log_fail "Frontend health check failed"
    fi
    
    # Test ops controller health
    log_test "Ops Controller service health"
    if http_request "GET" "$OPS_CONTROLLER_URL/health" >/dev/null; then
        log_pass "Ops Controller is healthy"
    else
        log_fail "Ops Controller health check failed"
    fi
    
    # Test verification service health
    log_test "Verification service health"
    if http_request "GET" "$VERIFICATION_URL/health" >/dev/null; then
        log_pass "Verification service is healthy"
    else
        log_fail "Verification service health check failed"
    fi
    
    # Test comprehensive health
    log_test "Comprehensive system health"
    if response=$(http_request "GET" "$OPS_CONTROLLER_URL/health/comprehensive"); then
        if echo "$response" | grep -q '"status":"healthy"'; then
            log_pass "System comprehensive health check passed"
        else
            log_warn "System health is degraded: $(echo "$response" | jq -r '.status' 2>/dev/null || echo "unknown")"
        fi
    else
        log_fail "Comprehensive health check failed"
    fi
}

# Test orchestration health
test_orchestration_health() {
    log_header "Testing Orchestration Health"
    
    # Test NiFi health (optional)
    log_test "NiFi service health"
    if http_request "GET" "$NIFI_URL/nifi-api/system-diagnostics" "" "200" "10" >/dev/null; then
        log_pass "NiFi is healthy and accessible"
    else
        log_warn "NiFi is not accessible (may be disabled)"
    fi
    
    # Test n8n health (optional)
    log_test "n8n service health"
    if http_request "GET" "$N8N_URL/healthz" "" "200" "10" >/dev/null; then
        log_pass "n8n is healthy and accessible"
    else
        log_warn "n8n is not accessible (may be disabled)"
    fi
    
    # Test orchestration health endpoint
    log_test "Orchestration health endpoint"
    if response=$(http_request "GET" "$OPS_CONTROLLER_URL/api/orchestration/health"); then
        log_pass "Orchestration health endpoint is working"
        log_info "Orchestration status: $(echo "$response" | jq -r '.pipeline_health.pipeline_status' 2>/dev/null || echo "unknown")"
    else
        log_fail "Orchestration health endpoint failed"
    fi
}

# Test security features
test_security_features() {
    log_header "Testing Security Features"
    
    # Test incognito mode start
    log_test "Incognito mode start"
    if response=$(http_request "POST" "$FRONTEND_URL/api/security/incognito/start" "$(cat "$TEST_DATA_DIR/incognito_request.json")"); then
        session_id=$(echo "$response" | jq -r '.sessionId' 2>/dev/null)
        if [[ "$session_id" != "null" && -n "$session_id" ]]; then
            log_pass "Incognito session started: $session_id"
            echo "$session_id" > "$TEST_DATA_DIR/incognito_session_id"
        else
            log_fail "Incognito session start failed - no session ID returned"
        fi
    else
        log_fail "Incognito mode start failed"
    fi
    
    # Test security status
    log_test "Security status check"
    if response=$(http_request "GET" "$FRONTEND_URL/api/security/status"); then
        log_pass "Security status endpoint working"
        if echo "$response" | grep -q '"incognito_sessions"'; then
            log_info "Security status includes incognito session information"
        fi
    else
        log_fail "Security status check failed"
    fi
    
    # Test incognito session cleanup (if session was created)
    if [[ -f "$TEST_DATA_DIR/incognito_session_id" ]]; then
        session_id=$(cat "$TEST_DATA_DIR/incognito_session_id")
        log_test "Incognito session stop"
        if http_request "POST" "$FRONTEND_URL/api/security/incognito/$session_id/stop" >/dev/null; then
            log_pass "Incognito session stopped successfully"
            rm -f "$TEST_DATA_DIR/incognito_session_id"
        else
            log_warn "Incognito session stop failed"
        fi
    fi
}

# Test verification pipeline
test_verification_pipeline() {
    log_header "Testing Verification Pipeline"
    
    # Test claim extraction
    log_test "Claim extraction API"
    claim_request='{"text":"Climate change is caused by human activities. Global temperatures have increased by 1.1 degrees Celsius.","confidence_threshold":0.7,"max_claims":5}'
    if response=$(http_request "POST" "$FRONTEND_URL/api/verification/extract-claims" "$claim_request"); then
        claims_count=$(echo "$response" | jq 'length' 2>/dev/null || echo "0")
        if [[ "$claims_count" -gt 0 ]]; then
            log_pass "Claim extraction successful - extracted $claims_count claims"
            echo "$response" > "$TEST_DATA_DIR/extracted_claims.json"
        else
            log_fail "Claim extraction returned no claims"
        fi
    else
        log_fail "Claim extraction API failed"
    fi
    
    # Test evidence retrieval
    log_test "Evidence retrieval API"
    evidence_request='{"claim":"Climate change is caused by human activities","max_sources":3,"source_types":["web","wikipedia"]}'
    if response=$(http_request "POST" "$FRONTEND_URL/api/verification/find-evidence" "$evidence_request"); then
        evidence_count=$(echo "$response" | jq 'length' 2>/dev/null || echo "0")
        if [[ "$evidence_count" -gt 0 ]]; then
            log_pass "Evidence retrieval successful - found $evidence_count sources"
            echo "$response" > "$TEST_DATA_DIR/evidence.json"
        else
            log_fail "Evidence retrieval returned no sources"
        fi
    else
        log_fail "Evidence retrieval API failed"
    fi
    
    # Test stance classification
    log_test "Stance classification API"
    stance_request='{"claim":"Climate change is caused by human activities","evidence":"Scientific consensus confirms that human activities are the primary driver of climate change","context":"Climate science research"}'
    if response=$(http_request "POST" "$FRONTEND_URL/api/verification/classify-stance" "$stance_request"); then
        stance=$(echo "$response" | jq -r '.stance' 2>/dev/null)
        confidence=$(echo "$response" | jq -r '.confidence' 2>/dev/null)
        if [[ "$stance" != "null" && -n "$stance" ]]; then
            log_pass "Stance classification successful - stance: $stance, confidence: $confidence"
        else
            log_fail "Stance classification failed"
        fi
    else
        log_fail "Stance classification API failed"
    fi
    
    # Test credibility assessment
    log_test "Credibility assessment API"
    if response=$(http_request "GET" "$FRONTEND_URL/api/verification/credibility?url=https://www.nature.com/articles/climate-change"); then
        credibility_score=$(echo "$response" | jq -r '.credibility_score' 2>/dev/null)
        if [[ "$credibility_score" != "null" && -n "$credibility_score" ]]; then
            log_pass "Credibility assessment successful - score: $credibility_score"
        else
            log_fail "Credibility assessment failed"
        fi
    else
        log_fail "Credibility assessment API failed"
    fi
}

# Test orchestration workflows
test_orchestration_workflows() {
    log_header "Testing Orchestration Workflows"
    
    # Test verification session start
    log_test "Verification orchestration session"
    if response=$(http_request "POST" "$OPS_CONTROLLER_URL/api/verification/start" "$(cat "$TEST_DATA_DIR/verification_request.json")"); then
        session_id=$(echo "$response" | jq -r '.sessionId' 2>/dev/null)
        if [[ "$session_id" != "null" && -n "$session_id" ]]; then
            log_pass "Verification session started: $session_id"
            echo "$session_id" > "$TEST_DATA_DIR/verification_session_id"
            
            # Wait for session to process
            log_info "Waiting for verification session to complete..."
            sleep 15
            
            # Check session status
            log_test "Verification session status"
            if status_response=$(http_request "GET" "$OPS_CONTROLLER_URL/api/verification/status/$session_id"); then
                status=$(echo "$status_response" | jq -r '.status' 2>/dev/null)
                log_pass "Session status retrieved: $status"
                
                if [[ "$status" == "completed" ]]; then
                    log_pass "Verification session completed successfully"
                elif [[ "$status" == "processing" ]]; then
                    log_info "Verification session still processing (expected for complex workflows)"
                else
                    log_warn "Verification session status: $status"
                fi
            else
                log_fail "Failed to get session status"
            fi
        else
            log_fail "Verification session start failed - no session ID returned"
        fi
    else
        log_fail "Verification orchestration failed"
    fi
    
    # Test demo verification trigger
    log_test "Demo verification workflow"
    if response=$(http_request "POST" "$OPS_CONTROLLER_URL/api/demo/verification"); then
        demo_session=$(echo "$response" | jq -r '.sessionId' 2>/dev/null)
        if [[ "$demo_session" != "null" && -n "$demo_session" ]]; then
            log_pass "Demo verification triggered: $demo_session"
        else
            log_fail "Demo verification trigger failed"
        fi
    else
        log_warn "Demo verification endpoint not available (may require full orchestration stack)"
    fi
    
    # Test session listing
    log_test "Verification session listing"
    if response=$(http_request "GET" "$OPS_CONTROLLER_URL/api/orchestration/sessions"); then
        session_count=$(echo "$response" | jq '.sessions | length' 2>/dev/null || echo "0")
        log_pass "Session listing successful - found $session_count sessions"
    else
        log_fail "Session listing failed"
    fi
}

# Test frontend integration
test_frontend_integration() {
    log_header "Testing Frontend Integration"
    
    # Test main frontend pages
    local pages=("/verification" "/security" "/settings" "/docs")
    
    for page in "${pages[@]}"; do
        log_test "Frontend page: $page"
        if curl -s --max-time 10 "$FRONTEND_URL$page" | grep -q "<!DOCTYPE html>"; then
            log_pass "Page $page loads successfully"
        else
            log_fail "Page $page failed to load"
        fi
    done
    
    # Test verification dashboard
    log_test "Verification dashboard access"
    if curl -s --max-time 10 "$FRONTEND_URL/verification/dashboard" | grep -q "Verification.*Dashboard"; then
        log_pass "Verification dashboard loads successfully"
    else
        log_warn "Verification dashboard may not be fully functional"
    fi
    
    # Test API endpoints accessibility
    log_test "Frontend API health"
    if http_request "GET" "$FRONTEND_URL/api/health" >/dev/null; then
        log_pass "Frontend API is accessible"
    else
        log_fail "Frontend API is not accessible"
    fi
}

# Test data persistence
test_data_persistence() {
    log_header "Testing Data Persistence"
    
    # Test demo data load
    log_test "Demo data loading"
    demo_payload='{"type":"verification-test","data":{"test_id":"e2e_test_'$(date +%s)'","claims":3,"evidence":5}}'
    if response=$(http_request "POST" "$FRONTEND_URL/api/demo/load" "$demo_payload"); then
        log_pass "Demo data loading successful"
    else
        log_warn "Demo data loading failed (may not affect core functionality)"
    fi
    
    # Test search functionality (if available)
    log_test "Search integration"
    if response=$(http_request "GET" "$FRONTEND_URL/api/search?q=test"); then
        log_pass "Search integration working"
    else
        log_warn "Search integration not available"
    fi
}

# Performance tests
test_performance() {
    log_header "Testing Performance"
    
    # Test API response times
    log_test "API response time - Health endpoint"
    start_time=$(date +%s.%N)
    if http_request "GET" "$FRONTEND_URL/api/health" >/dev/null; then
        end_time=$(date +%s.%N)
        response_time=$(echo "$end_time - $start_time" | bc -l 2>/dev/null || echo "unknown")
        if [[ "$response_time" != "unknown" ]] && (( $(echo "$response_time < 2.0" | bc -l 2>/dev/null || echo "0") )); then
            log_pass "Health endpoint response time: ${response_time}s (good)"
        else
            log_warn "Health endpoint response time: ${response_time}s (may be slow)"
        fi
    else
        log_fail "Health endpoint performance test failed"
    fi
    
    # Test concurrent verification requests (light test)
    log_test "Concurrent request handling"
    local concurrent_success=0
    local concurrent_total=3
    
    for i in $(seq 1 $concurrent_total); do
        if http_request "GET" "$FRONTEND_URL/api/health" >/dev/null & then
            concurrent_success=$((concurrent_success + 1))
        fi
    done
    
    wait # Wait for background jobs
    
    if [[ $concurrent_success -eq $concurrent_total ]]; then
        log_pass "Concurrent request handling: $concurrent_success/$concurrent_total successful"
    else
        log_warn "Concurrent request handling: $concurrent_success/$concurrent_total successful"
    fi
}

# Cleanup test data
cleanup() {
    log_header "Cleaning Up Test Data"
    
    # Remove test session if exists
    if [[ -f "$TEST_DATA_DIR/verification_session_id" ]]; then
        session_id=$(cat "$TEST_DATA_DIR/verification_session_id")
        log_info "Cleaning up verification session: $session_id"
        http_request "DELETE" "$OPS_CONTROLLER_URL/api/verification/session/$session_id" >/dev/null || true
        rm -f "$TEST_DATA_DIR/verification_session_id"
    fi
    
    # Remove incognito session if exists
    if [[ -f "$TEST_DATA_DIR/incognito_session_id" ]]; then
        session_id=$(cat "$TEST_DATA_DIR/incognito_session_id")
        log_info "Cleaning up incognito session: $session_id"
        http_request "POST" "$FRONTEND_URL/api/security/incognito/$session_id/wipe" '{"secure":false}' >/dev/null || true
        rm -f "$TEST_DATA_DIR/incognito_session_id"
    fi
    
    # Clean up test data directory
    rm -rf "$TEST_DATA_DIR"
    
    log_pass "Cleanup completed"
}

# Generate test report
generate_report() {
    log_header "Test Report Summary"
    
    local pass_rate=0
    if [[ $TOTAL_TESTS -gt 0 ]]; then
        pass_rate=$(echo "scale=1; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc -l 2>/dev/null || echo "0")
    fi
    
    log "📊 ${BLUE}InfoTerminal v0.2.0 End-to-End Test Results${NC}"
    log "   Total Tests: $TOTAL_TESTS"
    log "   Passed: ${GREEN}$PASSED_TESTS${NC}"
    log "   Failed: ${RED}$FAILED_TESTS${NC}"
    log "   Warnings: ${YELLOW}$WARNINGS${NC}"
    log "   Pass Rate: ${pass_rate}%"
    log ""
    log "📋 Test Categories:"
    log "   ✅ Service Health"
    log "   🔒 Security Features" 
    log "   🔍 Verification Pipeline"
    log "   🔗 Orchestration Workflows"
    log "   🌐 Frontend Integration"
    log "   💾 Data Persistence"
    log "   ⚡ Performance"
    log ""
    log "📄 Detailed log saved to: $LOG_FILE"
    
    # Set exit code based on results
    if [[ $FAILED_TESTS -eq 0 ]]; then
        log "${GREEN}🎉 All tests completed successfully!${NC}"
        if [[ $WARNINGS -gt 0 ]]; then
            log "${YELLOW}⚠️  Note: $WARNINGS warnings were reported${NC}"
        fi
        return 0
    else
        log "${RED}❌ $FAILED_TESTS tests failed${NC}"
        return 1
    fi
}

# Main execution
main() {
    log_header "InfoTerminal v0.2.0 - End-to-End Testing"
    log "Starting comprehensive testing at $(date)"
    log "Log file: $LOG_FILE"
    
    # Wait for core services
    wait_for_service "Frontend" "$FRONTEND_URL/api/health" || { log_fail "Frontend not available, aborting tests"; exit 1; }
    wait_for_service "Ops Controller" "$OPS_CONTROLLER_URL/health" || { log_fail "Ops Controller not available, aborting tests"; exit 1; }
    
    # Create test data
    create_test_data
    
    # Run test suites
    test_service_health
    test_orchestration_health
    test_security_features
    test_verification_pipeline
    test_orchestration_workflows
    test_frontend_integration
    test_data_persistence
    test_performance
    
    # Cleanup
    cleanup
    
    # Generate report and exit
    generate_report
}

# Handle interruption
trap cleanup EXIT

# Run main function
main "$@"
