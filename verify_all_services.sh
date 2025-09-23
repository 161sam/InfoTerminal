#!/bin/bash
# InfoTerminal Service Verification Script
# Überprüft alle 24 Services auf Implementierung und Verkabelung

set -e

echo "🔍 InfoTerminal Service Verification - $(date)"
echo "======================================="
echo ""

# Base directory
INFOTERMINAL_DIR="/home/saschi/InfoTerminal"
SERVICES_DIR="$INFOTERMINAL_DIR/services"

# Erwartete Services aus der Memory (24 total)
EXPECTED_SERVICES=(
    "_shared"
    "agent-connector"
    "archive" 
    "auth-service"
    "cache-manager"
    "collab-hub"
    "doc-entities"
    "egress-gateway"
    "feedback-aggregator"
    "flowise-connector"
    "forensics"
    "gateway"
    "graph-api"
    "graph-views"
    "media-forensics"
    "opa-audit-sink"
    "openbb-connector"
    "ops-controller"
    "performance-monitor"
    "plugin-runner"
    "policy"
    "rag-api"
    "search-api"
    "verification"
    "websocket-manager"
    "xai"
    "federation-proxy"
    "entity-resolution"
)

echo "1. 📁 Service Directory Check"
echo "==============================="
EXISTING_SERVICES=()
MISSING_SERVICES=()

for service in "${EXPECTED_SERVICES[@]}"; do
    if [ -d "$SERVICES_DIR/$service" ]; then
        EXISTING_SERVICES+=("$service")
        echo "✅ $service - Directory exists"
    else
        MISSING_SERVICES+=("$service")
        echo "❌ $service - Directory missing"
    fi
done

echo ""
echo "📊 Summary: ${#EXISTING_SERVICES[@]}/${#EXPECTED_SERVICES[@]} services have directories"
echo ""

echo "2. 🐳 Docker Compose Integration Check"
echo "======================================="

# Check main docker-compose.yml
echo "Checking main docker-compose.yml..."
MAIN_COMPOSE="$INFOTERMINAL_DIR/docker-compose.yml"
SERVICES_IN_MAIN_COMPOSE=()

if [ -f "$MAIN_COMPOSE" ]; then
    # Extract service names from docker-compose.yml
    while IFS= read -r line; do
        if [[ $line =~ ^[[:space:]]*([a-zA-Z0-9_-]+):[[:space:]]*$ ]]; then
            service_name="${BASH_REMATCH[1]}"
            # Skip non-service entries
            if [[ "$service_name" != "services" && "$service_name" != "volumes" && "$service_name" != "networks" ]]; then
                SERVICES_IN_MAIN_COMPOSE+=("$service_name")
            fi
        fi
    done < "$MAIN_COMPOSE"
    
    echo "Services in main compose: ${SERVICES_IN_MAIN_COMPOSE[*]}"
else
    echo "❌ Main docker-compose.yml not found"
fi

echo ""

# Check additional compose files
echo "Checking additional compose files..."
COMPOSE_FILES=(
    "docker-compose.agents.yml"
    "docker-compose.gateway.yml" 
    "docker-compose.observability.yml"
    "docker-compose.verification.yml"
    "docker-compose.nlp.yml"
)

ALL_COMPOSED_SERVICES=("${SERVICES_IN_MAIN_COMPOSE[@]}")

for compose_file in "${COMPOSE_FILES[@]}"; do
    compose_path="$INFOTERMINAL_DIR/$compose_file"
    if [ -f "$compose_path" ]; then
        echo "✅ $compose_file exists"
        # Extract services (simplified)
        services_in_file=$(grep -E "^[[:space:]]*[a-zA-Z0-9_-]+:" "$compose_path" | grep -v "services:" | grep -v "volumes:" | grep -v "networks:" | sed 's/[[:space:]]*\([^:]*\):.*/\1/' || true)
        if [ -n "$services_in_file" ]; then
            while IFS= read -r service; do
                ALL_COMPOSED_SERVICES+=("$service")
            done <<< "$services_in_file"
        fi
    else
        echo "⚠️  $compose_file not found"
    fi
done

echo ""
echo "📊 Total services across all compose files: ${#ALL_COMPOSED_SERVICES[@]}"
echo ""

echo "3. 🔗 Service Implementation Check"
echo "=================================="

IMPLEMENTED_SERVICES=()
UNIMPLEMENTED_SERVICES=()

