#!/bin/bash

# load_testing.sh
# InfoTerminal v1.0.0 - Concurrent Load Testing
# Tests system behavior under concurrent user load

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOAD_TEST_LOG="${RESULTS_DIR}/load_test_${TIMESTAMP}.json"

# Service URLs
FRONTEND_URL="${IT_FRONTEND_URL:-http://localhost:3000}"
GRAPH_API_URL="${IT_GRAPH_API_URL:-http://localhost:8403}"
SEARCH_API_URL="${IT_SEARCH_API_URL:-http://localhost:8401}"
DOC_ENTITIES_URL="${IT_DOC_ENTITIES_URL:-http://localhost:8402}"
VERIFICATION_URL="${IT_VERIFICATION_URL:-http://localhost:8617}"

# Load test parameters
MAX_USERS="${IT_LOAD_USERS:-100}"
RAMP_UP_TIME="${IT_RAMP_TIME:-30}"
TEST_DURATION="${IT_TEST_DURATION:-120}"
THINK_TIME="${IT_THINK_TIME:-2}"

# Performance thresholds
MAX_RESPONSE_TIME=5000  # 5 seconds
MAX_ERROR_RATE=5        # 5%
MIN_THROUGHPUT=10       # 10 RPS

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging
log() {
    echo -e "$1" | tee -a "${RESULTS_DIR}/load_test_${TIMESTAMP}.log"
}

# Initialize results
init_load_test_results() {
    mkdir -p "$RESULTS_DIR"
    cat > "$LOAD_TEST_LOG" << 'EOF'
{
  "timestamp": null,
  "configuration": {},
  "scenarios": {},
  "summary": {},
  "system_metrics": {}
}
EOF
    
    local config=$(cat << EOF
{
  "max_users": $MAX_USERS,
  "ramp_up_time": $RAMP_UP_TIME,
  "test_duration": $TEST_DURATION,
  "think_time": $THINK_TIME
}
EOF
    )
    
    jq --arg ts "$(date -Iseconds)" --argjson config "$config" \
        '.timestamp = $ts | .configuration = $config' \
        "$LOAD_TEST_LOG" > "${LOAD_TEST_LOG}.tmp" && mv "${LOAD_TEST_LOG}.tmp" "$LOAD_TEST_LOG"
}

# Simple load generator function
run_user_simulation() {
    local user_id="$1"
    local scenario="$2"
    local duration="$3"
    local output_file="$4"
    
    local requests=0
    local successful=0
    local failed=0
    local total_response_time=0
    local max_response_time=0
    local min_response_time=99999
    
    local start_time=$(date +%s)
    local end_time=$((start_time + duration))
    
    while [[ $(date +%s) -lt $end_time ]]; do
        local request_start=$(date +%s.%N)
        local success=false
        
        case "$scenario" in
            "search")
                if curl -s --max-time 10 "$FRONTEND_URL/api/search?q=test&limit=10" >/dev/null 2>&1; then
                    success=true
                fi
                ;;
            "health")
                if curl -s --max-time 5 "$FRONTEND_URL/api/health" >/dev/null 2>&1; then
                    success=true
                fi
                ;;
            "graph")
                if curl -s --max-time 10 "$GRAPH_API_URL/health" >/dev/null 2>&1; then
                    success=true
                fi
                ;;
            "nlp")
                local nlp_data='{"text":"Test document for load testing","options":{"extract_entities":true}}'
                if curl -s --max-time 15 -X POST -H "Content-Type: application/json" -d "$nlp_data" "$DOC_ENTITIES_URL/extract" >/dev/null 2>&1; then
                    success=true
                fi
                ;;
            "verification")
                local verify_data='{"text":"Test claim for verification","options":{"max_claims":3}}'
                if curl -s --max-time 20 -X POST -H "Content-Type: application/json" -d "$verify_data" "$VERIFICATION_URL/extract-claims" >/dev/null 2>&1; then
                    success=true
                fi
                ;;
        esac
        
        local request_end=$(date +%s.%N)
        local response_time=$(echo "($request_end - $request_start) * 1000" | bc -l)
        local response_time_int=$(echo "$response_time" | cut -d. -f1)
        
        requests=$((requests + 1))
        total_response_time=$(echo "$total_response_time + $response_time" | bc -l)
        
        if (( $(echo "$response_time_int > $max_response_time" | bc -l) )); then
            max_response_time=$response_time_int
        fi
        
        if (( $(echo "$response_time_int < $min_response_time" | bc -l) )); then
            min_response_time=$response_time_int
        fi
        
        if $success; then
            successful=$((successful + 1))
        else
            failed=$((failed + 1))
        fi
        
        # Think time
        sleep "$THINK_TIME"
    done
    
    local avg_response_time=0
    if [[ $requests -gt 0 ]]; then
        avg_response_time=$(echo "scale=2; $total_response_time / $requests" | bc -l)
    fi
    
    local error_rate=0
    if [[ $requests -gt 0 ]]; then
        error_rate=$(echo "scale=2; $failed * 100 / $requests" | bc -l)
    fi
    
    # Write results
    echo "$user_id,$scenario,$requests,$successful,$failed,$avg_response_time,$min_response_time,$max_response_time,$error_rate" > "$output_file"
}

