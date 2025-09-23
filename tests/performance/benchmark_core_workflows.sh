#!/bin/bash

# benchmark_core_workflows.sh
# InfoTerminal v1.0.0 - Core Workflow Performance Benchmarking
# Tests: Search, Graph, NLP, Verification, Security Workflows

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BENCHMARK_LOG="${RESULTS_DIR}/benchmark_${TIMESTAMP}.json"
BASELINE_FILE="${RESULTS_DIR}/baseline_metrics.json"

# Service URLs
FRONTEND_URL="${IT_FRONTEND_URL:-http://localhost:3000}"
GRAPH_API_URL="${IT_GRAPH_API_URL:-http://localhost:8403}"
SEARCH_API_URL="${IT_SEARCH_API_URL:-http://localhost:8401}"
DOC_ENTITIES_URL="${IT_DOC_ENTITIES_URL:-http://localhost:8402}"
VERIFICATION_URL="${IT_VERIFICATION_URL:-http://localhost:8617}"
NEO4J_HTTP_URL="${IT_NEO4J_HTTP_URL:-http://localhost:7474}"

# Performance Targets
TARGET_API_P95=200    # 200ms P95 for API endpoints
TARGET_SEARCH_P95=500 # 500ms P95 for search queries  
TARGET_GRAPH_P95=1000 # 1s P95 for graph queries
TARGET_NLP_P95=2000   # 2s P95 for NLP processing

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Initialize results structure
init_results() {
    mkdir -p "$RESULTS_DIR"
    cat > "$BENCHMARK_LOG" << 'EOF'
{
  "timestamp": null,
  "git_commit": null,
  "system_info": {},
  "workflows": {},
  "performance_summary": {},
  "regressions": []
}
EOF
    
    # Update timestamp and git info
    jq --arg ts "$(date -Iseconds)" '.timestamp = $ts' "$BENCHMARK_LOG" > "${BENCHMARK_LOG}.tmp" && mv "${BENCHMARK_LOG}.tmp" "$BENCHMARK_LOG"
    
    if git rev-parse HEAD >/dev/null 2>&1; then
        git_commit=$(git rev-parse HEAD)
        jq --arg commit "$git_commit" '.git_commit = $commit' "$BENCHMARK_LOG" > "${BENCHMARK_LOG}.tmp" && mv "${BENCHMARK_LOG}.tmp" "$BENCHMARK_LOG"
    fi
}

# System information collection
collect_system_info() {
    echo "📊 Collecting system information..."
    
    local system_info='{}'
    
    # CPU info
    if command -v nproc >/dev/null; then
        system_info=$(echo "$system_info" | jq --arg cores "$(nproc)" '.cpu_cores = $cores')
    fi
    
    # Memory info
    if command -v free >/dev/null; then
        memory_gb=$(free -g | awk '/^Mem:/ {print $2}')
        system_info=$(echo "$system_info" | jq --arg mem "${memory_gb}GB" '.memory = $mem')
    fi
    
    # Docker info
    if command -v docker >/dev/null && docker info >/dev/null 2>&1; then
        system_info=$(echo "$system_info" | jq '.docker_available = true')
    else
        system_info=$(echo "$system_info" | jq '.docker_available = false')
    fi
    
    # Update results
    jq --argjson info "$system_info" '.system_info = $info' "$BENCHMARK_LOG" > "${BENCHMARK_LOG}.tmp" && mv "${BENCHMARK_LOG}.tmp" "$BENCHMARK_LOG"
}

