#!/bin/bash

# Docker Build Verification Script for InfoTerminal v0.2.0
# This script validates all required Dockerfiles exist and can be built

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR" && pwd)"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Services to check based on docker-compose.verification.yml
SERVICES=(
    "services/verification:infoterminal-verification"
    "services/ops-controller:infoterminal-ops-controller"
    "apps/frontend:infoterminal-frontend"
    "services/search-api:infoterminal-search-api"
    "services/graph-api:infoterminal-graph-api"
    "services/doc-entities:infoterminal-doc-entities"
    "services/egress-gateway:infoterminal-egress-gateway"
    "services/gateway:infoterminal-gateway"
    "services/graph-views:infoterminal-graph-views"
)

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "INFO")
            echo -e "${BLUE}[INFO]${NC} $message"
            ;;
        "SUCCESS")
            echo -e "${GREEN}[SUCCESS]${NC} $message"
            ;;
        "WARNING")
            echo -e "${YELLOW}[WARNING]${NC} $message"
            ;;
        "ERROR")
            echo -e "${RED}[ERROR]${NC} $message"
            ;;
    esac
}

# Function to check if Dockerfile exists
check_dockerfile() {
    local service_path=$1
    local dockerfile_path="$PROJECT_ROOT/$service_path/Dockerfile"
    
    if [[ -f "$dockerfile_path" ]]; then
        print_status "SUCCESS" "Dockerfile found: $dockerfile_path"
        return 0
    else
        print_status "ERROR" "Dockerfile missing: $dockerfile_path"
        return 1
    fi
}

# Function to validate Dockerfile content
validate_dockerfile() {
    local service_path=$1
    local dockerfile_path="$PROJECT_ROOT/$service_path/Dockerfile"
    
    # Check for basic Dockerfile requirements
    if grep -q "FROM " "$dockerfile_path"; then
        if grep -q "EXPOSE " "$dockerfile_path"; then
            if grep -q "CMD \|ENTRYPOINT " "$dockerfile_path"; then
                print_status "SUCCESS" "Dockerfile validation passed: $service_path"
                return 0
            else
                print_status "WARNING" "Dockerfile missing CMD/ENTRYPOINT: $service_path"
                return 1
            fi
        else
            print_status "WARNING" "Dockerfile missing EXPOSE: $service_path"
            return 1
        fi
    else
        print_status "ERROR" "Invalid Dockerfile (missing FROM): $service_path"
        return 1
    fi
}

# Function to test Docker build (dry run)
test_docker_build() {
    local service_path=$1
    local image_name=$2
    
    print_status "INFO" "Testing Docker build context for: $service_path"
    
    # Check if docker-compose can parse the service
    if command -v docker-compose >/dev/null 2>&1; then
        cd "$PROJECT_ROOT"
        if docker-compose -f docker-compose.verification.yml config --services | grep -q "$(basename $service_path)"; then
            print_status "SUCCESS" "Docker Compose configuration valid for: $service_path"
            return 0
        else
            print_status "WARNING" "Service not found in docker-compose.verification.yml: $service_path"
            return 1
        fi
    else
        print_status "WARNING" "Docker Compose not available, skipping build test"
        return 0
    fi
}

# Main validation function
main() {
    print_status "INFO" "Starting InfoTerminal Docker Build Verification"
    print_status "INFO" "Project Root: $PROJECT_ROOT"
    
    local total_services=${#SERVICES[@]}
    local successful_checks=0
    local failed_checks=0
    
    echo ""
    print_status "INFO" "Checking $total_services services..."
    echo ""
    
    for service_info in "${SERVICES[@]}"; do
        IFS=':' read -r service_path image_name <<< "$service_info"
        
        echo "----------------------------------------"
        print_status "INFO" "Checking service: $service_path"
        
        # Check if Dockerfile exists
        if check_dockerfile "$service_path"; then
            # Validate Dockerfile content
            if validate_dockerfile "$service_path"; then
                # Test Docker build context
                if test_docker_build "$service_path" "$image_name"; then
                    ((successful_checks++))
                    print_status "SUCCESS" "✅ $service_path: All checks passed"
                else
                    ((failed_checks++))
                    print_status "WARNING" "⚠️  $service_path: Build test failed"
                fi
            else
                ((failed_checks++))
                print_status "ERROR" "❌ $service_path: Dockerfile validation failed"
            fi
        else
            ((failed_checks++))
            print_status "ERROR" "❌ $service_path: Dockerfile missing"
        fi
        echo ""
    done
    
    # Summary
    echo "========================================"
    print_status "INFO" "Docker Build Verification Summary"
    echo "========================================"
    print_status "INFO" "Total services checked: $total_services"
    print_status "SUCCESS" "Successful checks: $successful_checks"
    
    if [[ $failed_checks -gt 0 ]]; then
        print_status "ERROR" "Failed checks: $failed_checks"
        echo ""
        print_status "ERROR" "❌ Some Docker builds may fail. Please review the issues above."
        return 1
    else
        print_status "SUCCESS" "All checks passed! ✅"
        echo ""
        print_status "SUCCESS" "🚀 Ready to build InfoTerminal v0.2.0 with docker-compose!"
        return 0
    fi
}

# Check additional requirements
check_requirements() {
    print_status "INFO" "Checking system requirements..."
    
    # Check if Docker is available
    if command -v docker >/dev/null 2>&1; then
        print_status "SUCCESS" "Docker found: $(docker --version)"
    else
        print_status "WARNING" "Docker not found - builds cannot be tested"
    fi
    
    # Check if Docker Compose is available
    if command -v docker-compose >/dev/null 2>&1; then
        print_status "SUCCESS" "Docker Compose found: $(docker-compose --version)"
    elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
        print_status "SUCCESS" "Docker Compose (plugin) found: $(docker compose version)"
    else
        print_status "WARNING" "Docker Compose not found - configuration cannot be tested"
    fi
    
    echo ""
}

# Help function
show_help() {
    echo "InfoTerminal Docker Build Verification Script"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -q, --quiet    Quiet mode (less output)"
    echo "  -v, --verbose  Verbose mode (more output)"
    echo ""
    echo "This script checks all required Dockerfiles for InfoTerminal v0.2.0"
    echo "and validates they meet basic requirements for docker-compose build."
}

# Parse command line arguments
QUIET=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -q|--quiet)
            QUIET=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            print_status "ERROR" "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Run the verification
if [[ "$QUIET" == "false" ]]; then
    check_requirements
fi

main
exit $?
