#!/bin/bash

# chaos_engineering_tests.sh
# InfoTerminal v1.0.0 - Chaos Engineering & Resilience Testing
# Tests: Service Failures, Network Partitions, Database Issues, Recovery

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CHAOS_LOG="${RESULTS_DIR}/chaos_${TIMESTAMP}.json"
RECOVERY_TIMEOUT=30  # Maximum recovery time in seconds

# Service URLs and names
declare -A SERVICES=(
    ["frontend"]="${IT_FRONTEND_URL:-http://localhost:3000}"
    ["graph-api"]="${IT_GRAPH_API_URL:-http://localhost:8403}"
    ["search-api"]="${IT_SEARCH_API_URL:-http://localhost:8401}"
    ["doc-entities"]="${IT_DOC_ENTITIES_URL:-http://localhost:8402}"
    ["verification"]="${IT_VERIFICATION_URL:-http://localhost:8617}"
    ["ops-controller"]="${IT_OPS_CONTROLLER_URL:-http://localhost:8618}"
)

# Docker service names (if using Docker Compose)
declare -A DOCKER_SERVICES=(
    ["frontend"]="infoterminal-frontend"
    ["graph-api"]="infoterminal-graph-views"
    ["search-api"]="infoterminal-search-api"
    ["doc-entities"]="infoterminal-doc-entities"
    ["verification"]="infoterminal-verification"
    ["ops-controller"]="infoterminal-ops-controller"
    ["neo4j"]="infoterminal-neo4j"
    ["opensearch"]="infoterminal-opensearch"
    ["postgres"]="infoterminal-postgres"
)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Test counters
TOTAL_CHAOS_TESTS=0
PASSED_CHAOS_TESTS=0
FAILED_CHAOS_TESTS=0

# Logging functions
log() {
    echo -e "$1" | tee -a "${RESULTS_DIR}/chaos_${TIMESTAMP}.log"
}

log_header() {
    echo ""
    echo "=================================================================="
    log "${BLUE}$1${NC}"
    echo "=================================================================="
    echo ""
}

log_test() {
    TOTAL_CHAOS_TESTS=$((TOTAL_CHAOS_TESTS + 1))
    log "${PURPLE}[CHAOS TEST $TOTAL_CHAOS_TESTS] $1${NC}"
}

log_pass() {
    PASSED_CHAOS_TESTS=$((PASSED_CHAOS_TESTS + 1))
    log "${GREEN}✅ PASS: $1${NC}"
}

log_fail() {
    FAILED_CHAOS_TESTS=$((FAILED_CHAOS_TESTS + 1))
    log "${RED}❌ FAIL: $1${NC}"
}

log_info() {
    log "${BLUE}ℹ️  INFO: $1${NC}"
}

# Initialize chaos test results
init_chaos_results() {
    mkdir -p "$RESULTS_DIR"
    cat > "$CHAOS_LOG" << 'EOF'
{
  "timestamp": null,
  "chaos_tests": {},
  "resilience_metrics": {},
  "recovery_times": {},
  "failure_impact_analysis": {}
}
EOF
    
    jq --arg ts "$(date -Iseconds)" '.timestamp = $ts' "$CHAOS_LOG" > "${CHAOS_LOG}.tmp" && mv "${CHAOS_LOG}.tmp" "$CHAOS_LOG"
}