# Load test scenario execution
run_load_test_scenario() {
    local scenario_name="$1"
    local scenario_type="$2"
    local concurrent_users="$3"
    local test_duration="$4"
    
    log "🚀 Running load test: $scenario_name (${concurrent_users} users, ${test_duration}s)"
    
    local pids=()
    local result_files=()
    local start_time=$(date +%s.%N)
    
    # Start concurrent users with ramp-up
    for i in $(seq 1 "$concurrent_users"); do
        local result_file="${RESULTS_DIR}/user_${i}_${scenario_type}_${TIMESTAMP}.tmp"
        result_files+=("$result_file")
        
        # Ramp-up delay
        local ramp_delay=$(echo "scale=2; $i * $RAMP_UP_TIME / $concurrent_users" | bc -l)
        
        (
            sleep "$ramp_delay"
            run_user_simulation "$i" "$scenario_type" "$test_duration" "$result_file"
        ) &
        
        pids+=($!)
        
        # Progress indicator
        if (( i % 10 == 0 )); then
            printf "."
        fi
    done
    
    echo ""
    log "⏳ Waiting for $concurrent_users users to complete..."
    
    # Wait for all users to complete
    for pid in "${pids[@]}"; do
        wait "$pid"
    done
    
    local end_time=$(date +%s.%N)
    local total_test_time=$(echo "$end_time - $start_time" | bc -l)
    
    # Aggregate results
    local total_requests=0
    local total_successful=0
    local total_failed=0
    local total_response_time=0
    local max_response_time=0
    local min_response_time=99999
    local response_times=()
    
    for result_file in "${result_files[@]}"; do
        if [[ -f "$result_file" ]]; then
            IFS=',' read -r user_id scenario requests successful failed avg_rt min_rt max_rt error_rate < "$result_file"
            
            total_requests=$((total_requests + requests))
            total_successful=$((total_successful + successful))
            total_failed=$((total_failed + failed))
            total_response_time=$(echo "$total_response_time + ($avg_rt * $requests)" | bc -l)
            
            if (( $(echo "$max_rt > $max_response_time" | bc -l) )); then
                max_response_time=$max_rt
            fi
            
            if (( $(echo "$min_rt < $min_response_time" | bc -l) )); then
                min_response_time=$min_rt
            fi
            
            rm -f "$result_file"
        fi
    done
    
    # Calculate metrics
    local avg_response_time=0
    local throughput=0
    local error_rate=0
    
    if [[ $total_requests -gt 0 ]]; then
        avg_response_time=$(echo "scale=2; $total_response_time / $total_requests" | bc -l)
        throughput=$(echo "scale=2; $total_requests / $total_test_time" | bc -l)
        error_rate=$(echo "scale=2; $total_failed * 100 / $total_requests" | bc -l)
    fi
    
    # Status assessment
    local status="PASS"
    if (( $(echo "$avg_response_time > $MAX_RESPONSE_TIME" | bc -l) )) || \
       (( $(echo "$error_rate > $MAX_ERROR_RATE" | bc -l) )) || \
       (( $(echo "$throughput < $MIN_THROUGHPUT" | bc -l) )); then
        status="WARN"
    fi
    
    if (( $(echo "$error_rate > 20" | bc -l) )) || (( $(echo "$avg_response_time > 10000" | bc -l) )); then
        status="FAIL"
    fi
    
    # Output results
    case "$status" in
        "PASS") log "${GREEN}✅ $scenario_name: Throughput=${throughput} RPS, Avg RT=${avg_response_time}ms, Error=${error_rate}%${NC}" ;;
        "WARN") log "${YELLOW}⚠️  $scenario_name: Throughput=${throughput} RPS, Avg RT=${avg_response_time}ms, Error=${error_rate}%${NC}" ;;
        "FAIL") log "${RED}❌ $scenario_name: Throughput=${throughput} RPS, Avg RT=${avg_response_time}ms, Error=${error_rate}%${NC}" ;;
    esac
    
    # Store results in JSON
    local scenario_result=$(cat << EOF
{
  "name": "$scenario_name",
  "type": "$scenario_type",
  "concurrent_users": $concurrent_users,
  "test_duration": $test_duration,
  "total_requests": $total_requests,
  "successful_requests": $total_successful,
  "failed_requests": $total_failed,
  "avg_response_time_ms": $avg_response_time,
  "min_response_time_ms": $min_response_time,
  "max_response_time_ms": $max_response_time,
  "throughput_rps": $throughput,
  "error_rate_percent": $error_rate,
  "total_test_time_seconds": $total_test_time,
  "status": "$status"
}
EOF
    )
    
    jq --argjson result "$scenario_result" ".scenarios.\"$scenario_name\" = \$result" "$LOAD_TEST_LOG" > "${LOAD_TEST_LOG}.tmp" && mv "${LOAD_TEST_LOG}.tmp" "$LOAD_TEST_LOG"
    
    return $([ "$status" = "FAIL" ] && echo 1 || echo 0)
}