# HTTP benchmark function
benchmark_http() {
    local name="$1"
    local method="$2"
    local url="$3"
    local data="${4:-}"
    local iterations="${5:-10}"
    local timeout="${6:-30}"
    
    echo "🔄 Benchmarking: $name ($iterations iterations)"
    
    local times=()
    local successful=0
    local failed=0
    
    for i in $(seq 1 "$iterations"); do
        local start_time end_time duration
        start_time=$(date +%s.%N)
        
        if [[ -n "$data" ]]; then
            if curl -s -X "$method" -H "Content-Type: application/json" -d "$data" --max-time "$timeout" "$url" >/dev/null 2>&1; then
                successful=$((successful + 1))
            else
                failed=$((failed + 1))
            fi
        else
            if curl -s -X "$method" --max-time "$timeout" "$url" >/dev/null 2>&1; then
                successful=$((successful + 1))
            else
                failed=$((failed + 1))
            fi
        fi
        
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc -l)
        times+=("$duration")
        
        # Progress indicator
        printf "."
    done
    
    echo ""
    
    # Calculate statistics
    local sum=0
    for time in "${times[@]}"; do
        sum=$(echo "$sum + $time" | bc -l)
    done
    
    local avg=$(echo "scale=3; $sum / ${#times[@]}" | bc -l)
    
    # Sort times for percentile calculation
    IFS=$'\n' sorted_times=($(sort -n <<<"${times[*]}"))
    unset IFS
    
    local p50_idx=$(echo "${#sorted_times[@]} * 50 / 100" | bc)
    local p95_idx=$(echo "${#sorted_times[@]} * 95 / 100" | bc)
    local p99_idx=$(echo "${#sorted_times[@]} * 99 / 100" | bc)
    
    local p50=${sorted_times[$p50_idx]}
    local p95=${sorted_times[$p95_idx]}
    local p99=${sorted_times[$p99_idx]}
    local min=${sorted_times[0]}
    local max=${sorted_times[-1]}
    
    # Convert to milliseconds for readability
    local avg_ms=$(echo "$avg * 1000" | bc -l | xargs printf "%.1f")
    local p50_ms=$(echo "$p50 * 1000" | bc -l | xargs printf "%.1f")
    local p95_ms=$(echo "$p95 * 1000" | bc -l | xargs printf "%.1f")
    local p99_ms=$(echo "$p99 * 1000" | bc -l | xargs printf "%.1f")
    local min_ms=$(echo "$min * 1000" | bc -l | xargs printf "%.1f")
    local max_ms=$(echo "$max * 1000" | bc -l | xargs printf "%.1f")
    
    local success_rate=$(echo "scale=1; $successful * 100 / ($successful + $failed)" | bc -l)
    
    # Status based on P95 target
    local status="PASS"
    local p95_target_check=false
    
    case "$name" in
        *"API"*|*"Health"*)
            p95_target_check=$(echo "$p95_ms <= $TARGET_API_P95" | bc -l)
            ;;
        *"Search"*)
            p95_target_check=$(echo "$p95_ms <= $TARGET_SEARCH_P95" | bc -l)
            ;;
        *"Graph"*)
            p95_target_check=$(echo "$p95_ms <= $TARGET_GRAPH_P95" | bc -l)
            ;;
        *"NLP"*|*"Entities"*)
            p95_target_check=$(echo "$p95_ms <= $TARGET_NLP_P95" | bc -l)
            ;;
    esac
    
    if [[ "$p95_target_check" == "0" ]] || [[ "$success_rate" < "90.0" ]]; then
        status="WARN"
    fi
    
    if [[ "$success_rate" < "50.0" ]]; then
        status="FAIL"
    fi
    
    # Output results
    case "$status" in
        "PASS") echo -e "${GREEN}✅ $name: P95=${p95_ms}ms, Success=${success_rate}%${NC}" ;;
        "WARN") echo -e "${YELLOW}⚠️  $name: P95=${p95_ms}ms, Success=${success_rate}%${NC}" ;;
        "FAIL") echo -e "${RED}❌ $name: P95=${p95_ms}ms, Success=${success_rate}%${NC}" ;;
    esac
    
    # Store results in JSON
    local result=$(cat << EOF
{
  "name": "$name",
  "method": "$method",
  "url": "$url",
  "iterations": $iterations,
  "successful": $successful,
  "failed": $failed,
  "success_rate": $success_rate,
  "avg_ms": $avg_ms,
  "min_ms": $min_ms,
  "max_ms": $max_ms,
  "p50_ms": $p50_ms,
  "p95_ms": $p95_ms,
  "p99_ms": $p99_ms,
  "status": "$status"
}
EOF
    )
    
    # Update JSON file
    jq --argjson result "$result" ".workflows.\"$name\" = \$result" "$BENCHMARK_LOG" > "${BENCHMARK_LOG}.tmp" && mv "${BENCHMARK_LOG}.tmp" "$BENCHMARK_LOG"
}

