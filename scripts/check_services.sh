#!/bin/bash

# InfoTerminal Service Status Quick Check
# Überprüft alle Services und gibt Handlungsempfehlungen

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🔍 InfoTerminal Service Status Check"
echo "===================================="
echo "Project: $PROJECT_ROOT"
echo "Timestamp: $(date)"
echo ""

# Service Port-Mapping (authoritative list)
declare -A SERVICES
SERVICES["search-api"]="8611"
SERVICES["graph-api"]="8612" 
SERVICES["doc-entities"]="8613"
SERVICES["ops-controller"]="8614"
SERVICES["egress-gateway"]="8615"
SERVICES["auth-service"]="8616"
SERVICES["verification"]="8617"
SERVICES["media-forensics"]="8618"
SERVICES["nifi"]="8619"
SERVICES["plugin-runner"]="8621"
SERVICES["rag-api"]="8622"
SERVICES["collab-hub"]="8625"
SERVICES["xai"]="8626"
SERVICES["forensics"]="8627"
SERVICES["federation-proxy"]="8628"
SERVICES["performance-monitor"]="8629"
SERVICES["cache-manager"]="8630"
SERVICES["websocket-manager"]="8631"
SERVICES["feedback-aggregator"]="8632"
SERVICES["agent-connector"]="8633"
SERVICES["graph-views"]="8634"
SERVICES["gateway"]="8635"
SERVICES["policy"]="8636"
SERVICES["openbb-connector"]="8637"
SERVICES["opa-audit-sink"]="8638"
SERVICES["archive"]="8639"
SERVICES["flowise-connector"]="3417"

# Counters
HEALTHY=0
UNHEALTHY=0
NOT_RUNNING=0
TOTAL=${#SERVICES[@]}

# Results arrays
declare -a HEALTHY_SERVICES
declare -a UNHEALTHY_SERVICES  
declare -a NOT_RUNNING_SERVICES
declare -a MISSING_V1_API

echo "📊 Service Health Check Results:"
echo ""

# Check each service
for service in "${!SERVICES[@]}"; do
    port=${SERVICES[$service]}
    
    # Check if Docker container is running
    if docker ps --filter "name=$service" --format "{{.Names}}" | grep -q "^$service$"; then
        DOCKER_STATUS="🐳"
    else
        DOCKER_STATUS="❌"
    fi
    
    # Check health endpoint
    if curl -sSf "http://localhost:$port/health" >/dev/null 2>&1; then
        HEALTH_STATUS="✅"
        HEALTHY_SERVICES+=("$service")
        ((HEALTHY++))
    elif curl -sSf "http://localhost:$port/healthz" >/dev/null 2>&1; then
        HEALTH_STATUS="✅"
        HEALTHY_SERVICES+=("$service")
        ((HEALTHY++))
    elif curl -sSf "http://localhost:$port/" >/dev/null 2>&1; then
        HEALTH_STATUS="⚠️"
        UNHEALTHY_SERVICES+=("$service")
        ((UNHEALTHY++))
    else
        HEALTH_STATUS="❌"
        NOT_RUNNING_SERVICES+=("$service")
        ((NOT_RUNNING++))
    fi
    
    # Check for v1 API
    if curl -sSf "http://localhost:$port/v1" >/dev/null 2>&1; then
        V1_STATUS="🔄"
    else
        V1_STATUS=""
        if [[ "$HEALTH_STATUS" == "✅" ]]; then
            MISSING_V1_API+=("$service")
        fi
    fi
    
    printf "%-25s %s %s %-4s %s\n" "$service" "$DOCKER_STATUS" "$HEALTH_STATUS" ":$port" "$V1_STATUS"
done

echo ""
echo "📈 Summary:"
echo "  ✅ Healthy:     $HEALTHY/$TOTAL ($(( HEALTHY * 100 / TOTAL ))%)"
echo "  ⚠️  Unhealthy:   $UNHEALTHY/$TOTAL"  
echo "  ❌ Not Running: $NOT_RUNNING/$TOTAL"
echo ""

# Detailed Results
if [[ ${#HEALTHY_SERVICES[@]} -gt 0 ]]; then
    echo "✅ Healthy Services (${#HEALTHY_SERVICES[@]}):"
    for service in "${HEALTHY_SERVICES[@]}"; do
        echo "   - $service (http://localhost:${SERVICES[$service]})"
    done
    echo ""
fi

if [[ ${#UNHEALTHY_SERVICES[@]} -gt 0 ]]; then
    echo "⚠️ Unhealthy Services (${#UNHEALTHY_SERVICES[@]}):"
    for service in "${UNHEALTHY_SERVICES[@]}"; do
        echo "   - $service (http://localhost:${SERVICES[$service]}) - responds but not healthy"
    done
    echo ""
fi

if [[ ${#NOT_RUNNING_SERVICES[@]} -gt 0 ]]; then
    echo "❌ Not Running Services (${#NOT_RUNNING_SERVICES[@]}):"
    for service in "${NOT_RUNNING_SERVICES[@]}"; do
        if docker ps --filter "name=$service" --format "{{.Names}}" | grep -q "^$service$"; then
            echo "   - $service (Docker running, but service not responding)"
        else
            echo "   - $service (Docker container not running)"
        fi
    done
    echo ""
fi

if [[ ${#MISSING_V1_API[@]} -gt 0 ]]; then
    echo "🔄 Services Missing v1 API (${#MISSING_V1_API[@]}):"
    for service in "${MISSING_V1_API[@]}"; do
        echo "   - $service (needs migration to app_v1.py pattern)"
    done
    echo ""
fi

echo "🔧 Actionable Recommendations:"
echo ""

if [[ $NOT_RUNNING -gt 0 ]]; then
    echo "1. Start missing services:"
    echo "   docker-compose up -d"
    echo ""
fi

if [[ ${#MISSING_V1_API[@]} -gt 0 ]]; then
    echo "2. Migrate services to v1 API pattern:"
    for service in "${MISSING_V1_API[@]}"; do
        echo "   - $service: Create app_v1.py and routers/core_v1.py"
    done
    echo ""
fi

if [[ $UNHEALTHY -gt 0 ]]; then
    echo "3. Fix unhealthy services:"
    echo "   docker-compose logs [service-name]"
    echo "   docker-compose restart [service-name]"
    echo ""
fi

echo "📁 Check service implementation:"
echo "   ls -la services/"
echo ""

echo "🐳 Docker container status:"
echo "   docker-compose ps"
echo ""

echo "📊 Service Health Score: $HEALTHY/$TOTAL ($(( HEALTHY * 100 / TOTAL ))%)"

# Exit with appropriate code
if [[ $HEALTHY -eq $TOTAL ]]; then
    echo "🎉 All services are healthy!"
    exit 0
elif [[ $HEALTHY -gt $(( TOTAL / 2 )) ]]; then
    echo "⚠️ Most services are healthy, but some need attention."
    exit 1
else
    echo "❌ Critical: Many services are not running."
    exit 2
fi
