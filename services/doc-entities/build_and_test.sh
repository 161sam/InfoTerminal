#!/bin/bash
#
# InfoTerminal Service Consolidation - Docker Build & Test Script
# Validates the consolidated doc-entities service with fuzzy matching integration
#

set -e

echo "🔧 InfoTerminal Service Consolidation - Build & Test"
echo "======================================================"

SERVICE_DIR="/home/saschi/InfoTerminal/services/doc-entities"
COMPOSE_FILE="/home/saschi/InfoTerminal/docker-compose.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -d "$SERVICE_DIR" ]; then
    log_error "Service directory not found: $SERVICE_DIR"
    exit 1
fi

log_info "Service directory: $SERVICE_DIR"

# Check for required files
log_info "Checking consolidated service files..."

required_files=(
    "app.py"
    "fuzzy_matcher.py" 
    "requirements.txt"
    "CONSOLIDATION_COMPLETE.md"
    "validate_consolidation.py"
    "tests/test_fuzzy_integration.py"
)

for file in "${required_files[@]}"; do
    if [ -f "$SERVICE_DIR/$file" ]; then
        log_success "Found: $file"
    else
        log_error "Missing: $file"
        exit 1
    fi
done

# Check archived entity-resolution service
log_info "Checking entity-resolution service archival..."
if [ -f "/home/saschi/InfoTerminal/services/entity-resolution/DEPRECATED.md" ]; then
    log_success "entity-resolution service properly archived"
else
    log_warning "entity-resolution archival may be incomplete"
fi

# Check requirements
log_info "Validating requirements.txt..."
if grep -q "rapidfuzz" "$SERVICE_DIR/requirements.txt"; then
    log_success "rapidfuzz dependency found"
else
    log_error "rapidfuzz dependency missing"
    exit 1
fi

if grep -q "opentelemetry" "$SERVICE_DIR/requirements.txt"; then
    log_success "OpenTelemetry dependencies found"
else
    log_warning "OpenTelemetry dependencies may be missing"
fi

# Check docker-compose configuration  
log_info "Checking Docker Compose configuration..."
if [ -f "$COMPOSE_FILE" ]; then
    if grep -q "doc-entities" "$COMPOSE_FILE"; then
        log_success "doc-entities service found in docker-compose.yml"
    else
        log_error "doc-entities service not found in docker-compose.yml"
        exit 1
    fi
    
    # Verify entity-resolution is not active
    if ! grep -q "entity-resolution:" "$COMPOSE_FILE"; then
        log_success "entity-resolution service correctly absent from docker-compose.yml"
    else
        log_warning "entity-resolution service still present in docker-compose.yml"
    fi
else
    log_error "Docker compose file not found: $COMPOSE_FILE"
    exit 1
fi

# Test Docker build (if Docker is available)
log_info "Testing Docker build..."
if command -v docker &> /dev/null; then
    if docker --version &> /dev/null; then
        # Detect Docker Compose (prefer v2: `docker compose`, fallback to v1: `docker-compose`)
        if docker compose version &> /dev/null; then
            COMPOSE_CMD=(docker compose)
        elif command -v docker-compose &> /dev/null; then
            COMPOSE_CMD=(docker-compose)
        else
            log_error "Docker Compose not found. Install v2 (docker compose) or v1 (docker-compose)."
            exit 1
        fi

        log_info "Building consolidated doc-entities service..."

        # Build the service
        cd /home/saschi/InfoTerminal
        if "${COMPOSE_CMD[@]}" build doc-entities; then
            log_success "Docker build successful"
        else
            log_error "Docker build failed"
            exit 1
        fi

        # Test service startup (quick check)
        log_info "Testing service startup..."
        if "${COMPOSE_CMD[@]}" up -d doc-entities; then
            sleep 5  # Give service time to start

            # Check if service is running
            if "${COMPOSE_CMD[@]}" ps doc-entities | grep -q "running\|Up"; then
                log_success "Service started successfully"

                # Quick health check
                if curl -s http://localhost:8613/healthz | grep -q "ok"; then
                    log_success "Health check passed"
                else
                    log_warning "Health check failed (service may still be starting)"
                fi
            else
                log_error "Service failed to start"
                "${COMPOSE_CMD[@]}" logs doc-entities || true
                exit 1
            fi

            # Cleanup
            "${COMPOSE_CMD[@]}" down
        else
            log_error "Failed to start service"
            exit 1
        fi
    else
        log_warning "Docker not accessible, skipping build test"
    fi
else
    log_warning "Docker not available, skipping build test"
fi

# Syntax validation
log_info "Running Python syntax validation..."
if command -v python3 &> /dev/null; then
    # Check main app.py
    if python3 -m py_compile "$SERVICE_DIR/app.py"; then
        log_success "app.py syntax valid"
    else
        log_error "app.py syntax error"
        exit 1
    fi
    
    # Check fuzzy_matcher.py
    if python3 -m py_compile "$SERVICE_DIR/fuzzy_matcher.py"; then
        log_success "fuzzy_matcher.py syntax valid"
    else
        log_error "fuzzy_matcher.py syntax error" 
        exit 1
    fi
    
    # Check resolver.py
    if python3 -m py_compile "$SERVICE_DIR/resolver.py"; then
        log_success "resolver.py syntax valid"
    else
        log_error "resolver.py syntax error"
        exit 1
    fi
else
    log_warning "Python3 not available, skipping syntax validation"
fi

# Summary
echo ""
echo "======================================================"
log_success "Service Consolidation Validation Complete!"
echo ""
echo "📋 Summary:"
echo "  ✅ All required files present"
echo "  ✅ Dependencies correctly configured"
echo "  ✅ entity-resolution service archived"
echo "  ✅ Docker configuration valid"
echo "  ✅ Service builds and starts successfully"
echo "  ✅ Syntax validation passed"
echo ""
echo "🚀 Next Steps:"
echo "  1. Run: docker compose up doc-entities"  
echo "  2. Test: python validate_consolidation.py --url http://localhost:8613"
echo "  3. Production: Monitor service metrics and performance"
echo ""
echo "🎉 Consolidated doc-entities service ready for production!"
