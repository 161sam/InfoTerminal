#!/bin/bash

# typescript_audit.sh
# Comprehensive TypeScript Build Analysis for InfoTerminal v0.2.0

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FRONTEND_DIR="${FRONTEND_DIR:-$PROJECT_ROOT/apps/frontend}"
AUDIT_DIR="$PROJECT_ROOT/build-stabilization/audit-results"
DRY_RUN="${DRY_RUN:-0}"

usage() {
  cat <<USAGE
InfoTerminal TypeScript Build Audit

Usage:
  DRY_RUN=1 $0      # Print actions without modifying files
  FRONTEND_DIR=... $0  # Analyze a custom frontend path

Outputs:
  - $AUDIT_DIR (created if missing)
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

echo "🔍 InfoTerminal TypeScript Build Audit"
echo "======================================"
echo ""

if [[ ! -d "$FRONTEND_DIR" ]]; then
  echo "❌ Frontend directory not found: $FRONTEND_DIR" >&2
  exit 1
fi

echo "📂 Working Directory: $FRONTEND_DIR"
echo "📅 Audit Date: $(date)"
echo ""

# Create audit output directory (idempotent)
if [[ "$DRY_RUN" == "1" ]]; then
  echo "⏭️  DRY_RUN=1 → would create: $AUDIT_DIR"
else
  mkdir -p "$AUDIT_DIR"
fi

echo "📋 1. TypeScript Configuration Analysis"
echo "--------------------------------------"

if [ -f "tsconfig.json" ]; then
    echo "✅ tsconfig.json found"
    echo "📊 TypeScript Config:"
    grep -E "(target|module|strict|baseUrl)" tsconfig.json || true
else
    echo "❌ tsconfig.json NOT FOUND - Critical Issue!"
fi

echo ""
echo "📋 2. Package.json Dependencies Check"
echo "------------------------------------"

if [ -f "package.json" ]; then
    echo "✅ package.json found"
    
    # Check TypeScript version
    TS_VERSION=$(grep '"typescript"' package.json | head -1) || true
    echo "🔧 TypeScript Version: $TS_VERSION"
    
    # Check React version
    REACT_VERSION=$(grep '"react"' package.json | head -1) || true
    echo "⚛️ React Version: $REACT_VERSION"
    
    # Check Next.js version
    NEXT_VERSION=$(grep '"next"' package.json | head -1) || true
    echo "🚀 Next.js Version: $NEXT_VERSION"
    
    # Check for missing type packages
    echo ""
    echo "🔍 Checking for Missing @types Packages:"
    
    # Extract dependencies that might need @types
    PACKAGES=($(grep -E '"(@[^/]+/[^"]+|[^@][^"]+)"' package.json | sed 's/.*"\([^"]*\)".*/\1/' | grep -v "@types" | head -10))
    
    for package in "${PACKAGES[@]}"; do
        TYPE_PACKAGE="@types/$(echo $package | sed 's/@[^/]*\///' | sed 's/\//-/g')"
        if grep -q "\"$TYPE_PACKAGE\"" package.json; then
            echo "  ✅ $TYPE_PACKAGE - Found"
        else
            echo "  ⚠️  $TYPE_PACKAGE - Missing (may be needed)"
        fi
    done
    
else
    echo "❌ package.json NOT FOUND - Critical Issue!"
fi

echo ""
echo "📋 3. TypeScript Files Analysis"
echo "------------------------------"

# Count TypeScript files
TS_FILES=$(find . -name "*.ts" -o -name "*.tsx" | wc -l)
echo "📁 Total TypeScript Files: $TS_FILES"

# List file types
echo "📊 File Type Distribution:"
echo "  .ts files: $(find . -name "*.ts" | wc -l)"
echo "  .tsx files: $(find . -name "*.tsx" | wc -l)"
echo "  .js files: $(find . -name "*.js" | wc -l)"
echo "  .jsx files: $(find . -name "*.jsx" | wc -l)"

echo ""
echo "📋 4. Import Path Analysis"
echo "-------------------------"

echo "🔍 Checking @/* import paths:"
IMPORT_ISSUES=$(grep -r "from ['\"]@/" src/ pages/ 2>/dev/null | wc -l) || true
echo "📊 @/* imports found: $IMPORT_ISSUES"

echo ""
echo "🔍 Checking relative import issues:"
RELATIVE_IMPORTS=$(grep -r "from ['\"]\.\./" src/ pages/ 2>/dev/null | wc -l) || true
echo "📊 ../ relative imports: $RELATIVE_IMPORTS"

echo ""
echo "📋 5. API Routes Analysis"
echo "------------------------"

if [ -d "pages/api" ]; then
    API_FILES=$(find pages/api -name "*.ts" -o -name "*.js" | wc -l)
    echo "📁 API Route Files: $API_FILES"
    
    echo "🔍 API Files:"
    find pages/api -name "*.ts" -o -name "*.js" | head -10 | while read file; do
        echo "  📄 $file"
        # Check for proper types
        if grep -q "NextApiRequest\|NextApiResponse" "$file"; then
            echo "    ✅ Proper Next.js API types"
        else
            echo "    ⚠️  Missing Next.js API types"
        fi
    done
else
    echo "📁 No API routes directory found"
fi

echo ""
echo "📋 6. Component Props Analysis"
echo "-----------------------------"

echo "🔍 React Components without proper typing:"
COMPONENT_FILES=$(find src/ -name "*.tsx" 2>/dev/null | head -10) || true
if [ -n "$COMPONENT_FILES" ]; then
    echo "$COMPONENT_FILES" | while read file; do
        if [ -f "$file" ]; then
            echo "📄 Analyzing: $file"
            # Check for interface/type definitions
            if grep -q "interface.*Props\|type.*Props" "$file"; then
                echo "  ✅ Has Props interface/type"
            else
                echo "  ⚠️  Missing Props interface/type"
            fi
        fi
    done
else
    echo "📁 No .tsx component files found"
fi

echo ""
echo "📋 7. Next.js Specific Issues"
echo "----------------------------"

echo "🔍 Checking next.config.js:"
if [ -f "next.config.js" ]; then
    echo "✅ next.config.js found"
    # Check for common issues
    if grep -q "typescript:" next.config.js; then
        echo "  🔧 TypeScript configuration found"
    fi
    if grep -q "eslint:" next.config.js; then
        echo "  🔧 ESLint configuration found"  
    fi
else
    echo "❌ next.config.js NOT FOUND"
fi

echo ""
echo "🔍 Checking _app.tsx:"
if [ -f "pages/_app.tsx" ] || [ -f "src/pages/_app.tsx" ]; then
    echo "✅ _app.tsx found"
else
    echo "⚠️  _app.tsx not found (using default)"
fi

echo ""
echo "🔍 Checking _document.tsx:"
if [ -f "pages/_document.tsx" ] || [ -f "src/pages/_document.tsx" ]; then
    echo "✅ _document.tsx found"
else
    echo "ℹ️  _document.tsx not found (using default)"
fi

echo ""
echo "📋 8. Build Scripts Analysis"
echo "---------------------------"

echo "🔍 Available npm scripts:"
if [ -f "package.json" ]; then
    grep -A 20 '"scripts"' package.json | grep -E '"[^"]+":' | head -10 | while read script; do
        echo "  📜 $script"
    done
    
    echo ""
    echo "🔍 Critical build scripts status:"
    SCRIPTS=("build" "dev" "typecheck" "lint" "test")
    for script in "${SCRIPTS[@]}"; do
        if grep -q "\"$script\":" package.json; then
            echo "  ✅ $script script defined"
        else
            echo "  ❌ $script script MISSING"
        fi
    done
else
    echo "❌ Cannot analyze scripts - package.json missing"
fi

echo ""
echo "📋 9. Environment Configuration"
echo "------------------------------"

ENV_FILES=(".env" ".env.local" ".env.example" ".env.development" ".env.production")
for env_file in "${ENV_FILES[@]}"; do
    if [ -f "$env_file" ]; then
        echo "✅ $env_file found"
        # Count environment variables
        VAR_COUNT=$(grep -c "^[A-Z]" "$env_file" 2>/dev/null || echo "0")
        echo "  📊 Environment variables: $VAR_COUNT"
    else
        echo "ℹ️  $env_file not found"
    fi
done

echo ""
echo "📋 10. Git and CI Configuration"
echo "------------------------------"

if [ -f ".gitignore" ]; then
    echo "✅ .gitignore found"
    if grep -q "node_modules\|\.next\|dist\|build" .gitignore; then
        echo "  ✅ Proper build exclusions configured"
    fi
else
    echo "⚠️  .gitignore not found"
fi

if [ -f ".eslintrc.json" ]; then
    echo "✅ ESLint configuration found"
else
    echo "⚠️  .eslintrc.json not found"
fi

if [ -f ".prettierrc.json" ] || [ -f "prettier.config.js" ]; then
    echo "✅ Prettier configuration found"
else
    echo "⚠️  Prettier configuration not found"
fi

echo ""
echo "📋 AUDIT SUMMARY"
echo "================"
echo ""
echo "🎯 Critical Issues to Address:"
echo ""

# Check for critical issues
CRITICAL_ISSUES=0

# Missing TypeScript config
if [ ! -f "tsconfig.json" ]; then
    echo "❗ CRITICAL: Missing tsconfig.json"
    ((CRITICAL_ISSUES++))
fi

# Missing package.json  
if [ ! -f "package.json" ]; then
    echo "❗ CRITICAL: Missing package.json"
    ((CRITICAL_ISSUES++))
fi

# High warning count
if [ "$TS_FILES" -eq 0 ]; then
    echo "❗ CRITICAL: No TypeScript files found"
    ((CRITICAL_ISSUES++))
fi

if [ "$CRITICAL_ISSUES" -eq 0 ]; then
    echo "✅ No critical issues found - Ready for build testing"
else
    echo "❌ Found $CRITICAL_ISSUES critical issues - Must fix before proceeding"
fi

echo ""
echo "📊 Audit Complete!"
echo "📁 Results saved to: $AUDIT_DIR/"
echo ""
echo "🔧 Next Steps:"
echo "1. Address critical issues if any"
echo "2. Run TypeScript compilation: npm run typecheck"
echo "3. Run build test: npm run build"
echo "4. Fix identified warnings/errors"
echo ""

# Save summary to file
{
    echo "# TypeScript Audit Summary - $(date)"
    echo ""
    echo "## Statistics"
    echo "- TypeScript files: $TS_FILES"
    echo "- @/* imports: $IMPORT_ISSUES"  
    echo "- Relative imports: $RELATIVE_IMPORTS"
    echo "- Critical issues: $CRITICAL_ISSUES"
    echo ""
} > "$AUDIT_DIR/typescript-audit-summary.md"

echo "💾 Audit summary saved to: $AUDIT_DIR/typescript-audit-summary.md"
