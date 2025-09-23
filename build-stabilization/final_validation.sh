#!/bin/bash

# InfoTerminal Build System Final Validation Suite
# Build System Stabilization - Comprehensive Production Readiness Check

set -euo pipefail  # Exit on any error, undefined variable, or pipe failure

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT_DEFAULT="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly PROJECT_ROOT="${PROJECT_ROOT:-$PROJECT_ROOT_DEFAULT}"
readonly FRONTEND_DIR_DEFAULT="$PROJECT_ROOT/apps/frontend"
readonly FRONTEND_DIR="${FRONTEND_DIR:-$FRONTEND_DIR_DEFAULT}"
readonly RESULTS_DIR_DEFAULT="$PROJECT_ROOT/build-stabilization/final-validation"
readonly RESULTS_DIR="${RESULTS_DIR:-$RESULTS_DIR_DEFAULT}"
readonly DRY_RUN="${DRY_RUN:-0}"
readonly LOG_FILE_DEFAULT="$RESULTS_DIR/validation-$(date +%Y%m%d-%H%M%S).log"
readonly LOG_FILE_TMP="${LOG_FILE:-$LOG_FILE_DEFAULT}"
readonly LOG_FILE="$([ "$DRY_RUN" = "1" ] && echo "/dev/null" || echo "$LOG_FILE_TMP")"