# Concurrent load test
benchmark_concurrent() {
    local name="$1"
    local url="$2"
    local concurrent="${3:-5}"
    local requests_per_worker="${4:-10}"
    
    echo "🚀 Concurrent load test: $name (${concurrent} workers, ${requests_per_worker} requests each)"
    
    local pids=()
    local temp_results=()
    local start_time end_time
    
    start_time=$(date +%s.%N)
    
    # Start concurrent workers
    for i in $(seq 1 "$concurrent"); do
        local temp_file="${RESULTS_DIR}/concurrent_${i}_${TIMESTAMP}.tmp"
        temp_results+=("$temp_file")
        
        (
            local worker_successful=0
            local worker_failed=0
            local worker_times=()
            
            for j in $(seq 1 "$requests_per_worker"); do
                local req_start req_end req_duration
                req_start=$(date +%s.%N)
                
                if curl -s --max-time 10 "$url" >/dev/null 2>&1; then
                    worker_successful=$((worker_successful + 1))
                else
                    worker_failed=$((worker_failed + 1))
                fi
                
                req_end=$(date +%s.%N)
                req_duration=$(echo "$req_end - $req_start" | bc -l)
                worker_times+=("$req_duration")
            done
            
            # Write worker results
            echo "$worker_successful,$worker_failed,${worker_times[*]}" > "$temp_file"
        ) &
        
        pids+=($!)
    done
    
    # Wait for all workers
    for pid in "${pids[@]}"; do
        wait "$pid"
    done
    
    end_time=$(date +%s.%N)
    local total_duration=$(echo "$end_time - $start_time" | bc -l)
    
    # Aggregate results
    local total_successful=0
    local total_failed=0
    local all_times=()
    
    for temp_file in "${temp_results[@]}"; do
        if [[ -f "$temp_file" ]]; then
            IFS=',' read -r successful failed times <<< "$(cat "$temp_file")"
            total_successful=$((total_successful + successful))
            total_failed=$((total_failed + failed))
            
            # Parse times
            IFS=' ' read -ra worker_times <<< "$times"
            all_times+=("${worker_times[@]}")
            
            rm -f "$temp_file"
        fi
    done
    
    local total_requests=$((total_successful + total_failed))
    local rps=$(echo "scale=1; $total_requests / $total_duration" | bc -l)
    local success_rate=$(echo "scale=1; $total_successful * 100 / $total_requests" | bc -l)
    
    # Calculate percentiles for concurrent test
    if [[ ${#all_times[@]} -gt 0 ]]; then
        IFS=$'\n' sorted_concurrent_times=($(sort -n <<<"${all_times[*]}"))
        unset IFS
        
        local p95_concurrent_idx=$(echo "${#sorted_concurrent_times[@]} * 95 / 100" | bc)
        local p95_concurrent=${sorted_concurrent_times[$p95_concurrent_idx]}
        local p95_concurrent_ms=$(echo "$p95_concurrent * 1000" | bc -l | xargs printf "%.1f")
        
        echo -e "🔥 Concurrent Results: RPS=${rps}, P95=${p95_concurrent_ms}ms, Success=${success_rate}%"
        
        # Store concurrent results
        local concurrent_result=$(cat << EOF
{
  "name": "${name}_concurrent",
  "workers": $concurrent,
  "requests_per_worker": $requests_per_worker,
  "total_requests": $total_requests,
  "total_duration_seconds": $total_duration,
  "requests_per_second": $rps,
  "success_rate": $success_rate,
  "p95_ms": $p95_concurrent_ms
}
EOF
        )
        
        jq --argjson result "$concurrent_result" ".workflows.\"${name}_concurrent\" = \$result" "$BENCHMARK_LOG" > "${BENCHMARK_LOG}.tmp" && mv "${BENCHMARK_LOG}.tmp" "$BENCHMARK_LOG"
    fi
}

# Workflow-specific benchmarks
benchmark_search_workflow() {
    echo -e "\n${BLUE}🔍 Search Workflow Benchmarking${NC}"
    
    # Basic search health
    benchmark_http "Search API Health" "GET" "$SEARCH_API_URL/health" "" 5 10
    
    # Search query (if search service exists)
    if curl -s --max-time 5 "$SEARCH_API_URL/health" >/dev/null 2>&1; then
        local search_query='{"query":"climate change","limit":10,"filters":{}}'
        benchmark_http "Search Query" "POST" "$SEARCH_API_URL/search" "$search_query" 10 15
        
        # Complex search
        local complex_query='{"query":"climate change human activities","limit":50,"filters":{"source_type":"web","date_range":"2023-2024"},"sort":"relevance"}'
        benchmark_http "Complex Search" "POST" "$SEARCH_API_URL/search" "$complex_query" 5 20
    else
        echo "⚠️  Search API not available, skipping search benchmarks"
    fi
    
    # Frontend search integration
    benchmark_http "Frontend Search" "GET" "$FRONTEND_URL/api/search?q=test&limit=10" "" 10 15
}

benchmark_graph_workflow() {
    echo -e "\n${BLUE}🕸️ Graph Workflow Benchmarking${NC}"
    
    # Graph API health
    benchmark_http "Graph API Health" "GET" "$GRAPH_API_URL/health" "" 5 10
    
    # Node operations
    if curl -s --max-time 5 "$GRAPH_API_URL/health" >/dev/null 2>&1; then
        # Get nodes
        benchmark_http "Graph Get Nodes" "GET" "$GRAPH_API_URL/nodes?limit=10" "" 10 15
        
        # Node creation (if writes allowed)
        local node_data='{"name":"benchmark_test_node","type":"test","properties":{"created_by":"benchmark","timestamp":"'$(date -Iseconds)'"}}'
        benchmark_http "Graph Create Node" "POST" "$GRAPH_API_URL/nodes" "$node_data" 5 20
        
        # Graph analytics
        benchmark_http "Graph Analytics" "GET" "$GRAPH_API_URL/analytics/summary" "" 5 25
        
        # Concurrent graph operations
        benchmark_concurrent "Graph API" "$GRAPH_API_URL/health" 5 10
    else
        echo "⚠️  Graph API not available, skipping graph benchmarks"
    fi
}

benchmark_nlp_workflow() {
    echo -e "\n${BLUE}🧠 NLP Workflow Benchmarking${NC}"
    
    # Doc entities health
    benchmark_http "Doc Entities Health" "GET" "$DOC_ENTITIES_URL/health" "" 5 10
    
    if curl -s --max-time 5 "$DOC_ENTITIES_URL/health" >/dev/null 2>&1; then
        # Entity extraction
        local text_sample='{"text":"Climate change represents one of the most pressing challenges of our time. Recent studies indicate that global temperatures have risen by approximately 1.1 degrees Celsius since the late 19th century.","options":{"extract_entities":true,"extract_relations":true}}'
        benchmark_http "NLP Entity Extraction" "POST" "$DOC_ENTITIES_URL/extract" "$text_sample" 5 30
        
        # Large document processing
        local large_text='{"text":"'$(printf 'Climate change represents one of the most pressing challenges of our time. %.0s' {1..100})'","options":{"extract_entities":true}}'
        benchmark_http "NLP Large Document" "POST" "$DOC_ENTITIES_URL/extract" "$large_text" 3 60
    else
        echo "⚠️  Doc Entities API not available, skipping NLP benchmarks"
    fi
}

benchmark_verification_workflow() {
    echo -e "\n${BLUE}🔍 Verification Workflow Benchmarking${NC}"
    
    # Verification service health
    benchmark_http "Verification Health" "GET" "$VERIFICATION_URL/health" "" 5 10
    
    if curl -s --max-time 5 "$VERIFICATION_URL/health" >/dev/null 2>&1; then
        # Claim extraction
        local claim_request='{"text":"Climate change is caused by human activities. Global temperatures have increased by 1.1 degrees Celsius.","confidence_threshold":0.7,"max_claims":5}'
        benchmark_http "Claim Extraction" "POST" "$VERIFICATION_URL/extract-claims" "$claim_request" 5 25
        
        # Evidence retrieval
        local evidence_request='{"claim":"Climate change is caused by human activities","max_sources":3,"source_types":["web","wikipedia"]}'
        benchmark_http "Evidence Retrieval" "POST" "$VERIFICATION_URL/find-evidence" "$evidence_request" 3 45
        
        # Stance classification
        local stance_request='{"claim":"Climate change is caused by human activities","evidence":"Scientific consensus confirms that human activities are the primary driver of climate change"}'
        benchmark_http "Stance Classification" "POST" "$VERIFICATION_URL/classify-stance" "$stance_request" 5 20
    else
        echo "⚠️  Verification API not available, skipping verification benchmarks"
    fi
    
    # Frontend verification integration
    benchmark_http "Frontend Verification" "GET" "$FRONTEND_URL/api/verification/status" "" 5 15
}

benchmark_security_workflow() {
    echo -e "\n${BLUE}🔒 Security Workflow Benchmarking${NC}"
    
    # Security status
    benchmark_http "Security Status" "GET" "$FRONTEND_URL/api/security/status" "" 5 15
    
    # Incognito mode operations
    local incognito_request='{"sessionId":"benchmark_test","autoWipeMinutes":5,"memoryOnlyMode":true}'
    benchmark_http "Incognito Start" "POST" "$FRONTEND_URL/api/security/incognito/start" "$incognito_request" 5 20
    
    # Session cleanup is handled by the service automatically for benchmark sessions
}

# Database performance tests
benchmark_database_performance() {
    echo -e "\n${BLUE}🗄️ Database Performance Benchmarking${NC}"
    
    # Neo4j HTTP API (if available)
    if curl -s --max-time 5 "$NEO4J_HTTP_URL" >/dev/null 2>&1; then
        benchmark_http "Neo4j Health" "GET" "$NEO4J_HTTP_URL" "" 5 10
        
        # Simple Cypher query via HTTP
        local cypher_query='{"statements":[{"statement":"MATCH (n) RETURN count(n) as node_count LIMIT 1"}]}'
        benchmark_http "Neo4j Node Count" "POST" "$NEO4J_HTTP_URL/db/data/transaction/commit" "$cypher_query" 5 15
    else
        echo "⚠️  Neo4j HTTP API not available, skipping database benchmarks"
    fi
    
    # Test graph API database operations
    if curl -s --max-time 5 "$GRAPH_API_URL/health" >/dev/null 2>&1; then
        benchmark_http "Database via Graph API" "GET" "$GRAPH_API_URL/stats" "" 5 20
    fi
}

# Performance regression detection
check_performance_regressions() {
    echo -e "\n${BLUE}📈 Performance Regression Analysis${NC}"
    
    if [[ ! -f "$BASELINE_FILE" ]]; then
        echo "ℹ️  No baseline file found, creating baseline from current results"
        cp "$BENCHMARK_LOG" "$BASELINE_FILE"
        echo "✅ Baseline created: $BASELINE_FILE"
        return 0
    fi
    
    echo "🔄 Comparing against baseline..."
    
    local regressions=[]
    local improvements=[]
    
    # Compare key metrics
    local current_workflows=$(jq -r '.workflows | keys[]' "$BENCHMARK_LOG")
    
    while IFS= read -r workflow; do
        local current_p95=$(jq -r ".workflows.\"$workflow\".p95_ms // \"null\"" "$BENCHMARK_LOG")
        local baseline_p95=$(jq -r ".workflows.\"$workflow\".p95_ms // \"null\"" "$BASELINE_FILE")
        
        if [[ "$current_p95" != "null" ]] && [[ "$baseline_p95" != "null" ]]; then
            local change_percent=$(echo "scale=1; ($current_p95 - $baseline_p95) * 100 / $baseline_p95" | bc -l)
            
            # Regression threshold: 20% slower
            if (( $(echo "$change_percent > 20" | bc -l) )); then
                local regression="{\"workflow\":\"$workflow\",\"current_p95\":$current_p95,\"baseline_p95\":$baseline_p95,\"change_percent\":$change_percent}"
                regressions=$(echo "$regressions" | jq ". + [$regression]")
                echo -e "${RED}📉 REGRESSION: $workflow: ${current_p95}ms vs ${baseline_p95}ms (+${change_percent}%)${NC}"
            elif (( $(echo "$change_percent < -10" | bc -l) )); then
                local improvement="{\"workflow\":\"$workflow\",\"current_p95\":$current_p95,\"baseline_p95\":$baseline_p95,\"change_percent\":$change_percent}"
                improvements=$(echo "$improvements" | jq ". + [$improvement]")
                echo -e "${GREEN}📈 IMPROVEMENT: $workflow: ${current_p95}ms vs ${baseline_p95}ms (${change_percent}%)${NC}"
            fi
        fi
    done <<< "$current_workflows"
    
    # Update results with regression analysis
    jq --argjson regressions "$regressions" '.regressions = $regressions' "$BENCHMARK_LOG" > "${BENCHMARK_LOG}.tmp" && mv "${BENCHMARK_LOG}.tmp" "$BENCHMARK_LOG"
    
    if [[ $(echo "$regressions" | jq 'length') -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  Performance regressions detected!${NC}"
        return 1
    else
        echo -e "${GREEN}✅ No performance regressions detected${NC}"
        return 0
    fi
}

# Generate performance summary
generate_performance_summary() {
    echo -e "\n${BLUE}📊 Performance Summary${NC}"
    
    local total_workflows=$(jq '.workflows | length' "$BENCHMARK_LOG")
    local passed_workflows=$(jq '[.workflows[] | select(.status == "PASS")] | length' "$BENCHMARK_LOG")
    local warned_workflows=$(jq '[.workflows[] | select(.status == "WARN")] | length' "$BENCHMARK_LOG")
    local failed_workflows=$(jq '[.workflows[] | select(.status == "FAIL")] | length' "$BENCHMARK_LOG")
    
    local pass_rate=0
    if [[ $total_workflows -gt 0 ]]; then
        pass_rate=$(echo "scale=1; $passed_workflows * 100 / $total_workflows" | bc -l)
    fi
    
    local summary=$(cat << EOF
{
  "total_workflows": $total_workflows,
  "passed": $passed_workflows,
  "warned": $warned_workflows,
  "failed": $failed_workflows,
  "pass_rate": $pass_rate
}
EOF
    )
    
    jq --argjson summary "$summary" '.performance_summary = $summary' "$BENCHMARK_LOG" > "${BENCHMARK_LOG}.tmp" && mv "${BENCHMARK_LOG}.tmp" "$BENCHMARK_LOG"
    
    echo "📋 Total Benchmarks: $total_workflows"
    echo -e "✅ Passed: ${GREEN}$passed_workflows${NC}"
    echo -e "⚠️  Warned: ${YELLOW}$warned_workflows${NC}"
    echo -e "❌ Failed: ${RED}$failed_workflows${NC}"
    echo "📊 Pass Rate: ${pass_rate}%"
    
    # Performance grade
    if (( $(echo "$pass_rate >= 90" | bc -l) )); then
        echo -e "${GREEN}🏆 Performance Grade: EXCELLENT${NC}"
    elif (( $(echo "$pass_rate >= 75" | bc -l) )); then
        echo -e "${YELLOW}🥉 Performance Grade: GOOD${NC}"
    elif (( $(echo "$pass_rate >= 60" | bc -l) )); then
        echo -e "${YELLOW}⚠️  Performance Grade: ACCEPTABLE${NC}"
    else
        echo -e "${RED}❌ Performance Grade: POOR${NC}"
    fi
}

# Main execution
main() {
    echo -e "${BLUE}🚀 InfoTerminal Performance Benchmark Suite${NC}"
    echo "Timestamp: $(date)"
    echo "Results: $BENCHMARK_LOG"
    echo ""
    
    # Initialize
    init_results
    collect_system_info
    
    # Run workflow benchmarks
    benchmark_search_workflow
    benchmark_graph_workflow  
    benchmark_nlp_workflow
    benchmark_verification_workflow
    benchmark_security_workflow
    benchmark_database_performance
    
    # Analysis
    generate_performance_summary
    check_performance_regressions
    
    echo ""
    echo -e "${GREEN}✅ Performance benchmarking completed${NC}"
    echo "📄 Detailed results: $BENCHMARK_LOG"
    
    # Return appropriate exit code
    local failed_count=$(jq '.performance_summary.failed' "$BENCHMARK_LOG")
    local regression_count=$(jq '.regressions | length' "$BENCHMARK_LOG")
    
    if [[ $failed_count -gt 0 ]] || [[ $regression_count -gt 0 ]]; then
        exit 1
    else
        exit 0
    fi
}

# Handle dependencies
if ! command -v jq >/dev/null; then
    echo "❌ jq is required but not installed. Please install jq."
    exit 1
fi

if ! command -v bc >/dev/null; then
    echo "❌ bc is required but not installed. Please install bc."
    exit 1
fi

if ! command -v curl >/dev/null; then
    echo "❌ curl is required but not installed. Please install curl."
    exit 1
fi

# Run main function
main "$@"
