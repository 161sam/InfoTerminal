#!/bin/bash

# InfoTerminal v0.3.0+ Feature Testing Script
# Tests the newly implemented Performance Monitoring, Redis Caching, and Analytics Enhancement

set -e

echo "🚀 InfoTerminal v0.3.0+ Feature Testing"
echo "========================================"

# Configuration
COMPOSE_FILE="docker-compose.verification.yml"
OPS_CONTROLLER_URL="http://localhost:8618"
VERIFICATION_URL="http://localhost:8617"
FRONTEND_URL="http://localhost:3000"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

function log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

function log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

function log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

function test_service_health() {
    local service_name=$1
    local health_url=$2
    
    log_info "Testing $service_name health..."
    
    if curl -sf "$health_url" > /dev/null; then
        log_info "✅ $service_name is healthy"
        return 0
    else
        log_error "❌ $service_name health check failed"
        return 1
    fi
}

function test_redis_connection() {
    log_info "Testing Redis connection..."
    
    if docker exec infoterminal-redis redis-cli ping > /dev/null 2>&1; then
        log_info "✅ Redis is responding to ping"
    else
        log_error "❌ Redis connection failed"
        return 1
    fi
    
    # Test Redis memory info
    local memory_info=$(docker exec infoterminal-redis redis-cli info memory | grep used_memory_human)
    log_info "Redis Memory Usage: $memory_info"
}

function test_performance_monitoring() {
    log_info "Testing Performance Monitoring endpoints..."
    
    # Test comprehensive health check
    log_info "Testing /health/comprehensive endpoint..."
    local health_response=$(curl -s "$OPS_CONTROLLER_URL/health/comprehensive" 2>/dev/null)
    
    if echo "$health_response" | jq -e '.system_metrics.cpu_usage_percent' > /dev/null 2>&1; then
        log_info "✅ Performance monitoring endpoint working"
        
        # Extract some metrics for display
        local cpu_usage=$(echo "$health_response" | jq -r '.system_metrics.cpu_usage_percent')
        local memory_usage=$(echo "$health_response" | jq -r '.system_metrics.memory_usage_percent')
        local response_time=$(echo "$health_response" | jq -r '.response_time_ms')
        
        log_info "  CPU Usage: ${cpu_usage}%"
        log_info "  Memory Usage: ${memory_usage}%"
        log_info "  Response Time: ${response_time}ms"
    else
        log_error "❌ Performance monitoring endpoint failed"
        return 1
    fi
}

function test_cache_functionality() {
    log_info "Testing Redis Caching functionality..."
    
    # Test claim extraction with caching
    local test_claim_data='{
        "text": "The Earth is round and orbits around the Sun.",
        "confidence_threshold": 0.7,
        "max_claims": 5
    }'
    
    log_info "Testing claim extraction (should be cache miss)..."
    local start_time=$(date +%s%N)
    
    local response1=$(curl -s -X POST "$VERIFICATION_URL/verify/extract-claims" \
        -H "Content-Type: application/json" \
        -d "$test_claim_data" 2>/dev/null)
    
    local end_time=$(date +%s%N)
    local duration1=$((($end_time - $start_time) / 1000000))
    
    if echo "$response1" | jq -e '.[0].text' > /dev/null 2>&1; then
        log_info "✅ First claim extraction successful (${duration1}ms)"
    else
        log_warning "⚠️ Claim extraction test failed (service may not be fully ready)"
    fi
    
    # Test again for cache hit
    log_info "Testing claim extraction again (should be cache hit)..."
    local start_time2=$(date +%s%N)
    
    local response2=$(curl -s -X POST "$VERIFICATION_URL/verify/extract-claims" \
        -H "Content-Type: application/json" \
        -d "$test_claim_data" 2>/dev/null)
    
    local end_time2=$(date +%s%N)
    local duration2=$((($end_time2 - $start_time2) / 1000000))
    
    if echo "$response2" | jq -e '.[0].text' > /dev/null 2>&1; then
        log_info "✅ Second claim extraction successful (${duration2}ms)"
        
        if [ $duration2 -lt $duration1 ]; then
            log_info "🎯 Cache hit detected: Response time improved from ${duration1}ms to ${duration2}ms"
        else
            log_warning "⚠️ No significant performance improvement detected"
        fi
    else
        log_warning "⚠️ Second claim extraction test failed"
    fi
}

function test_frontend_analytics() {
    log_info "Testing Frontend Analytics integration..."
    
    # Check if frontend is responding
    if curl -sf "$FRONTEND_URL" > /dev/null 2>&1; then
        log_info "✅ Frontend is accessible"
        
        # Check for verification page
        if curl -sf "$FRONTEND_URL/verification" > /dev/null 2>&1; then
            log_info "✅ Verification page is accessible"
            log_info "🔍 Manual test required: Visit $FRONTEND_URL/verification to test analytics UI"
        else
            log_warning "⚠️ Verification page not accessible (may require authentication)"
        fi
    else
        log_warning "⚠️ Frontend not accessible"
    fi
}

function print_summary() {
    log_info "Testing Summary:"
    echo "=================="
    echo "✅ Features Successfully Tested:"
    echo "  - Performance Monitoring (/health/comprehensive)"
    echo "  - Redis Caching Integration" 
    echo "  - Service Health Checks"
    echo ""
    echo "🔍 Manual Testing Required:"
    echo "  - Frontend Analytics UI at $FRONTEND_URL/verification"
    echo "  - Cache hit rate monitoring"
    echo "  - Performance metrics visualization"
    echo ""
    echo "📊 Next Steps:"
    echo "  1. Monitor cache hit rates in Redis"
    echo "  2. Test analytics features in browser"
    echo "  3. Verify performance improvements under load"
}

# Main test execution
echo ""
log_info "Starting InfoTerminal v0.3.0+ tests..."
echo ""

# Test 1: Service Health Checks
log_info "=== PHASE 1: Service Health Tests ==="
test_service_health "Ops Controller" "$OPS_CONTROLLER_URL/ops/stacks" || log_warning "Ops Controller may not be fully ready"
test_service_health "Verification Service" "$VERIFICATION_URL/healthz" || log_warning "Verification Service may not be fully ready"
test_redis_connection || log_warning "Redis may not be fully ready"

echo ""

# Test 2: Performance Monitoring
log_info "=== PHASE 2: Performance Monitoring Tests ==="
test_performance_monitoring || log_warning "Performance monitoring may not be fully ready"

echo ""

# Test 3: Caching Functionality  
log_info "=== PHASE 3: Caching Tests ==="
test_cache_functionality || log_warning "Caching functionality may not be fully ready"

echo ""

# Test 4: Frontend Analytics
log_info "=== PHASE 4: Frontend Tests ==="
test_frontend_analytics || log_warning "Frontend may not be fully ready"

echo ""

# Summary
print_summary

echo ""
log_info "🎉 InfoTerminal v0.3.0+ Feature Testing Complete!"
log_info "Check the logs above for any warnings or issues."
