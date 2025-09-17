#!/bin/bash

# Docker Build Test Script
# Tests the build fixes for InfoTerminal v0.2.0

set -e

echo "🔧 Testing Docker Build Fixes..."
echo "================================="

# Test individual service builds
echo "Testing ops-controller build..."
if docker build -t test-ops-controller -f services/ops-controller/Dockerfile .; then
    echo "✅ ops-controller build successful"
    docker rmi test-ops-controller >/dev/null 2>&1 || true
else
    echo "❌ ops-controller build failed"
    exit 1
fi

echo "Testing verification-service build..."
if docker build -t test-verification -f services/verification/Dockerfile .; then
    echo "✅ verification-service build successful"
    docker rmi test-verification >/dev/null 2>&1 || true
else
    echo "❌ verification-service build failed"
    exit 1
fi

echo "Testing search-api build..."
if docker build -t test-search-api -f services/search-api/Dockerfile .; then
    echo "✅ search-api build successful"
    docker rmi test-search-api >/dev/null 2>&1 || true
else
    echo "❌ search-api build failed"
    exit 1
fi

echo ""
echo "🎉 All Docker builds successful!"
echo "Ready to run: docker-compose -f docker-compose.verification.yml up -d"

