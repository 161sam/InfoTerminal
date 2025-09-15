#!/bin/bash

# InfoTerminal v0.2.0 - Backup Files Cleanup Script
# This script removes migration artifacts and backup files

echo "🧹 Cleaning up InfoTerminal migration artifacts and backup files..."

# Critical backup files from analysis document
echo "Removing critical backup files..."
rm -v .gitignore.bak.20250902233015
rm -v Makefile.bak.20250902233320
rm -v migration_20250903_132819.log

# Docker compose backup files
echo "Removing docker-compose backup files..."
rm -v docker-compose.yml.bak.*
rm -v docker-compose.*.bak.*

# Frontend backup files
echo "Removing frontend backup files..."
rm -v apps/frontend/.env.local.bak.*
rm -v apps/frontend/package.json.bak.*

# Other backup files found
echo "Removing other backup files..."
find . -name "*.bak.*" -type f -delete

# Verify cleanup
echo ""
echo "✅ Cleanup completed!"
echo "Remaining backup files (should be empty):"
find . -name "*.bak.*" -o -name "migration_*.log" 2>/dev/null || echo "  (None found - cleanup successful!)"

echo ""
echo "🎯 Migration cleanup completed successfully!"
echo "Next steps:"
echo "  1. Run the test suite: make test"
echo "  2. Test the operations UI: http://localhost:3000/settings (ops tab)"
echo "  3. Test the doc-entities resolver: curl -X POST http://localhost:8613/resolve/{doc_id}"
