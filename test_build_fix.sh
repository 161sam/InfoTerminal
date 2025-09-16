#!/bin/bash

# test_build_fix.sh
# Script to test if InfoTerminal v0.2.0 TypeScript build issues are resolved

set -e

echo "🔧 InfoTerminal v0.2.0 - Testing Build Fix"
echo "==========================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [[ ! -f "package.json" ]] || [[ ! -d "apps/frontend" ]]; then
    echo -e "${RED}❌ Error: Please run this script from the InfoTerminal root directory${NC}"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo ""

# Check TypeScript compilation
echo "🔍 Checking TypeScript compilation..."
echo ""

# Navigate to frontend directory and check types
cd apps/frontend

echo "📋 Checking package.json scripts..."
if grep -q '"build"' package.json; then
    echo -e "${GREEN}✅ Build script found${NC}"
else
    echo -e "${RED}❌ Build script not found${NC}"
    exit 1
fi

echo ""
echo "🔧 Running TypeScript type check..."
echo ""

# Try to compile TypeScript files
if npx tsc --noEmit --skipLibCheck 2>&1; then
    echo -e "${GREEN}✅ TypeScript compilation successful!${NC}"
    echo ""
    
    echo "📝 Key fixes applied:"
    echo "   • Fixed Evidence type from 'Evidence | null' to 'Evidence | undefined'"
    echo "   • Added named export for Button component"
    echo "   • All UI components properly exported"
    echo ""
    
    echo -e "${GREEN}🎉 InfoTerminal v0.2.0 build fix completed successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "   1. Run 'pnpm -w -F @infoterminal/frontend build' to build the frontend"
    echo "   2. Run 'docker-compose -f docker-compose.verification.yml up -d' to start services"
    echo "   3. Run './test_infoterminal_v020_e2e.sh' for comprehensive testing"
    
else
    echo -e "${RED}❌ TypeScript compilation failed${NC}"
    echo ""
    echo "Please check the error messages above and fix any remaining issues."
    exit 1
fi
