#!/bin/bash

# fix_build_errors.sh
# InfoTerminal Frontend Build Error Fixes

echo "🔧 InfoTerminal v0.2.0 - Build Error Fixes"
echo "==========================================="

cd "$(dirname "$0")"

# Install missing dependencies
echo "📦 Installing missing dependencies..."
pnpm add clsx tailwind-merge

echo ""
echo "✅ Build error fixes applied successfully!"
echo ""
echo "🚀 Now run: pnpm -w -F @infoterminal/frontend build"
echo ""
echo "📋 Fixed issues:"
echo "   ✅ fetch() timeout error in security/status.ts"
echo "   ✅ Missing Badge, Progress, Alert, Textarea UI components"  
echo "   ✅ Missing cn() utility function"
echo "   ✅ Missing Card component exports"
echo "   ✅ Added clsx and tailwind-merge dependencies"
echo ""