# System resource monitoring
monitor_system_resources() {
    local monitoring_duration="$1"
    local output_file="${RESULTS_DIR}/system_metrics_${TIMESTAMP}.json"
    
    log "📊 Monitoring system resources for ${monitoring_duration}s..."
    
    local start_time=$(date +%s)
    local end_time=$((start_time + monitoring_duration))
    local samples=0
    local total_cpu=0
    local total_memory=0
    local max_cpu=0
    local max_memory=0
    
    while [[ $(date +%s) -lt $end_time ]]; do
        # CPU usage
        local cpu_usage=0
        if command -v top >/dev/null; then
            cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 2>/dev/null || echo "0")
        elif command -v vmstat >/dev/null; then
            cpu_usage=$(vmstat 1 2 | tail -1 | awk '{print 100 - $15}' 2>/dev/null || echo "0")
        fi
        
        # Memory usage
        local memory_usage=0
        if command -v free >/dev/null; then
            memory_usage=$(free | grep '^Mem:' | awk '{printf "%.1f", $3/$2 * 100.0}' 2>/dev/null || echo "0")
        fi
        
        # Update statistics
        samples=$((samples + 1))
        total_cpu=$(echo "$total_cpu + $cpu_usage" | bc -l 2>/dev/null || echo "$total_cpu")
        total_memory=$(echo "$total_memory + $memory_usage" | bc -l 2>/dev/null || echo "$total_memory")
        
        if (( $(echo "$cpu_usage > $max_cpu" | bc -l 2>/dev/null || echo "0") )); then
            max_cpu=$cpu_usage
        fi
        
        if (( $(echo "$memory_usage > $max_memory" | bc -l 2>/dev/null || echo "0") )); then
            max_memory=$memory_usage
        fi
        
        sleep 2
    done
    
    # Calculate averages
    local avg_cpu=0
    local avg_memory=0
    if [[ $samples -gt 0 ]]; then
        avg_cpu=$(echo "scale=1; $total_cpu / $samples" | bc -l 2>/dev/null || echo "0")
        avg_memory=$(echo "scale=1; $total_memory / $samples" | bc -l 2>/dev/null || echo "0")
    fi
    
    # Store system metrics
    local system_metrics=$(cat << EOF
{
  "monitoring_duration": $monitoring_duration,
  "samples": $samples,
  "cpu": {
    "average": $avg_cpu,
    "maximum": $max_cpu
  },
  "memory": {
    "average": $avg_memory,
    "maximum": $max_memory
  }
}
EOF
    )
    
    jq --argjson metrics "$system_metrics" '.system_metrics = $metrics' "$LOAD_TEST_LOG" > "${LOAD_TEST_LOG}.tmp" && mv "${LOAD_TEST_LOG}.tmp" "$LOAD_TEST_LOG"
    
    log "📈 System metrics - CPU: avg=${avg_cpu}% max=${max_cpu}%, Memory: avg=${avg_memory}% max=${max_memory}%"
}

