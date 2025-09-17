#!/bin/bash

echo "🧪 Testing Docker Build Fixes for InfoTerminal v0.2.0"
echo "======================================================"

# Test the individual services that were problematic
echo ""
echo "1. Testing ops-controller build..."
if docker build -t test-ops-controller -f services/ops-controller/Dockerfile . > /dev/null 2>&1; then
    echo "   ✅ ops-controller build SUCCESS"
    docker rmi test-ops-controller > /dev/null 2>&1
else
    echo "   ❌ ops-controller build FAILED"
    echo "   Detailed error:"
    docker build -f services/ops-controller/Dockerfile .
    exit 1
fi

echo ""
echo "2. Testing verification-service build..."  
if docker build -t test-verification -f services/verification/Dockerfile . > /dev/null 2>&1; then
    echo "   ✅ verification-service build SUCCESS"
    docker rmi test-verification > /dev/null 2>&1
else
    echo "   ❌ verification-service build FAILED"
    echo "   Detailed error:"
    docker build -f services/verification/Dockerfile .
    exit 1
fi

echo ""
echo "3. Testing doc-entities build..."
if docker build -t test-doc-entities -f services/doc-entities/Dockerfile . > /dev/null 2>&1; then
    echo "   ✅ doc-entities build SUCCESS" 
    docker rmi test-doc-entities > /dev/null 2>&1
else
    echo "   ❌ doc-entities build FAILED"
    echo "   Detailed error:"
    docker build -f services/doc-entities/Dockerfile .
    exit 1
fi

echo ""
echo "🎉 All individual Docker builds successful!"
echo ""
echo "Now testing Docker Compose configuration..."
if docker compose -f docker-compose.verification.yml config > /dev/null 2>&1; then
    echo "   ✅ docker-compose.verification.yml configuration valid"
else  
    echo "   ❌ docker-compose.verification.yml configuration invalid"
    docker compose -f docker-compose.verification.yml config
    exit 1
fi

echo ""
echo "🚀 Ready to deploy InfoTerminal v0.2.0!"
echo "Run: docker compose -f docker-compose.verification.yml up -d"