# Check if service is healthy
check_service_health() {
    local service_name="$1"
    local url="${SERVICES[$service_name]}"
    local timeout="${2:-5}"
    
    if curl -s --max-time "$timeout" "$url/health" >/dev/null 2>&1 || \
       curl -s --max-time "$timeout" "$url/api/health" >/dev/null 2>&1 || \
       curl -s --max-time "$timeout" "$url" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Monitor service recovery
monitor_service_recovery() {
    local service_name="$1"
    local max_wait="${2:-$RECOVERY_TIMEOUT}"
    local check_interval="${3:-2}"
    
    local start_time=$(date +%s)
    local attempts=0
    
    log_info "Monitoring $service_name recovery (max ${max_wait}s)..."
    
    while [[ $attempts -lt $((max_wait / check_interval)) ]]; do
        if check_service_health "$service_name" 3; then
            local recovery_time=$(($(date +%s) - start_time))
            log_info "$service_name recovered in ${recovery_time}s"
            return $recovery_time
        fi
        
        attempts=$((attempts + 1))
        sleep "$check_interval"
        printf "."
    done
    
    echo ""
    log_info "$service_name did not recover within ${max_wait}s"
    return -1
}

# Docker service manipulation
stop_docker_service() {
    local service_name="$1"
    local docker_name="${DOCKER_SERVICES[$service_name]:-$service_name}"
    
    if command -v docker >/dev/null && docker ps --format "table {{.Names}}" | grep -q "$docker_name"; then
        log_info "Stopping Docker service: $docker_name"
        docker stop "$docker_name" >/dev/null 2>&1 || true
        return 0
    elif command -v docker-compose >/dev/null && [[ -f "docker-compose.yml" ]]; then
        log_info "Stopping service via docker-compose: $service_name"
        docker-compose stop "$service_name" >/dev/null 2>&1 || true
        return 0
    else
        log_info "Docker service manipulation not available for $service_name"
        return 1
    fi
}

start_docker_service() {
    local service_name="$1"
    local docker_name="${DOCKER_SERVICES[$service_name]:-$service_name}"
    
    if command -v docker >/dev/null; then
        log_info "Starting Docker service: $docker_name"
        docker start "$docker_name" >/dev/null 2>&1 || true
        return 0
    elif command -v docker-compose >/dev/null && [[ -f "docker-compose.yml" ]]; then
        log_info "Starting service via docker-compose: $service_name"
        docker-compose start "$service_name" >/dev/null 2>&1 || true
        return 0
    else
        log_info "Docker service manipulation not available for $service_name"
        return 1
    fi
}

# Simulate network partition using iptables (requires sudo)
simulate_network_partition() {
    local service_name="$1"
    local url="${SERVICES[$service_name]}"
    local port=$(echo "$url" | sed -n 's/.*:\([0-9]*\).*/\1/p')
    
    if [[ -z "$port" ]]; then
        log_info "Cannot determine port for $service_name, skipping network partition"
        return 1
    fi
    
    if command -v iptables >/dev/null && [[ $EUID -eq 0 ]]; then
        log_info "Creating network partition for port $port"
        iptables -A INPUT -p tcp --dport "$port" -j DROP 2>/dev/null || true
        iptables -A OUTPUT -p tcp --sport "$port" -j DROP 2>/dev/null || true
        return 0
    else
        log_info "Network partition simulation requires root privileges, using alternative method"
        # Alternative: simulate by overwhelming the service
        simulate_service_overload "$service_name"
        return $?
    fi
}

remove_network_partition() {
    local service_name="$1"
    local url="${SERVICES[$service_name]}"
    local port=$(echo "$url" | sed -n 's/.*:\([0-9]*\).*/\1/p')
    
    if [[ -n "$port" ]] && command -v iptables >/dev/null && [[ $EUID -eq 0 ]]; then
        log_info "Removing network partition for port $port"
        iptables -D INPUT -p tcp --dport "$port" -j DROP 2>/dev/null || true
        iptables -D OUTPUT -p tcp --sport "$port" -j DROP 2>/dev/null || true
        return 0
    fi
    
    return 0
}

# Simulate service overload
simulate_service_overload() {
    local service_name="$1"
    local url="${SERVICES[$service_name]}"
    local duration="${2:-10}"
    
    log_info "Simulating overload for $service_name (${duration}s)"
    
    local pids=()
    
    # Start multiple concurrent request streams
    for i in {1..20}; do
        (
            local end_time=$(($(date +%s) + duration))
            while [[ $(date +%s) -lt $end_time ]]; do
                curl -s --max-time 1 "$url" >/dev/null 2>&1 || true
                curl -s --max-time 1 "$url/health" >/dev/null 2>&1 || true
            done
        ) &
        pids+=($!)
    done
    
    # Wait for overload simulation to complete
    sleep "$duration"
    
    # Clean up background processes
    for pid in "${pids[@]}"; do
        kill "$pid" 2>/dev/null || true
    done
    
    wait 2>/dev/null || true
    log_info "Service overload simulation completed"
}

# Test 1: Single Service Failure Recovery
test_service_failure_recovery() {
    log_header "Service Failure Recovery Testing"
    
    for service in "${!SERVICES[@]}"; do
        log_test "Service failure recovery: $service"
        
        # Check initial health
        if ! check_service_health "$service"; then
            log_info "$service is already unhealthy, skipping test"
            continue
        fi
        
        local test_start=$(date +%s)
        
        # Record pre-failure state
        local pre_failure_response=""
        if pre_failure_response=$(curl -s --max-time 5 "${SERVICES[$service]}/health" 2>/dev/null); then
            log_info "$service pre-failure health: OK"
        fi
        
        # Simulate service failure
        local failure_simulated=false
        if stop_docker_service "$service"; then
            failure_simulated=true
            log_info "$service stopped successfully"
        else
            log_info "Cannot stop $service, simulating with network issues"
            simulate_service_overload "$service" 15
            failure_simulated=true
        fi
        
        if $failure_simulated; then
            # Verify service is down
            sleep 3
            if check_service_health "$service" 3; then
                log_info "$service still responding after failure simulation"
            else
                log_info "$service failure confirmed"
            fi
            
            # Restore service
            if start_docker_service "$service"; then
                log_info "$service restart initiated"
            fi
            
            # Monitor recovery
            local recovery_time
            recovery_time=$(monitor_service_recovery "$service")
            local test_end=$(date +%s)
            local total_test_time=$((test_end - test_start))
            
            if [[ $recovery_time -ge 0 ]] && [[ $recovery_time -le $RECOVERY_TIMEOUT ]]; then
                log_pass "$service recovered in ${recovery_time}s (within ${RECOVERY_TIMEOUT}s limit)"
                
                # Store successful recovery
                local recovery_result=$(cat << EOF
{
  "service": "$service",
  "recovery_time_seconds": $recovery_time,
  "total_test_time": $total_test_time,
  "status": "success",
  "recovery_method": "docker_restart"
}
EOF
                )
                
                jq --argjson result "$recovery_result" ".chaos_tests.\"${service}_recovery\" = \$result" "$CHAOS_LOG" > "${CHAOS_LOG}.tmp" && mv "${CHAOS_LOG}.tmp" "$CHAOS_LOG"
            else
                log_fail "$service recovery failed or exceeded timeout"
                
                local recovery_result=$(cat << EOF
{
  "service": "$service",
  "recovery_time_seconds": $recovery_time,
  "total_test_time": $total_test_time,
  "status": "failed",
  "recovery_method": "docker_restart"
}
EOF
                )
                
                jq --argjson result "$recovery_result" ".chaos_tests.\"${service}_recovery\" = \$result" "$CHAOS_LOG" > "${CHAOS_LOG}.tmp" && mv "${CHAOS_LOG}.tmp" "$CHAOS_LOG"
            fi
        else
            log_info "Could not simulate failure for $service, skipping test"
        fi
        
        # Cool-down period
        sleep 5
    done
}

# Test 2: Database Connection Loss Recovery
test_database_connection_loss() {
    log_header "Database Connection Loss Recovery"
    
    # Test Neo4j connection loss
    log_test "Neo4j connection loss recovery"
    
    if [[ "${DOCKER_SERVICES[neo4j]:-}" ]]; then
        local neo4j_service="${DOCKER_SERVICES[neo4j]}"
        
        # Check services dependent on Neo4j
        local dependent_services=("graph-api")
        
        for dep_service in "${dependent_services[@]}"; do
            if check_service_health "$dep_service"; then
                log_info "$dep_service is healthy before Neo4j failure"
                
                # Stop Neo4j
                if docker stop "$neo4j_service" >/dev/null 2>&1; then
                    log_info "Neo4j stopped"
                    
                    # Wait and check dependent service behavior
                    sleep 5
                    
                    # Test if dependent service handles database loss gracefully
                    local graceful_degradation=false
                    if curl -s --max-time 10 "${SERVICES[$dep_service]}/health" | grep -q "degraded\|partial\|unhealthy"; then
                        graceful_degradation=true
                        log_info "$dep_service shows graceful degradation"
                    elif ! check_service_health "$dep_service" 10; then
                        log_info "$dep_service became unavailable (expected behavior)"
                    fi
                    
                    # Restart Neo4j
                    docker start "$neo4j_service" >/dev/null 2>&1 || true
                    log_info "Neo4j restart initiated"
                    
                    # Monitor service recovery
                    sleep 10  # Give Neo4j time to start
                    local recovery_time
                    recovery_time=$(monitor_service_recovery "$dep_service" 45)
                    
                    if [[ $recovery_time -ge 0 ]]; then
                        log_pass "$dep_service recovered after Neo4j restoration in ${recovery_time}s"
                    else
                        log_fail "$dep_service did not recover after Neo4j restoration"
                    fi
                else
                    log_info "Cannot stop Neo4j, skipping database connection test"
                fi
            fi
        done
    else
        log_info "Neo4j service not identified, skipping database connection test"
    fi
}

# Test 3: High Load Degradation Recovery
test_high_load_degradation() {
    log_header "High Load Degradation and Recovery"
    
    log_test "System behavior under extreme load"
    
    # Identify the most critical service (frontend)
    local critical_service="frontend"
    
    if check_service_health "$critical_service"; then
        # Measure baseline performance
        log_info "Measuring baseline performance"
        local baseline_start=$(date +%s.%N)
        curl -s --max-time 5 "${SERVICES[$critical_service]}/api/health" >/dev/null 2>&1
        local baseline_end=$(date +%s.%N)
        local baseline_time=$(echo "$baseline_end - $baseline_start" | bc -l)
        local baseline_ms=$(echo "$baseline_time * 1000" | bc -l | cut -d. -f1)
        
        log_info "Baseline response time: ${baseline_ms}ms"
        
        # Generate extreme load
        log_info "Generating extreme load for 20 seconds..."
        local load_pids=()
        
        # Start 50 concurrent load generators
        for i in {1..50}; do
            (
                local end_time=$(($(date +%s) + 20))
                while [[ $(date +%s) -lt $end_time ]]; do
                    curl -s --max-time 2 "${SERVICES[$critical_service]}/api/health" >/dev/null 2>&1 || true
                    curl -s --max-time 2 "${SERVICES[$critical_service]}" >/dev/null 2>&1 || true
                done
            ) &
            load_pids+=($!)
        done
        
        # Monitor system during load
        sleep 5  # Let load ramp up
        
        local under_load_times=()
        for i in {1..5}; do
            local load_start=$(date +%s.%N)
            if curl -s --max-time 10 "${SERVICES[$critical_service]}/api/health" >/dev/null 2>&1; then
                local load_end=$(date +%s.%N)
                local load_time=$(echo "$load_end - $load_start" | bc -l)
                local load_ms=$(echo "$load_time * 1000" | bc -l | cut -d. -f1)
                under_load_times+=("$load_ms")
            fi
            sleep 2
        done
        
        # Stop load generation
        for pid in "${load_pids[@]}"; do
            kill "$pid" 2>/dev/null || true
        done
        wait 2>/dev/null || true
        
        log_info "Load generation stopped, monitoring recovery"
        
        # Monitor recovery
        sleep 5  # Recovery grace period
        
        local recovery_times=()
        for i in {1..5}; do
            local recovery_start=$(date +%s.%N)
            if curl -s --max-time 5 "${SERVICES[$critical_service]}/api/health" >/dev/null 2>&1; then
                local recovery_end=$(date +%s.%N)
                local recovery_time=$(echo "$recovery_end - $recovery_start" | bc -l)
                local recovery_ms=$(echo "$recovery_time * 1000" | bc -l | cut -d. -f1)
                recovery_times+=("$recovery_ms")
            fi
            sleep 1
        done
        
        # Analyze results
        local avg_under_load=0
        local avg_recovery=0
        
        if [[ ${#under_load_times[@]} -gt 0 ]]; then
            local sum_load=0
            for time in "${under_load_times[@]}"; do
                sum_load=$((sum_load + time))
            done
            avg_under_load=$((sum_load / ${#under_load_times[@]}))
        fi
        
        if [[ ${#recovery_times[@]} -gt 0 ]]; then
            local sum_recovery=0
            for time in "${recovery_times[@]}"; do
                sum_recovery=$((sum_recovery + time))
            done
            avg_recovery=$((sum_recovery / ${#recovery_times[@]}))
        fi
        
        log_info "Performance analysis:"
        log_info "  Baseline: ${baseline_ms}ms"
        log_info "  Under load: ${avg_under_load}ms"
        log_info "  After recovery: ${avg_recovery}ms"
        
        # Evaluate degradation and recovery
        local degradation_factor=1
        local recovery_factor=1
        
        if [[ $baseline_ms -gt 0 ]]; then
            degradation_factor=$(echo "scale=1; $avg_under_load / $baseline_ms" | bc -l)
            recovery_factor=$(echo "scale=1; $avg_recovery / $baseline_ms" | bc -l)
        fi
        
        # Store load test results
        local load_test_result=$(cat << EOF
{
  "baseline_response_ms": $baseline_ms,
  "under_load_avg_ms": $avg_under_load,
  "recovery_avg_ms": $avg_recovery,
  "degradation_factor": $degradation_factor,
  "recovery_factor": $recovery_factor,
  "load_duration_seconds": 20,
  "concurrent_users": 50
}
EOF
        )
        
        jq --argjson result "$load_test_result" '.chaos_tests.high_load_degradation = $result' "$CHAOS_LOG" > "${CHAOS_LOG}.tmp" && mv "${CHAOS_LOG}.tmp" "$CHAOS_LOG"
        
        # Evaluate success criteria
        if (( $(echo "$recovery_factor < 3" | bc -l) )) && [[ $avg_recovery -lt 2000 ]]; then
            log_pass "System recovered well from high load (recovery factor: $recovery_factor)"
        elif (( $(echo "$recovery_factor < 5" | bc -l) )) && [[ $avg_recovery -lt 5000 ]]; then
            log_pass "System recovery acceptable (recovery factor: $recovery_factor)"
        else
            log_fail "System recovery poor or failed (recovery factor: $recovery_factor)"
        fi
    else
        log_info "$critical_service is not available for load testing"
    fi
}

# Test 4: Cascade Failure Detection
test_cascade_failure_detection() {
    log_header "Cascade Failure Detection and Prevention"
    
    log_test "Multi-service cascade failure simulation"
    
    # Identify service dependencies
    local primary_services=("frontend" "ops-controller")
    local secondary_services=("graph-api" "doc-entities" "verification")
    
    local cascade_detected=false
    local services_affected=0
    
    # Check initial system health
    log_info "Checking initial system health"
    local healthy_services=()
    for service in "${!SERVICES[@]}"; do
        if check_service_health "$service"; then
            healthy_services+=("$service")
        fi
    done
    
    log_info "Initially healthy services: ${#healthy_services[@]}"
    
    # Simulate failure of a critical secondary service
    local target_service=""
    for service in "${secondary_services[@]}"; do
        if [[ " ${healthy_services[*]} " =~ " $service " ]]; then
            target_service="$service"
            break
        fi
    done
    
    if [[ -n "$target_service" ]]; then
        log_info "Simulating failure of $target_service to test cascade prevention"
        
        # Stop the target service
        if stop_docker_service "$target_service"; then
            log_info "$target_service stopped"
            sleep 5
            
            # Check if other services are affected
            local affected_services=()
            for service in "${primary_services[@]}"; do
                if [[ " ${healthy_services[*]} " =~ " $service " ]]; then
                    if ! check_service_health "$service" 10; then
                        affected_services+=("$service")
                        services_affected=$((services_affected + 1))
                    fi
                fi
            done
            
            if [[ $services_affected -gt 0 ]]; then
                cascade_detected=true
                log_info "Cascade failure detected: ${affected_services[*]} affected by $target_service failure"
            else
                log_info "No cascade failure detected - system properly isolated"
            fi
            
            # Restore the service
            start_docker_service "$target_service"
            log_info "$target_service restore initiated"
            
            # Monitor cascade recovery
            local cascade_recovery_time=0
            local max_cascade_recovery=60
            local recovery_start=$(date +%s)
            
            while [[ $cascade_recovery_time -lt $max_cascade_recovery ]]; do
                local all_recovered=true
                
                # Check target service
                if ! check_service_health "$target_service" 5; then
                    all_recovered=false
                fi
                
                # Check affected services
                for service in "${affected_services[@]}"; do
                    if ! check_service_health "$service" 5; then
                        all_recovered=false
                        break
                    fi
                done
                
                if $all_recovered; then
                    cascade_recovery_time=$(($(date +%s) - recovery_start))
                    log_info "System fully recovered from cascade in ${cascade_recovery_time}s"
                    break
                fi
                
                sleep 3
                cascade_recovery_time=$(($(date +%s) - recovery_start))
            done
            
            # Store cascade test results
            local cascade_result=$(cat << EOF
{
  "target_service": "$target_service",
  "cascade_detected": $cascade_detected,
  "services_affected": $services_affected,
  "affected_services": [$(printf '"%s",' "${affected_services[@]}" | sed 's/,$//')]",
  "cascade_recovery_time": $cascade_recovery_time,
  "max_recovery_time": $max_cascade_recovery
}
EOF
            )
            
            jq --argjson result "$cascade_result" '.chaos_tests.cascade_failure = $result' "$CHAOS_LOG" > "${CHAOS_LOG}.tmp" && mv "${CHAOS_LOG}.tmp" "$CHAOS_LOG"
            
            # Evaluate cascade prevention
            if [[ $services_affected -eq 0 ]]; then
                log_pass "Excellent cascade prevention - no services affected"
            elif [[ $services_affected -le 2 ]] && [[ $cascade_recovery_time -le 30 ]]; then
                log_pass "Good cascade management - limited impact and fast recovery"
            else
                log_fail "Poor cascade management - significant impact or slow recovery"
            fi
        else
            log_info "Cannot simulate cascade failure - service manipulation not available"
        fi
    else
        log_info "No suitable target service for cascade testing"
    fi
}

# Generate chaos engineering report
generate_chaos_report() {
    log_header "Chaos Engineering Test Report"
    
    local pass_rate=0
    if [[ $TOTAL_CHAOS_TESTS -gt 0 ]]; then
        pass_rate=$(echo "scale=1; $PASSED_CHAOS_TESTS * 100 / $TOTAL_CHAOS_TESTS" | bc -l)
    fi
    
    # Calculate resilience metrics
    local avg_recovery_time=0
    local successful_recoveries=0
    
    # Extract recovery times from results
    local recovery_times=$(jq -r '.chaos_tests[] | select(.recovery_time_seconds? and .recovery_time_seconds > 0) | .recovery_time_seconds' "$CHAOS_LOG" 2>/dev/null || echo "")
    
    if [[ -n "$recovery_times" ]]; then
        local sum_recovery=0
        local count=0
        while IFS= read -r time; do
            if [[ -n "$time" ]] && [[ "$time" != "null" ]]; then
                sum_recovery=$(echo "$sum_recovery + $time" | bc -l)
                count=$((count + 1))
                if [[ $time -le $RECOVERY_TIMEOUT ]]; then
                    successful_recoveries=$((successful_recoveries + 1))
                fi
            fi
        done <<< "$recovery_times"
        
        if [[ $count -gt 0 ]]; then
            avg_recovery_time=$(echo "scale=1; $sum_recovery / $count" | bc -l)
        fi
    fi
    
    # Store resilience metrics
    local resilience_metrics=$(cat << EOF
{
  "total_tests": $TOTAL_CHAOS_TESTS,
  "passed_tests": $PASSED_CHAOS_TESTS,
  "failed_tests": $FAILED_CHAOS_TESTS,
  "pass_rate": $pass_rate,
  "avg_recovery_time": $avg_recovery_time,
  "successful_recoveries": $successful_recoveries,
  "recovery_timeout": $RECOVERY_TIMEOUT
}
EOF
    )
    
    jq --argjson metrics "$resilience_metrics" '.resilience_metrics = $metrics' "$CHAOS_LOG" > "${CHAOS_LOG}.tmp" && mv "${CHAOS_LOG}.tmp" "$CHAOS_LOG"
    
    # Output report
    log "📊 ${BLUE}Chaos Engineering Results Summary${NC}"
    log "   Total Tests: $TOTAL_CHAOS_TESTS"
    log "   Passed: ${GREEN}$PASSED_CHAOS_TESTS${NC}"
    log "   Failed: ${RED}$FAILED_CHAOS_TESTS${NC}"
    log "   Pass Rate: ${pass_rate}%"
    log "   Average Recovery Time: ${avg_recovery_time}s"
    log "   Successful Recoveries: $successful_recoveries"
    log ""
    log "📋 Chaos Test Categories:"
    log "   🔄 Service Failure Recovery"
    log "   🗄️  Database Connection Loss"
    log "   📈 High Load Degradation"
    log "   ⛓️  Cascade Failure Prevention"
    log ""
    log "📄 Detailed results: $CHAOS_LOG"
    
    # Resilience grade
    local resilience_grade="POOR"
    if [[ $pass_rate -ge 80 ]] && (( $(echo "$avg_recovery_time <= $RECOVERY_TIMEOUT" | bc -l) )); then
        resilience_grade="EXCELLENT"
    elif [[ $pass_rate -ge 60 ]] && (( $(echo "$avg_recovery_time <= $(($RECOVERY_TIMEOUT * 2))" | bc -l) )); then
        resilience_grade="GOOD"
    elif [[ $pass_rate -ge 40 ]]; then
        resilience_grade="ACCEPTABLE"
    fi
    
    case "$resilience_grade" in
        "EXCELLENT") log "${GREEN}🏆 Resilience Grade: EXCELLENT${NC}" ;;
        "GOOD") log "${GREEN}🥉 Resilience Grade: GOOD${NC}" ;;
        "ACCEPTABLE") log "${YELLOW}⚠️  Resilience Grade: ACCEPTABLE${NC}" ;;
        "POOR") log "${RED}❌ Resilience Grade: POOR${NC}" ;;
    esac
    
    # Return appropriate exit code
    if [[ $FAILED_CHAOS_TESTS -eq 0 ]] && [[ $pass_rate -ge 80 ]]; then
        return 0
    elif [[ $pass_rate -ge 50 ]]; then
        return 1
    else
        return 2
    fi
}

# Cleanup function
cleanup_chaos_tests() {
    log_info "Cleaning up chaos test artifacts..."
    
    # Remove any network partitions
    for service in "${!SERVICES[@]}"; do
        remove_network_partition "$service" 2>/dev/null || true
    done
    
    # Ensure all services are started
    for service in "${!DOCKER_SERVICES[@]}"; do
        start_docker_service "$service" >/dev/null 2>&1 || true
    done
    
    # Kill any background processes
    jobs -p | xargs -r kill 2>/dev/null || true
    
    log_info "Chaos test cleanup completed"
}

# Main execution
main() {
    log_header "InfoTerminal Chaos Engineering & Resilience Testing"
    log "Starting chaos engineering tests at $(date)"
    log "Recovery timeout: ${RECOVERY_TIMEOUT}s"
    log "Results log: $CHAOS_LOG"
    
    # Dependencies check
    if ! command -v bc >/dev/null; then
        log "${RED}❌ bc is required but not installed${NC}"
        exit 1
    fi
    
    if ! command -v jq >/dev/null; then
        log "${RED}❌ jq is required but not installed${NC}"
        exit 1
    fi
    
    # Initialize results
    init_chaos_results
    
    # Check if we can manipulate Docker services
    if command -v docker >/dev/null && docker info >/dev/null 2>&1; then
        log_info "Docker available for service manipulation"
    else
        log "${YELLOW}⚠️  Docker not available - some chaos tests will be limited${NC}"
    fi
    
    # Run chaos engineering tests
    test_service_failure_recovery
    test_database_connection_loss
    test_high_load_degradation
    test_cascade_failure_detection
    
    # Generate report and cleanup
    cleanup_chaos_tests
    generate_chaos_report
}

# Handle interruption
trap cleanup_chaos_tests EXIT

# Execute main function
main "$@"