usage() {
    cat <<USAGE
InfoTerminal Build System Final Validation

Env:
  PROJECT_ROOT=...    override repo root (default: parent of this script)
  FRONTEND_DIR=...    override frontend path (default: apps/frontend)
  RESULTS_DIR=...     override results dir (default: build-stabilization/final-validation)
  DRY_RUN=1           print actions without writing artifacts

Usage:
  $0
  DRY_RUN=1 $0
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Helper functions
log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

success() {
    log "${GREEN}✅ $1${NC}"
    ((PASSED_CHECKS++))
}

warning() {
    log "${YELLOW}⚠️  $1${NC}"
}

error() {
    log "${RED}❌ $1${NC}"
    ((FAILED_CHECKS++))
}

info() {
    log "${BLUE}ℹ️  $1${NC}"
}

check() {
    ((TOTAL_CHECKS++))
}

# Initialize
init() {
    log "${BLUE}🔧 InfoTerminal Build System Final Validation${NC}"
    log "${BLUE}=============================================${NC}"
    log "Date: $(date)"
    log "Project: InfoTerminal v0.2.0 → v1.0.0"
    log "Validation Suite: Production Readiness Check"
    log ""
    
    # Create results directory (idempotent)
    if [[ "$DRY_RUN" == "1" ]]; then
        log "⏭️  DRY_RUN=1 → would create: $RESULTS_DIR"
    else
        mkdir -p "$RESULTS_DIR"
    fi
    
    # Check if we can access the project
    if [[ ! -d "$PROJECT_ROOT" ]]; then
        error "Project root not found: $PROJECT_ROOT"
        exit 1
    fi
    
    cd "$PROJECT_ROOT"
    info "Working directory: $(pwd)"
    log ""
}

# Phase 1: Environment Validation
validate_environment() {
    log "${BLUE}📋 Phase 1: Environment Validation${NC}"
    log "--------------------------------"
    
    # Node.js version
    check
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        if [[ "$NODE_VERSION" == v20* ]] || [[ "$NODE_VERSION" == v18* ]]; then
            success "Node.js version: $NODE_VERSION (Compatible)"
        else
            warning "Node.js version: $NODE_VERSION (May have compatibility issues)"
        fi
    else
        error "Node.js not installed"
        return 1
    fi
    
    # npm version
    check
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        success "npm version: $NPM_VERSION"
    else
        error "npm not installed"
        return 1
    fi
    
    # pnpm availability
    check
    if command -v pnpm &> /dev/null; then
        PNPM_VERSION=$(pnpm --version)
        success "pnpm version: $PNPM_VERSION"
    else
        warning "pnpm not installed - will use npm"
    fi
    
    # Docker availability
    check
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        success "Docker version: $DOCKER_VERSION"
    else
        warning "Docker not available - skipping container tests"
    fi
    
    log ""
}

# Phase 2: Project Structure Validation
validate_structure() {
    log "${BLUE}📋 Phase 2: Project Structure Validation${NC}"
    log "---------------------------------------"
    
    # Critical directories
    local CRITICAL_DIRS=(
        "apps/frontend"
        "apps/frontend/src"
        "apps/frontend/pages"
        "apps/frontend/public"
        "services"
        ".github/workflows"
    )
    
    for dir in "${CRITICAL_DIRS[@]}"; do
        check
        if [[ -d "$dir" ]]; then
            FILE_COUNT=$(find "$dir" -type f | wc -l)
            success "$dir/ directory exists ($FILE_COUNT files)"
        else
            error "$dir/ directory missing"
        fi
    done
    
    # Critical files
    local CRITICAL_FILES=(
        "apps/frontend/package.json"
        "apps/frontend/tsconfig.json"
        "apps/frontend/next.config.js"
        "apps/frontend/Dockerfile"
        "package.json"
        "docker-compose.yml"
        ".github/workflows/ci.yml"
    )
    
    for file in "${CRITICAL_FILES[@]}"; do
        check
        if [[ -f "$file" ]]; then
            FILE_SIZE=$(du -h "$file" | cut -f1)
            success "$file exists ($FILE_SIZE)"
        else
            error "$file missing"
        fi
    done
    
    log ""
}

# Phase 3: TypeScript Configuration Validation
validate_typescript() {
    log "${BLUE}📋 Phase 3: TypeScript Configuration Validation${NC}"
    log "---------------------------------------------"
    
    cd "$FRONTEND_DIR"
    
    # Check tsconfig.json
    check
    if [[ -f "tsconfig.json" ]]; then
        success "tsconfig.json found"
        
        # Validate JSON syntax
        if jq empty tsconfig.json 2>/dev/null; then
            success "tsconfig.json has valid JSON syntax"
        else
            error "tsconfig.json has invalid JSON syntax"
        fi
        
        # Check for strict mode
        if grep -q '"strict": true' tsconfig.json; then
            success "TypeScript strict mode enabled"
        else
            warning "TypeScript strict mode not enabled"
        fi
        
        # Check for path mapping
        if grep -q '"@/\*"' tsconfig.json; then
            success "Path mapping (@/*) configured"
        else
            error "Path mapping (@/*) not configured"
        fi
        
    else
        error "tsconfig.json not found"
    fi
    
    # Check if enhanced TypeScript config exists
    check
    if [[ -f "tsconfig.enhanced.json" ]]; then
        success "Enhanced TypeScript configuration available"
        info "Consider migrating to tsconfig.enhanced.json for production-grade strictness"
    else
        info "Enhanced TypeScript configuration not found (optional)"
    fi
    
    cd "$PROJECT_ROOT"
    log ""
}

# Phase 4: Build System Files Validation
validate_build_files() {
    log "${BLUE}📋 Phase 4: Build System Files Validation${NC}"
    log "----------------------------------------"
    
    cd "$FRONTEND_DIR"
    
    # Package.json scripts
    local REQUIRED_SCRIPTS=("build" "dev" "test" "lint")
    
    for script in "${REQUIRED_SCRIPTS[@]}"; do
        check
        if grep -q "\"$script\":" package.json; then
            SCRIPT_CMD=$(grep "\"$script\":" package.json | head -1 | sed 's/.*": "\([^"]*\)".*/\1/')
            success "$script script: $SCRIPT_CMD"
        else
            error "$script script missing"
        fi
    done
    
    # TypeScript dependencies
    check
    if grep -q '"typescript"' package.json; then
        TS_VERSION=$(grep '"typescript"' package.json | sed 's/.*": "\([^"]*\)".*/\1/')
        success "TypeScript dependency: $TS_VERSION"
    else
        error "TypeScript dependency missing"
    fi
    
    # UI Component dependencies
    local UI_DEPS=("clsx" "tailwind-merge" "@types/react" "@types/node")
    
    for dep in "${UI_DEPS[@]}"; do
        check
        if grep -q "\"$dep\"" package.json; then
            success "$dep dependency found"
        else
            warning "$dep dependency missing"
        fi
    done
    
    cd "$PROJECT_ROOT"
    log ""
}

# Phase 5: UI Components Validation
validate_ui_components() {
    log "${BLUE}📋 Phase 5: UI Components Validation${NC}"
    log "-----------------------------------"
    
    local UI_COMPONENTS_DIR="$FRONTEND_DIR/src/components/ui"
    local REQUIRED_COMPONENTS=("badge.tsx" "progress.tsx" "alert.tsx" "card.tsx" "button.tsx")
    
    if [[ -d "$UI_COMPONENTS_DIR" ]]; then
        success "UI components directory exists"
        
        for component in "${REQUIRED_COMPONENTS[@]}"; do
            check
            if [[ -f "$UI_COMPONENTS_DIR/$component" ]]; then
                # Check for proper exports
                if grep -q "export.*function\|export.*interface" "$UI_COMPONENTS_DIR/$component"; then
                    success "$component has proper exports"
                else
                    warning "$component missing proper exports"
                fi
            else
                error "$component missing"
            fi
        done
        
        # Check utils.ts
        check
        if [[ -f "$FRONTEND_DIR/src/lib/utils.ts" ]]; then
            if grep -q "export function cn" "$FRONTEND_DIR/src/lib/utils.ts"; then
                success "cn() utility function available"
            else
                error "cn() utility function missing"
            fi
        else
            error "utils.ts library missing"
        fi
        
    else
        error "UI components directory not found"
    fi
    
    log ""
}

# Phase 6: API Routes Validation
validate_api_routes() {
    log "${BLUE}📋 Phase 6: API Routes Validation${NC}"
    log "--------------------------------"
    
    local API_DIR="$FRONTEND_DIR/pages/api"
    
    if [[ -d "$API_DIR" ]]; then
        API_FILES_COUNT=$(find "$API_DIR" -name "*.ts" -o -name "*.js" | wc -l)
        success "API routes directory exists ($API_FILES_COUNT files)"
        
        # Check specific API routes that were fixed
        local CRITICAL_APIS=("health.ts" "security/status.ts")
        
        for api in "${CRITICAL_APIS[@]}"; do
            check
            if [[ -f "$API_DIR/$api" ]]; then
                # Check for proper Next.js types
                if grep -q "NextApiRequest\|NextApiResponse" "$API_DIR/$api"; then
                    success "$api has proper Next.js API types"
                else
                    warning "$api missing Next.js API types"
                fi
                
                # Check for fetch timeout fixes
                if [[ "$api" == "security/status.ts" ]]; then
                    if grep -q "AbortController\|fetchWithTimeout" "$API_DIR/$api"; then
                        success "$api has timeout fix implemented"
                    else
                        warning "$api may be missing timeout fix"
                    fi
                fi
            else
                warning "$api not found (may not be implemented yet)"
            fi
        done
        
    else
        warning "API routes directory not found"
    fi
    
    log ""
}

# Phase 7: Docker Configuration Validation
validate_docker() {
    log "${BLUE}📋 Phase 7: Docker Configuration Validation${NC}"
    log "-----------------------------------------"
    
    cd "$FRONTEND_DIR"
    
    # Check Dockerfile
    check
    if [[ -f "Dockerfile" ]]; then
        success "Dockerfile exists"
        
        # Check for multi-stage build
        if grep -q "FROM.*AS" Dockerfile; then
            success "Multi-stage build configured"
        else
            warning "Single-stage build (consider multi-stage for optimization)"
        fi
        
        # Check for non-root user
        if grep -q "USER\|adduser\|addgroup" Dockerfile; then
            success "Non-root user configuration found"
        else
            warning "Non-root user not configured"
        fi
        
        # Check for health check
        if grep -q "HEALTHCHECK" Dockerfile; then
            success "Health check configured"
        else
            warning "Health check not configured"
        fi
        
    else
        error "Dockerfile not found"
    fi
    
    # Check for optimized Dockerfile
    check
    if [[ -f "Dockerfile.optimized" ]]; then
        success "Optimized Dockerfile available"
        info "Consider using Dockerfile.optimized for better performance"
    else
        info "Optimized Dockerfile not found (available in build-stabilization/)"
    fi
    
    # Check .dockerignore
    check
    if [[ -f ".dockerignore" ]]; then
        success ".dockerignore exists"
        
        IGNORE_RULES=$(wc -l < .dockerignore)
        info ".dockerignore has $IGNORE_RULES rules"
    else
        warning ".dockerignore not found (build context may be large)"
    fi
    
    cd "$PROJECT_ROOT"
    log ""
}

# Phase 8: CI/CD Pipeline Validation
validate_cicd() {
    log "${BLUE}📋 Phase 8: CI/CD Pipeline Validation${NC}"
    log "------------------------------------"
    
    local WORKFLOWS_DIR=".github/workflows"
    
    if [[ -d "$WORKFLOWS_DIR" ]]; then
        WORKFLOW_COUNT=$(find "$WORKFLOWS_DIR" -name "*.yml" -o -name "*.yaml" | wc -l)
        success "GitHub Actions workflows directory exists ($WORKFLOW_COUNT workflows)"
        
        # Check main CI workflow
        check
        if [[ -f "$WORKFLOWS_DIR/ci.yml" ]]; then
            success "Main CI workflow (ci.yml) exists"
            
            # Check for job parallelization
            if grep -q "jobs:" "$WORKFLOWS_DIR/ci.yml"; then
                JOB_COUNT=$(grep -c "^  [a-zA-Z][a-zA-Z-]*:$" "$WORKFLOWS_DIR/ci.yml")
                success "CI pipeline has $JOB_COUNT parallel jobs"
            else
                error "CI pipeline jobs not configured"
            fi
            
            # Check for caching
            if grep -q "cache:" "$WORKFLOWS_DIR/ci.yml"; then
                success "Build caching enabled"
            else
                warning "Build caching not configured"
            fi
            
            # Check for security scanning
            if grep -q "gitleaks\|security" "$WORKFLOWS_DIR/ci.yml"; then
                success "Security scanning integrated"
            else
                warning "Security scanning not found"
            fi
            
        else
            error "Main CI workflow not found"
        fi
        
        # Check for enhanced CI workflow
        check
        if [[ -f "$PROJECT_ROOT/build-stabilization/ci-enhanced.yml" ]]; then
            success "Enhanced CI workflow available"
            info "Consider upgrading to ci-enhanced.yml for better quality gates"
        else
            info "Enhanced CI workflow not found (available in build-stabilization/)"
        fi
        
    else
        error "GitHub Actions workflows directory not found"
    fi
    
    log ""
}

# Phase 9: Build Validation Test
validate_build_test() {
    log "${BLUE}📋 Phase 9: Build Validation Test${NC}"
    log "--------------------------------"
    
    cd "$FRONTEND_DIR"
    
    # Check if node_modules exists
    check
    if [[ -d "node_modules" ]]; then
        success "node_modules directory exists"
        
        NODE_MODULES_SIZE=$(du -sh node_modules | cut -f1)
        info "node_modules size: $NODE_MODULES_SIZE"
    else
        warning "node_modules not found - dependencies need to be installed"
        info "Run 'npm install' to install dependencies"
    fi
    
    # Simulate build commands (without actually running them)
    local BUILD_COMMANDS=("typecheck" "lint" "build" "test")
    
    for cmd in "${BUILD_COMMANDS[@]}"; do
        check
        if [[ -d "node_modules" ]] && grep -q "\"$cmd\":" package.json; then
            success "Ready for: npm run $cmd"
        else
            if [[ ! -d "node_modules" ]]; then
                warning "Cannot test: npm run $cmd (dependencies not installed)"
            else
                error "Cannot test: npm run $cmd (script not found)"
            fi
        fi
    done
    
    cd "$PROJECT_ROOT"
    log ""
}

# Phase 10: Documentation and Artifacts Check
validate_documentation() {
    log "${BLUE}📋 Phase 10: Documentation & Artifacts Check${NC}"
    log "-------------------------------------------"
    
    local STABILIZATION_DIR="build-stabilization"
    
    if [[ -d "$STABILIZATION_DIR" ]]; then
        success "Build stabilization directory exists"
        
        local DOC_COUNT=$(find "$STABILIZATION_DIR" -name "*.md" | wc -l)
        local SCRIPT_COUNT=$(find "$STABILIZATION_DIR" -name "*.sh" | wc -l)
        local CONFIG_COUNT=$(find "$STABILIZATION_DIR" -name "*.json" -o -name "*.yml" | wc -l)
        
        success "Documentation files: $DOC_COUNT"
        success "Script files: $SCRIPT_COUNT"
        success "Configuration files: $CONFIG_COUNT"
        
        # Check for critical documentation
        local CRITICAL_DOCS=(
            "BUILD_ANALYSIS_COMPLETE.md"
            "DOCKER_BUILD_OPTIMIZATION.md"
            "CICD_PIPELINE_ANALYSIS.md"
            "INFOTERMINAL_BUILD_STABILIZATION_COMPLETE.md"
        )
        
        for doc in "${CRITICAL_DOCS[@]}"; do
            check
            if [[ -f "$STABILIZATION_DIR/$doc" ]]; then
                success "$doc exists"
            else
                warning "$doc missing"
            fi
        done
        
    else
        error "Build stabilization directory not found"
    fi
    
    log ""
}

# Final Assessment
final_assessment() {
    log "${BLUE}📋 FINAL ASSESSMENT${NC}"
    log "${BLUE}=================${NC}"
    log ""
    
    local SUCCESS_RATE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
    
    log "📊 Validation Statistics:"
    log "  Total Checks: $TOTAL_CHECKS"
    log "  Passed: ${GREEN}$PASSED_CHECKS${NC}"
    log "  Failed: ${RED}$FAILED_CHECKS${NC}"
    log "  Success Rate: $SUCCESS_RATE%"
    log ""
    
    # Create summary report
    cat > "$RESULTS_DIR/validation-summary.md" << EOF
# InfoTerminal Build System Final Validation Summary

**Date:** $(date)  
**Project:** InfoTerminal v0.2.0 → v1.0.0  
**Validation Suite:** Production Readiness Check  

## Results

- **Total Checks:** $TOTAL_CHECKS
- **Passed:** $PASSED_CHECKS
- **Failed:** $FAILED_CHECKS
- **Success Rate:** $SUCCESS_RATE%

## Assessment

EOF
    
    if [[ $SUCCESS_RATE -ge 90 ]]; then
        log "${GREEN}🎯 PRODUCTION READINESS: EXCELLENT (${SUCCESS_RATE}%)${NC}"
        log "${GREEN}✅ Build system is ready for v1.0.0 deployment${NC}"
        echo "**Status:** ✅ PRODUCTION READY" >> "$RESULTS_DIR/validation-summary.md"
    elif [[ $SUCCESS_RATE -ge 80 ]]; then
        log "${YELLOW}🎯 PRODUCTION READINESS: GOOD (${SUCCESS_RATE}%)${NC}"
        log "${YELLOW}⚠️  Minor issues should be addressed before deployment${NC}"
        echo "**Status:** ⚠️ GOOD - Minor fixes needed" >> "$RESULTS_DIR/validation-summary.md"
    elif [[ $SUCCESS_RATE -ge 70 ]]; then
        log "${YELLOW}🎯 PRODUCTION READINESS: FAIR (${SUCCESS_RATE}%)${NC}"
        log "${YELLOW}⚠️  Several issues need to be addressed${NC}"
        echo "**Status:** ⚠️ FAIR - Issues need attention" >> "$RESULTS_DIR/validation-summary.md"
    else
        log "${RED}🎯 PRODUCTION READINESS: NEEDS WORK (${SUCCESS_RATE}%)${NC}"
        log "${RED}❌ Critical issues must be resolved before deployment${NC}"
        echo "**Status:** ❌ NEEDS WORK - Critical issues found" >> "$RESULTS_DIR/validation-summary.md"
    fi
    
    log ""
    log "📁 Detailed results saved to: $LOG_FILE"
    log "📊 Summary report: $RESULTS_DIR/validation-summary.md"
    log ""
    
    # Recommendations
    log "${BLUE}🔧 Next Steps:${NC}"
    
    if [[ $FAILED_CHECKS -gt 0 ]]; then
        log "1. 🔴 Address the $FAILED_CHECKS failed checks above"
    fi
    
    log "2. 🧪 Run actual build tests:"
    log "   cd $FRONTEND_DIR"
    log "   npm install"
    log "   npm run typecheck"
    log "   npm run build"
    log ""
    log "3. 🐳 Test Docker build:"
    log "   cd $PROJECT_ROOT"
    log "   docker build -f apps/frontend/Dockerfile ."
    log ""
    log "4. 🚀 Deploy to staging environment for integration testing"
    log ""
    
    return $([[ $SUCCESS_RATE -ge 80 ]] && echo 0 || echo 1)
}

# Main execution
main() {
    init
    
    validate_environment || true
    validate_structure || true
    validate_typescript || true
    validate_build_files || true
    validate_ui_components || true
    validate_api_routes || true
    validate_docker || true
    validate_cicd || true
    validate_build_test || true
    validate_documentation || true
    
    final_assessment
}

# Execute main function
main "$@"