# Stress testing with gradually increasing load
run_stress_test() {
    log "🔥 Running stress test with gradually increasing load..."
    
    local stress_results=()
    local max_stable_users=0
    
    # Test with increasing user counts
    local user_counts=(10 25 50 75 100)
    if [[ $MAX_USERS -gt 100 ]]; then
        user_counts+=(150 200)
    fi
    
    for users in "${user_counts[@]}"; do
        if [[ $users -le $MAX_USERS ]]; then
            log "🧪 Stress test with $users concurrent users..."
            
            # Start system monitoring in background
            monitor_system_resources 60 &
            local monitor_pid=$!
            
            # Run short stress test
            run_load_test_scenario "Stress_${users}_Users" "health" "$users" 60
            local stress_result=$?
            
            # Stop monitoring
            kill $monitor_pid 2>/dev/null || true
            wait $monitor_pid 2>/dev/null || true
            
            if [[ $stress_result -eq 0 ]]; then
                max_stable_users=$users
                log "${GREEN}✅ System stable at $users concurrent users${NC}"
            else
                log "${YELLOW}⚠️  System degraded at $users concurrent users${NC}"
                break
            fi
            
            # Cool-down period
            log "⏸️  Cool-down period (10s)..."
            sleep 10
        fi
    done
    
    log "📊 Maximum stable concurrent users: $max_stable_users"
    
    # Store stress test summary
    local stress_summary=$(cat << EOF
{
  "max_stable_users": $max_stable_users,
  "test_user_counts": [$(IFS=,; echo "${user_counts[*]}")],
  "degradation_point": $(( max_stable_users + 25 ))
}
EOF
    )
    
    jq --argjson summary "$stress_summary" '.stress_test = $summary' "$LOAD_TEST_LOG" > "${LOAD_TEST_LOG}.tmp" && mv "${LOAD_TEST_LOG}.tmp" "$LOAD_TEST_LOG"
}

# Generate load test summary
generate_load_test_summary() {
    log ""
    log "=================================================================="
    log "${BLUE}Load Test Summary${NC}"
    log "=================================================================="
    
    local total_scenarios=$(jq '.scenarios | length' "$LOAD_TEST_LOG")
    local passed_scenarios=$(jq '[.scenarios[] | select(.status == "PASS")] | length' "$LOAD_TEST_LOG")
    local warned_scenarios=$(jq '[.scenarios[] | select(.status == "WARN")] | length' "$LOAD_TEST_LOG")
    local failed_scenarios=$(jq '[.scenarios[] | select(.status == "FAIL")] | length' "$LOAD_TEST_LOG")
    
    local overall_throughput=0
    local overall_avg_response=0
    local overall_error_rate=0
    
    if [[ $total_scenarios -gt 0 ]]; then
        overall_throughput=$(jq '[.scenarios[].throughput_rps] | add / length' "$LOAD_TEST_LOG" 2>/dev/null | xargs printf "%.1f" || echo "0")
        overall_avg_response=$(jq '[.scenarios[].avg_response_time_ms] | add / length' "$LOAD_TEST_LOG" 2>/dev/null | xargs printf "%.1f" || echo "0")
        overall_error_rate=$(jq '[.scenarios[].error_rate_percent] | add / length' "$LOAD_TEST_LOG" 2>/dev/null | xargs printf "%.1f" || echo "0")
    fi
    
    # System resource summary
    local max_cpu=$(jq '.system_metrics.cpu.maximum // 0' "$LOAD_TEST_LOG")
    local max_memory=$(jq '.system_metrics.memory.maximum // 0' "$LOAD_TEST_LOG")
    
    # Store summary
    local summary=$(cat << EOF
{
  "total_scenarios": $total_scenarios,
  "passed": $passed_scenarios,
  "warned": $warned_scenarios,
  "failed": $failed_scenarios,
  "overall_throughput_rps": $overall_throughput,
  "overall_avg_response_ms": $overall_avg_response,
  "overall_error_rate": $overall_error_rate,
  "max_cpu_usage": $max_cpu,
  "max_memory_usage": $max_memory
}
EOF
    )
    
    jq --argjson summary "$summary" '.summary = $summary' "$LOAD_TEST_LOG" > "${LOAD_TEST_LOG}.tmp" && mv "${LOAD_TEST_LOG}.tmp" "$LOAD_TEST_LOG"
    
    # Output summary
    log "📊 Load Test Results:"
    log "   Total Scenarios: $total_scenarios"
    log "   Passed: ${GREEN}$passed_scenarios${NC}"
    log "   Warned: ${YELLOW}$warned_scenarios${NC}"
    log "   Failed: ${RED}$failed_scenarios${NC}"
    log ""
    log "📈 Performance Metrics:"
    log "   Average Throughput: ${overall_throughput} RPS"
    log "   Average Response Time: ${overall_avg_response}ms"
    log "   Average Error Rate: ${overall_error_rate}%"
    log ""
    log "🖥️  System Resources:"
    log "   Max CPU Usage: ${max_cpu}%"
    log "   Max Memory Usage: ${max_memory}%"
    log ""
    log "📄 Detailed results: $LOAD_TEST_LOG"
    
    # Performance grade
    local grade="POOR"
    if [[ $failed_scenarios -eq 0 ]] && (( $(echo "$overall_error_rate < 2" | bc -l) )); then
        if (( $(echo "$overall_throughput >= 50" | bc -l) )) && (( $(echo "$overall_avg_response < 500" | bc -l) )); then
            grade="EXCELLENT"
        elif (( $(echo "$overall_throughput >= 25" | bc -l) )) && (( $(echo "$overall_avg_response < 1000" | bc -l) )); then
            grade="GOOD"
        else
            grade="ACCEPTABLE"
        fi
    fi
    
    case "$grade" in
        "EXCELLENT") log "${GREEN}🏆 Performance Grade: EXCELLENT${NC}" ;;
        "GOOD") log "${GREEN}🥉 Performance Grade: GOOD${NC}" ;;
        "ACCEPTABLE") log "${YELLOW}⚠️  Performance Grade: ACCEPTABLE${NC}" ;;
        "POOR") log "${RED}❌ Performance Grade: POOR${NC}" ;;
    esac
    
    # Return exit code
    if [[ $failed_scenarios -gt 0 ]]; then
        return 2
    elif [[ $warned_scenarios -gt 0 ]]; then
        return 1
    else
        return 0
    fi
}

