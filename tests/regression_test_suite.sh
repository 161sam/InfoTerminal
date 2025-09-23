#!/bin/bash

# regression_test_suite.sh
# InfoTerminal v1.0.0 - Automated Regression Testing
# Detects: Performance, Functionality, API Breaking Changes

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
BASELINES_DIR="${SCRIPT_DIR}/baselines"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REGRESSION_LOG="${RESULTS_DIR}/regression_${TIMESTAMP}.json"

# Regression thresholds
PERFORMANCE_THRESHOLD=20  # 20% performance degradation threshold
API_BREAKING_THRESHOLD=1  # Any breaking change is critical
FUNCTIONALITY_THRESHOLD=5 # 5% functionality regression threshold

# Git comparison
BASELINE_COMMIT="${IT_BASELINE_COMMIT:-HEAD~1}"
CURRENT_COMMIT="${IT_CURRENT_COMMIT:-HEAD}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging
log() {
    echo -e "$1" | tee -a "${RESULTS_DIR}/regression_${TIMESTAMP}.log"
}

log_header() {
    echo ""
    echo "=================================================================="
    log "${BLUE}$1${NC}"
    echo "=================================================================="
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

# Initialize regression testing
init_regression_testing() {
    log_header "InfoTerminal Regression Testing Suite"
    log "Comparing: $BASELINE_COMMIT → $CURRENT_COMMIT"
    log "Thresholds: Performance=${PERFORMANCE_THRESHOLD}%, API Breaking=${API_BREAKING_THRESHOLD}, Functionality=${FUNCTIONALITY_THRESHOLD}%"
    
    mkdir -p "$RESULTS_DIR" "$BASELINES_DIR"
    
    # Initialize results structure
    cat > "$REGRESSION_LOG" << 'EOF'
{
  "timestamp": null,
  "baseline_commit": null,
  "current_commit": null,
  "regression_summary": {
    "performance_regressions": 0,
    "api_breaking_changes": 0,
    "functionality_regressions": 0,
    "total_regressions": 0
  },
  "performance_analysis": {},
  "api_analysis": {},
  "functionality_analysis": {},
  "recommendations": []
}
EOF
    
    # Update metadata
    jq --arg ts "$(date -Iseconds)" \
       --arg baseline "$BASELINE_COMMIT" \
       --arg current "$CURRENT_COMMIT" \
       '.timestamp = $ts | .baseline_commit = $baseline | .current_commit = $current' \
       "$REGRESSION_LOG" > "${REGRESSION_LOG}.tmp" && mv "${REGRESSION_LOG}.tmp" "$REGRESSION_LOG"
}

# Performance regression analysis
analyze_performance_regressions() {
    log_header "Performance Regression Analysis"
    
    local baseline_file="$BASELINES_DIR/performance_baseline.json"
    local current_file="${RESULTS_DIR}/current_performance.json"
    local regressions=0
    
    # Run current performance benchmarks
    log_info "Running current performance benchmarks..."
    if [[ -f "$SCRIPT_DIR/performance/benchmark_core_workflows.sh" ]]; then
        cd "$SCRIPT_DIR/performance"
        if ./benchmark_core_workflows.sh >/dev/null 2>&1; then
            local latest_benchmark=$(ls -t results/benchmark_*.json 2>/dev/null | head -1 || echo "")
            if [[ -n "$latest_benchmark" ]]; then
                cp "$latest_benchmark" "$current_file"
                log_success "Current performance benchmarks completed"
            else
                log_error "No current performance results found"
                return 1
            fi
        else
            log_error "Current performance benchmarks failed"
            return 1
        fi
    else
        log_error "Performance benchmark script not found"
        return 1
    fi
    
    # Load or create baseline
    if [[ ! -f "$baseline_file" ]]; then
        log_warn "No performance baseline found, creating from current results"
        cp "$current_file" "$baseline_file"
        log_success "Performance baseline created"
        return 0
    fi
    
    log_info "Comparing performance against baseline..."
    
    # Analyze each workflow
    local workflows=$(jq -r '.workflows | keys[]' "$current_file" 2>/dev/null || echo "")
    
    while IFS= read -r workflow; do
        [[ -z "$workflow" ]] && continue
        
        local current_p95=$(jq -r ".workflows.\"$workflow\".p95_ms // 0" "$current_file")
        local baseline_p95=$(jq -r ".workflows.\"$workflow\".p95_ms // 0" "$baseline_file")
        
        if [[ "$current_p95" != "0" ]] && [[ "$baseline_p95" != "0" ]]; then
            local degradation=$(echo "scale=1; ($current_p95 - $baseline_p95) * 100 / $baseline_p95" | bc -l 2>/dev/null || echo "0")
            
            if (( $(echo "$degradation > $PERFORMANCE_THRESHOLD" | bc -l 2>/dev/null || echo "0") )); then
                regressions=$((regressions + 1))
                log_error "Performance regression in $workflow: ${current_p95}ms vs ${baseline_p95}ms (+${degradation}%)"
                
                # Store regression details
                local regression_detail=$(cat << EOF
{
  "workflow": "$workflow",
  "current_p95": $current_p95,
  "baseline_p95": $baseline_p95,
  "degradation_percent": $degradation,
  "severity": "$(if (( $(echo "$degradation > 50" | bc -l 2>/dev/null || echo "0") )); then echo "critical"; elif (( $(echo "$degradation > 30" | bc -l 2>/dev/null || echo "0") )); then echo "high"; else echo "medium"; fi)"
}
EOF
                )
                
                jq --argjson detail "$regression_detail" \
                   ".performance_analysis.regressions += [\$detail]" \
                   "$REGRESSION_LOG" > "${REGRESSION_LOG}.tmp" && mv "${REGRESSION_LOG}.tmp" "$REGRESSION_LOG"
            else
                log_info "✓ $workflow: ${current_p95}ms vs ${baseline_p95}ms (${degradation}%)"
            fi
        fi
    done <<< "$workflows"
    
    # Update regression count
    jq --argjson count "$regressions" \
       '.regression_summary.performance_regressions = $count' \
       "$REGRESSION_LOG" > "${REGRESSION_LOG}.tmp" && mv "${REGRESSION_LOG}.tmp" "$REGRESSION_LOG"
    
    if [[ $regressions -eq 0 ]]; then
        log_success "No performance regressions detected"
    else
        log_warn "$regressions performance regressions detected"
    fi
    
    return $regressions
}

# API breaking changes analysis
analyze_api_breaking_changes() {
    log_header "API Breaking Changes Analysis"
    
    local breaking_changes=0
    local api_baseline="$BASELINES_DIR/api_baseline.json"
    local api_current="${RESULTS_DIR}/api_current.json"
    
    # Extract current API schema
    log_info "Extracting current API schema..."
    if extract_api_schema "$api_current"; then
        log_success "Current API schema extracted"
    else
        log_error "Failed to extract current API schema"
        return 1
    fi
    
    # Load or create baseline
    if [[ ! -f "$api_baseline" ]]; then
        log_warn "No API baseline found, creating from current schema"
        cp "$api_current" "$api_baseline"
        log_success "API baseline created"
        return 0
    fi
    
    log_info "Analyzing API changes..."
    
    # Check for removed endpoints
    local removed_endpoints=$(jq -r '
        .baseline.endpoints as $baseline |
        .current.endpoints as $current |
        $baseline | keys[] | select(. as $key | $current | has($key) | not)
    ' <(jq -n --slurpfile baseline "$api_baseline" --slurpfile current "$api_current" \
        '{baseline: $baseline[0], current: $current[0]}') 2>/dev/null || echo "")
    
    while IFS= read -r endpoint; do
        [[ -z "$endpoint" ]] && continue
        breaking_changes=$((breaking_changes + 1))
        log_error "BREAKING: Endpoint removed: $endpoint"
        
        local change_detail=$(cat << EOF
{
  "type": "endpoint_removed",
  "endpoint": "$endpoint",
  "severity": "critical",
  "description": "API endpoint was removed"
}
EOF
        )
        
        jq --argjson detail "$change_detail" \
           ".api_analysis.breaking_changes += [\$detail]" \
           "$REGRESSION_LOG" > "${REGRESSION_LOG}.tmp" && mv "${REGRESSION_LOG}.tmp" "$REGRESSION_LOG"
    done <<< "$removed_endpoints"
    
    # Check for changed response schemas
    local changed_schemas=$(jq -r '
        .baseline.endpoints as $baseline |
        .current.endpoints as $current |
        $baseline | keys[] | select(. as $key | 
            $current | has($key) and 
            ($baseline[$key].response_schema != $current[$key].response_schema)
        )
    ' <(jq -n --slurpfile baseline "$api_baseline" --slurpfile current "$api_current" \
        '{baseline: $baseline[0], current: $current[0]}') 2>/dev/null || echo "")
    
    while IFS= read -r endpoint; do
        [[ -z "$endpoint" ]] && continue
        breaking_changes=$((breaking_changes + 1))
        log_error "BREAKING: Response schema changed: $endpoint"
        
        local change_detail=$(cat << EOF
{
  "type": "schema_changed",
  "endpoint": "$endpoint",
  "severity": "high",
  "description": "Response schema modified"
}
EOF
        )
        
        jq --argjson detail "$change_detail" \
           ".api_analysis.breaking_changes += [\$detail]" \
           "$REGRESSION_LOG" > "${REGRESSION_LOG}.tmp" && mv "${REGRESSION_LOG}.tmp" "$REGRESSION_LOG"
    done <<< "$changed_schemas"
    
    # Update breaking changes count
    jq --argjson count "$breaking_changes" \
       '.regression_summary.api_breaking_changes = $count' \
       "$REGRESSION_LOG" > "${REGRESSION_LOG}.tmp" && mv "${REGRESSION_LOG}.tmp" "$REGRESSION_LOG"
    
    if [[ $breaking_changes -eq 0 ]]; then
        log_success "No API breaking changes detected"
    else
        log_error "$breaking_changes API breaking changes detected"
    fi
    
    return $breaking_changes
}

# Extract API schema for comparison
extract_api_schema() {
    local output_file="$1"
    local frontend_url="${IT_FRONTEND_URL:-http://localhost:3000}"
    local graph_api_url="${IT_GRAPH_API_URL:-http://localhost:8403}"
    
    # Check if services are available
    if ! curl -s --max-time 5 "$frontend_url/api/health" >/dev/null 2>&1; then
        log_warn "Frontend not available for API schema extraction"
        return 1
    fi
    
    # Extract API endpoints and schemas
    cat > "$output_file" << 'EOF'
{
  "extracted_at": null,
  "endpoints": {}
}
EOF
    
    # Update timestamp
    jq --arg ts "$(date -Iseconds)" '.extracted_at = $ts' "$output_file" > "${output_file}.tmp" && mv "${output_file}.tmp" "$output_file"
    
    # Common API endpoints to check
    local endpoints=(
        "GET:/api/health"
        "GET:/api/search"
        "POST:/api/verification/extract-claims"
        "POST:/api/verification/find-evidence"
        "GET:/api/security/status"
        "GET:$graph_api_url/health"
        "GET:$graph_api_url/nodes"
        "POST:$graph_api_url/nodes"
    )
    
    for endpoint_spec in "${endpoints[@]}"; do
        local method="${endpoint_spec%%:*}"
        local path="${endpoint_spec#*:}"
        local full_url
        
        if [[ "$path" =~ ^http ]]; then
            full_url="$path"
        else
            full_url="$frontend_url$path"
        fi
        
        # Test endpoint and extract response schema
        local response_code
        local response_body
        
        case "$method" in
            "GET")
                response_code=$(curl -s -w "%{http_code}" -o /tmp/api_response "$full_url" 2>/dev/null || echo "000")
                ;;
            "POST")
                response_code=$(curl -s -w "%{http_code}" -o /tmp/api_response \
                    -X POST -H "Content-Type: application/json" \
                    -d '{"test": true}' "$full_url" 2>/dev/null || echo "000")
                ;;
        esac
        
        if [[ -f /tmp/api_response ]]; then
            response_body=$(cat /tmp/api_response 2>/dev/null || echo "{}")
            rm -f /tmp/api_response
        else
            response_body="{}"
        fi
        
        # Store endpoint information
        local endpoint_info=$(cat << EOF
{
  "method": "$method",
  "path": "$path",
  "response_code": "$response_code",
  "response_schema": $(echo "$response_body" | jq -c 'keys' 2>/dev/null || echo "[]"),
  "available": $(if [[ "$response_code" =~ ^[2-4] ]]; then echo "true"; else echo "false"; fi)
}
EOF
        )
        
        jq --arg key "${method}:${path}" --argjson info "$endpoint_info" \
           '.endpoints[$key] = $info' \
           "$output_file" > "${output_file}.tmp" && mv "${output_file}.tmp" "$output_file"
    done
    
    return 0
}

# Functionality regression analysis
analyze_functionality_regressions() {
    log_header "Functionality Regression Analysis"
    
    local functionality_regressions=0
    local integration_baseline="$BASELINES_DIR/integration_baseline.json"
    local integration_current="${RESULTS_DIR}/integration_current.json"
    
    # Run current integration tests
    log_info "Running current integration tests..."
    if [[ -f "$SCRIPT_DIR/integration/integration_workflow_tests.sh" ]]; then
        cd "$SCRIPT_DIR/integration"
        if timeout 600 ./integration_workflow_tests.sh >/dev/null 2>&1; then
            # Extract results from log
            local latest_log=$(ls -t results/integration_*.log 2>/dev/null | head -1 || echo "")
            if [[ -n "$latest_log" ]]; then
                extract_integration_results "$latest_log" "$integration_current"
                log_success "Current integration tests completed"
            else
                log_error "No current integration results found"
                return 1
            fi
        else
            log_error "Current integration tests failed"
            return 1
        fi
    else
        log_error "Integration test script not found"
        return 1
    fi
    
    # Load or create baseline
    if [[ ! -f "$integration_baseline" ]]; then
        log_warn "No functionality baseline found, creating from current results"
        cp "$integration_current" "$integration_baseline"
        log_success "Functionality baseline created"
        return 0
    fi
    
    log_info "Comparing functionality against baseline..."
    
    # Compare workflow success rates
    local workflows=$(jq -r '.workflows | keys[]' "$integration_current" 2>/dev/null || echo "")
    
    while IFS= read -r workflow; do
        [[ -z "$workflow" ]] && continue
        
        local current_success=$(jq -r ".workflows.\"$workflow\".success_rate // 0" "$integration_current")
        local baseline_success=$(jq -r ".workflows.\"$workflow\".success_rate // 0" "$integration_baseline")
        
        if [[ "$current_success" != "0" ]] && [[ "$baseline_success" != "0" ]]; then
            local degradation=$(echo "scale=1; ($baseline_success - $current_success)" | bc -l 2>/dev/null || echo "0")
            
            if (( $(echo "$degradation > $FUNCTIONALITY_THRESHOLD" | bc -l 2>/dev/null || echo "0") )); then
                functionality_regressions=$((functionality_regressions + 1))
                log_error "Functionality regression in $workflow: ${current_success}% vs ${baseline_success}% (-${degradation}%)"
                
                local regression_detail=$(cat << EOF
{
  "workflow": "$workflow",
  "current_success_rate": $current_success,
  "baseline_success_rate": $baseline_success,
  "degradation_percent": $degradation,
  "severity": "$(if (( $(echo "$degradation > 20" | bc -l 2>/dev/null || echo "0") )); then echo "critical"; elif (( $(echo "$degradation > 10" | bc -l 2>/dev/null || echo "0") )); then echo "high"; else echo "medium"; fi)"
}
EOF
                )
                
                jq --argjson detail "$regression_detail" \
                   ".functionality_analysis.regressions += [\$detail]" \
                   "$REGRESSION_LOG" > "${REGRESSION_LOG}.tmp" && mv "${REGRESSION_LOG}.tmp" "$REGRESSION_LOG"
            else
                log_info "✓ $workflow: ${current_success}% vs ${baseline_success}% (-${degradation}%)"
            fi
        fi
    done <<< "$workflows"
    
    # Update regression count
    jq --argjson count "$functionality_regressions" \
       '.regression_summary.functionality_regressions = $count' \
       "$REGRESSION_LOG" > "${REGRESSION_LOG}.tmp" && mv "${REGRESSION_LOG}.tmp" "$REGRESSION_LOG"
    
    if [[ $functionality_regressions -eq 0 ]]; then
        log_success "No functionality regressions detected"
    else
        log_warn "$functionality_regressions functionality regressions detected"
    fi
    
    return $functionality_regressions
}

# Extract integration test results from log
extract_integration_results() {
    local log_file="$1"
    local output_file="$2"
    
    cat > "$output_file" << 'EOF'
{
  "extracted_at": null,
  "workflows": {}
}
EOF
    
    jq --arg ts "$(date -Iseconds)" '.extracted_at = $ts' "$output_file" > "${output_file}.tmp" && mv "${output_file}.tmp" "$output_file"
    
    # Parse log for workflow results
    if [[ -f "$log_file" ]]; then
        # Extract workflow success information (this is a simplified parser)
        local workflows=("search" "graph" "nlp" "verification" "security")
        
        for workflow in "${workflows[@]}"; do
            local success_count=0
            local total_count=0
            
            # Count successes and total tests for this workflow
            while IFS= read -r line; do
                if echo "$line" | grep -qi "$workflow"; then
                    total_count=$((total_count + 1))
                    if echo "$line" | grep -q "PASS"; then
                        success_count=$((success_count + 1))
                    fi
                fi
            done < "$log_file"
            
            local success_rate=0
            if [[ $total_count -gt 0 ]]; then
                success_rate=$(echo "scale=1; $success_count * 100 / $total_count" | bc -l 2>/dev/null || echo "0")
            fi
            
            local workflow_info=$(cat << EOF
{
  "success_count": $success_count,
  "total_count": $total_count,
  "success_rate": $success_rate
}
EOF
            )
            
            jq --arg workflow "$workflow" --argjson info "$workflow_info" \
               '.workflows[$workflow] = $info' \
               "$output_file" > "${output_file}.tmp" && mv "${output_file}.tmp" "$output_file"
        done
    fi
}

# Generate recommendations
generate_recommendations() {
    log_header "Generating Recommendations"
    
    local recommendations=()
    
    # Performance recommendations
    local perf_regressions=$(jq '.regression_summary.performance_regressions' "$REGRESSION_LOG")
    if [[ $perf_regressions -gt 0 ]]; then
        recommendations+=("\"Review and optimize performance-critical code paths that show degradation > ${PERFORMANCE_THRESHOLD}%\"")
        recommendations+=("\"Profile application to identify bottlenecks in regressed workflows\"")
        recommendations+=("\"Consider caching strategies for frequently accessed data\"")
    fi
    
    # API recommendations
    local api_changes=$(jq '.regression_summary.api_breaking_changes' "$REGRESSION_LOG")
    if [[ $api_changes -gt 0 ]]; then
        recommendations+=("\"Implement API versioning to maintain backward compatibility\"")
        recommendations+=("\"Document all API changes in release notes\"")
        recommendations+=("\"Consider deprecation strategy instead of immediate removal\"")
    fi
    
    # Functionality recommendations
    local func_regressions=$(jq '.regression_summary.functionality_regressions' "$REGRESSION_LOG")
    if [[ $func_regressions -gt 0 ]]; then
        recommendations+=("\"Investigate and fix failing integration test workflows\"")
        recommendations+=("\"Enhance error handling and resilience in affected components\"")
        recommendations+=("\"Review recent code changes for unintended side effects\"")
    fi
    
    # General recommendations
    if [[ $perf_regressions -eq 0 ]] && [[ $api_changes -eq 0 ]] && [[ $func_regressions -eq 0 ]]; then
        recommendations+=("\"No regressions detected - system is stable for release\"")
        recommendations+=("\"Consider updating performance baselines with current results\"")
    else
        recommendations+=("\"Do not proceed with release until all regressions are resolved\"")
        recommendations+=("\"Run additional testing after fixes are implemented\"")
    fi
    
    # Update recommendations in results
    local recommendations_json="[$(IFS=','; echo "${recommendations[*]}")]"
    jq --argjson recs "$recommendations_json" '.recommendations = $recs' \
       "$REGRESSION_LOG" > "${REGRESSION_LOG}.tmp" && mv "${REGRESSION_LOG}.tmp" "$REGRESSION_LOG"
    
    log_info "Generated $(echo "$recommendations_json" | jq 'length') recommendations"
}

# Update baselines
update_baselines() {
    log_header "Updating Performance Baselines"
    
    local force_update="${1:-false}"
    local total_regressions=$(jq '.regression_summary | .performance_regressions + .api_breaking_changes + .functionality_regressions' "$REGRESSION_LOG")
    
    if [[ "$force_update" == "true" ]] || [[ $total_regressions -eq 0 ]]; then
        # Update performance baseline
        if [[ -f "${RESULTS_DIR}/current_performance.json" ]]; then
            cp "${RESULTS_DIR}/current_performance.json" "$BASELINES_DIR/performance_baseline.json"
            log_success "Performance baseline updated"
        fi
        
        # Update API baseline
        if [[ -f "${RESULTS_DIR}/api_current.json" ]]; then
            cp "${RESULTS_DIR}/api_current.json" "$BASELINES_DIR/api_baseline.json"
            log_success "API baseline updated"
        fi
        
        # Update integration baseline
        if [[ -f "${RESULTS_DIR}/integration_current.json" ]]; then
            cp "${RESULTS_DIR}/integration_current.json" "$BASELINES_DIR/integration_baseline.json"
            log_success "Integration baseline updated"
        fi
        
        # Store baseline metadata
        cat > "$BASELINES_DIR/baseline_metadata.json" << EOF
{
  "updated_at": "$(date -Iseconds)",
  "commit": "$CURRENT_COMMIT",
  "performance_threshold": $PERFORMANCE_THRESHOLD,
  "api_threshold": $API_BREAKING_THRESHOLD,
  "functionality_threshold": $FUNCTIONALITY_THRESHOLD
}
EOF
        
        log_success "Baselines updated successfully"
    else
        log_warn "Baselines not updated due to detected regressions"
    fi
}

# Generate final report
generate_regression_report() {
    log_header "Regression Test Report"
    
    local total_regressions=$(jq '.regression_summary | .performance_regressions + .api_breaking_changes + .functionality_regressions' "$REGRESSION_LOG")
    local perf_regressions=$(jq '.regression_summary.performance_regressions' "$REGRESSION_LOG")
    local api_changes=$(jq '.regression_summary.api_breaking_changes' "$REGRESSION_LOG")
    local func_regressions=$(jq '.regression_summary.functionality_regressions' "$REGRESSION_LOG")
    
    # Update total in JSON
    jq --argjson total "$total_regressions" '.regression_summary.total_regressions = $total' \
       "$REGRESSION_LOG" > "${REGRESSION_LOG}.tmp" && mv "${REGRESSION_LOG}.tmp" "$REGRESSION_LOG"
    
    # Console output
    log "📊 ${BLUE}Regression Analysis Results${NC}"
    log "   Baseline: $BASELINE_COMMIT"
    log "   Current:  $CURRENT_COMMIT"
    log "   Performance Regressions: ${RED}$perf_regressions${NC}"
    log "   API Breaking Changes: ${RED}$api_changes${NC}"
    log "   Functionality Regressions: ${RED}$func_regressions${NC}"
    log "   Total Regressions: ${RED}$total_regressions${NC}"
    log ""
    log "📄 Detailed report: $REGRESSION_LOG"
    
    # Generate markdown report
    local md_report="${RESULTS_DIR}/REGRESSION_REPORT_${TIMESTAMP}.md"
    cat > "$md_report" << EOF
# InfoTerminal Regression Test Report

**Date:** $(date)  
**Baseline:** $BASELINE_COMMIT  
**Current:** $CURRENT_COMMIT  

## Summary

| Category | Regressions | Status |
|----------|-------------|--------|
| Performance | $perf_regressions | $(if [[ $perf_regressions -eq 0 ]]; then echo "✅ PASS"; else echo "❌ FAIL"; fi) |
| API Breaking Changes | $api_changes | $(if [[ $api_changes -eq 0 ]]; then echo "✅ PASS"; else echo "❌ FAIL"; fi) |
| Functionality | $func_regressions | $(if [[ $func_regressions -eq 0 ]]; then echo "✅ PASS"; else echo "❌ FAIL"; fi) |
| **Total** | **$total_regressions** | $(if [[ $total_regressions -eq 0 ]]; then echo "✅ PASS"; else echo "❌ FAIL"; fi) |

EOF
    
    # Add recommendations
    echo "## Recommendations" >> "$md_report"
    echo "" >> "$md_report"
    jq -r '.recommendations[]' "$REGRESSION_LOG" | while read -r rec; do
        echo "- $rec" >> "$md_report"
    done
    
    # Deployment decision
    echo "" >> "$md_report"
    echo "## Deployment Decision" >> "$md_report"
    echo "" >> "$md_report"
    if [[ $total_regressions -eq 0 ]]; then
        echo "🎉 **APPROVED** - No regressions detected, safe to deploy" >> "$md_report"
    else
        echo "🛑 **BLOCKED** - Regressions detected, do not deploy until resolved" >> "$md_report"
    fi
    
    log_info "Markdown report: $md_report"
    
    # Final assessment
    if [[ $total_regressions -eq 0 ]]; then
        log_success "No regressions detected - deployment approved"
        return 0
    else
        log_error "$total_regressions regressions detected - deployment blocked"
        return 1
    fi
}

# Main execution
main() {
    local command="${1:-run}"
    
    case "$command" in
        "run")
            init_regression_testing
            analyze_performance_regressions || true
            analyze_api_breaking_changes || true
            analyze_functionality_regressions || true
            generate_recommendations
            generate_regression_report
            ;;
        "update-baselines")
            log_header "Forcing Baseline Update"
            update_baselines "true"
            ;;
        "report-only")
            log_header "Generating Report from Existing Data"
            generate_regression_report
            ;;
        *)
            echo "Usage: $0 [run|update-baselines|report-only]"
            exit 1
            ;;
    esac
}

# Check dependencies
if ! command -v jq >/dev/null; then
    log_error "jq is required but not installed"
    exit 1
fi

if ! command -v bc >/dev/null; then
    log_error "bc is required but not installed"
    exit 1
fi

# Execute main function
main "$@"