for service in "${EXISTING_SERVICES[@]}"; do
    service_dir="$SERVICES_DIR/$service"
    
    # Check for key implementation files
    has_implementation=false
    
    # Check for Python implementation
    if [ -f "$service_dir/main.py" ] || [ -f "$service_dir/app.py" ] || [ -f "$service_dir/__init__.py" ]; then
        has_implementation=true
    fi
    
    # Check for FastAPI v1 implementation
    if [ -f "$service_dir/app_v1.py" ]; then
        has_implementation=true
    fi
    
    # Check for Dockerfile
    dockerfile_exists=false
    if [ -f "$service_dir/Dockerfile" ]; then
        dockerfile_exists=true
    fi
    
    # Check for requirements/dependencies
    deps_exist=false
    if [ -f "$service_dir/requirements.txt" ] || [ -f "$service_dir/pyproject.toml" ] || [ -f "$service_dir/package.json" ]; then
        deps_exist=true
    fi
    
    if [ "$has_implementation" = true ]; then
        IMPLEMENTED_SERVICES+=("$service")
        status="✅"
        if [ "$dockerfile_exists" = true ]; then
            status="$status 🐳"
        fi
        if [ "$deps_exist" = true ]; then
            status="$status 📦"
        fi
        echo "$status $service - Implemented"
    else
        UNIMPLEMENTED_SERVICES+=("$service")
        echo "❌ $service - No implementation found"
    fi
done

echo ""
echo "📊 Implementation Summary: ${#IMPLEMENTED_SERVICES[@]}/${#EXISTING_SERVICES[@]} services implemented"
echo ""

echo "4. 🚀 Migration Status Check (*_v1.py pattern)"
echo "==============================================="

V1_MIGRATED_SERVICES=()
LEGACY_SERVICES=()

for service in "${IMPLEMENTED_SERVICES[@]}"; do
    service_dir="$SERVICES_DIR/$service"
    
    if [ -f "$service_dir/app_v1.py" ]; then
        V1_MIGRATED_SERVICES+=("$service")
        echo "✅ $service - Migrated to v1 pattern"
    else
        LEGACY_SERVICES+=("$service") 
        echo "⚠️  $service - Legacy implementation"
    fi
done

echo ""
echo "📊 Migration Summary: ${#V1_MIGRATED_SERVICES[@]}/${#IMPLEMENTED_SERVICES[@]} services migrated to v1 pattern"
echo ""

echo "5. 📋 Final Summary Report"
echo "=========================="
echo ""
echo "🏗️  **Service Infrastructure Status:**"
echo "   Total Expected Services: ${#EXPECTED_SERVICES[@]}"
echo "   Services with Directories: ${#EXISTING_SERVICES[@]}"
echo "   Services Implemented: ${#IMPLEMENTED_SERVICES[@]}"
echo "   Services in Docker Compose: ${#ALL_COMPOSED_SERVICES[@]}"
echo "   Services with v1 Migration: ${#V1_MIGRATED_SERVICES[@]}"
echo ""

if [ ${#MISSING_SERVICES[@]} -gt 0 ]; then
    echo "❌ **Missing Service Directories:**"
    for service in "${MISSING_SERVICES[@]}"; do
        echo "   - $service"
    done
    echo ""
fi

if [ ${#UNIMPLEMENTED_SERVICES[@]} -gt 0 ]; then
    echo "⚠️  **Services Needing Implementation:**"
    for service in "${UNIMPLEMENTED_SERVICES[@]}"; do
        echo "   - $service"
    done
    echo ""
fi

if [ ${#LEGACY_SERVICES[@]} -gt 0 ]; then
    echo "🔄 **Services Needing v1 Migration:**"
    for service in "${LEGACY_SERVICES[@]}"; do
        echo "   - $service"
    done
    echo ""
fi

echo "✅ **Fully Ready Services (v1 migrated):**"
for service in "${V1_MIGRATED_SERVICES[@]}"; do
    echo "   - $service"
done
echo ""

# Calculate readiness percentage
total_expected=${#EXPECTED_SERVICES[@]}
total_implemented=${#IMPLEMENTED_SERVICES[@]}
total_v1_migrated=${#V1_MIGRATED_SERVICES[@]}

readiness_percentage=$((total_implemented * 100 / total_expected))
v1_percentage=$((total_v1_migrated * 100 / total_expected))

echo "📈 **Overall InfoTerminal Service Readiness:**"
echo "   Service Implementation: $readiness_percentage% ($total_implemented/$total_expected)"
echo "   v1 Migration Progress: $v1_percentage% ($total_v1_migrated/$total_expected)"
echo ""

if [ $readiness_percentage -ge 90 ] && [ $v1_percentage -ge 60 ]; then
    echo "🎉 **STATUS: PRODUCTION READY** - All critical services implemented and majority migrated"
elif [ $readiness_percentage -ge 75 ]; then
    echo "⚡ **STATUS: NEAR PRODUCTION READY** - Most services implemented, migration ongoing"
elif [ $readiness_percentage -ge 50 ]; then
    echo "🚧 **STATUS: DEVELOPMENT READY** - Core services available, significant work remaining"
else
    echo "🔨 **STATUS: EARLY DEVELOPMENT** - Major implementation work needed"
fi

echo ""
echo "Verification completed at $(date)"
echo "================================="