# Main execution
main() {
    log "${BLUE}🚀 InfoTerminal Load Testing Suite${NC}"
    log "Configuration: $MAX_USERS users, ${TEST_DURATION}s duration, ${RAMP_UP_TIME}s ramp-up"
    log "Results: $LOAD_TEST_LOG"
    log ""
    
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
    init_load_test_results
    
    # Service availability check
    log "🔍 Checking service availability..."
    if ! curl -s --max-time 5 "$FRONTEND_URL/api/health" >/dev/null 2>&1; then
        log "${RED}❌ Frontend service not available at $FRONTEND_URL${NC}"
        exit 1
    fi
    log "${GREEN}✅ Frontend service available${NC}"
    
    # Run load test scenarios
    log ""
    log "🎯 Starting load test scenarios..."
    
    # Health endpoint load test (baseline)
    run_load_test_scenario "Health_Check_Load" "health" 20 60
    
    # Search functionality load test
    if curl -s --max-time 5 "$SEARCH_API_URL/health" >/dev/null 2>&1 || \
       curl -s --max-time 5 "$FRONTEND_URL/api/search?q=test" >/dev/null 2>&1; then
        run_load_test_scenario "Search_Load" "search" 30 90
    else
        log "${YELLOW}⚠️  Search service not available, skipping search load test${NC}"
    fi
    
    # Graph API load test
    if curl -s --max-time 5 "$GRAPH_API_URL/health" >/dev/null 2>&1; then
        run_load_test_scenario "Graph_API_Load" "graph" 25 60
    else
        log "${YELLOW}⚠️  Graph API not available, skipping graph load test${NC}"
    fi
    
    # NLP service load test (more intensive)
    if curl -s --max-time 5 "$DOC_ENTITIES_URL/health" >/dev/null 2>&1; then
        run_load_test_scenario "NLP_Service_Load" "nlp" 15 120
    else
        log "${YELLOW}⚠️  NLP service not available, skipping NLP load test${NC}"
    fi
    
    # Verification service load test
    if curl -s --max-time 5 "$VERIFICATION_URL/health" >/dev/null 2>&1; then
        run_load_test_scenario "Verification_Load" "verification" 10 90
    else
        log "${YELLOW}⚠️  Verification service not available, skipping verification load test${NC}"
    fi
    
    # Stress testing
    if [[ "${IT_SKIP_STRESS_TEST:-false}" != "true" ]]; then
        run_stress_test
    else
        log "${YELLOW}⚠️  Stress testing skipped (IT_SKIP_STRESS_TEST=true)${NC}"
    fi
    
    # Generate final report
    generate_load_test_summary
}

# Handle cleanup on exit
cleanup_load_test() {
    log "🧹 Cleaning up load test processes..."
    # Kill any remaining background processes
    jobs -p | xargs -r kill 2>/dev/null || true
    # Remove temporary files
    rm -f "${RESULTS_DIR}"/*.tmp 2>/dev/null || true
}

trap cleanup_load_test EXIT

# Execute main function
main "$@"
