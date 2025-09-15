#!/bin/bash

# InfoTerminal v0.2.0 - Validation and Testing Script
# This script validates that all critical v0.2.0 functionality is working

echo "InfoTerminal v0.2.0 - Functionality Validation"
echo "============================================="

# Function to check if service is responding
check_service() {
    local name=$1
    local url=$2
    echo "Checking $name ($url)..."
    
    if curl -f -s "$url" > /dev/null 2>&1; then
        echo "  ✓ $name is responding"
        return 0
    else
        echo "  ✗ $name is NOT responding"
        return 1
    fi
}

# Function to test API endpoint
test_api_endpoint() {
    local name=$1
    local method=$2
    local url=$3
    local data=$4
    echo "Testing $name..."
    
    if [ "$method" = "POST" ] && [ -n "$data" ]; then
        response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" "$url")
    else
        response=$(curl -s "$url")
    fi
    
    if [ $? -eq 0 ] && [ -n "$response" ]; then
        echo "  ✓ $name working"
        return 0
    else
        echo "  ✗ $name failed"
        return 1
    fi
}

echo ""
echo "1. CORE SERVICE HEALTH CHECKS"
echo "------------------------------"

# Check core services
check_service "doc-entities" "http://localhost:8613/healthz"
check_service "search-api" "http://localhost:8611/healthz" 
check_service "graph-api" "http://localhost:8612/healthz"
check_service "ops-controller" "http://localhost:8614/ops/stacks"

echo ""
echo "2. DOC-ENTITIES RESOLVER FUNCTIONALITY"
echo "--------------------------------------"

# Test doc-entities NER
echo "Testing doc-entities NER endpoint..."
ner_response=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"text": "Barack Obama was born in Hawaii."}' \
  "http://localhost:8613/ner")

if echo "$ner_response" | grep -q "entities"; then
    echo "  ✓ NER endpoint working"
else
    echo "  ✗ NER endpoint failed"
fi

# Test doc-entities annotation with resolver
echo "Testing doc-entities annotation..."
annot_response=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"text": "John Smith works at Apple Inc in New York.", "title": "Test Doc"}' \
  "http://localhost:8613/annotate")

if echo "$annot_response" | grep -q "doc_id"; then
    echo "  ✓ Annotation endpoint working"
    
    # Extract doc_id for resolver tests
    doc_id=$(echo "$annot_response" | grep -o '"doc_id":"[^"]*"' | cut -d'"' -f4)
    if [ -n "$doc_id" ]; then
        echo "  Document ID: $doc_id"
        
        # Test document resolution (no longer HTTP 501)
        echo "Testing document resolution..."
        resolve_response=$(curl -s -X POST "http://localhost:8613/resolve/$doc_id")
        
        if echo "$resolve_response" | grep -q "resolution_started"; then
            echo "  ✓ Document resolution working (no longer HTTP 501)"
        else
            echo "  ✗ Document resolution failed"
        fi
        
        # Test individual entity resolution if entities exist
        entity_id=$(echo "$annot_response" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
        if [ -n "$entity_id" ]; then
            echo "Testing entity resolution..."
            entity_resolve_response=$(curl -s -X POST "http://localhost:8613/resolve/entity/$entity_id")
            
            if echo "$entity_resolve_response" | grep -q "resolution"; then
                echo "  ✓ Entity resolution working (no longer HTTP 501)"
            else
                echo "  ✗ Entity resolution failed"
            fi
        fi
    fi
else
    echo "  ✗ Annotation endpoint failed"
fi

echo ""
echo "3. OPERATIONS UI API ENDPOINTS"
echo "-------------------------------"

# Test frontend operations API endpoints
test_api_endpoint "Operations API - Stacks List" "GET" "http://localhost:3000/api/ops/stacks"

echo ""
echo "4. FRONTEND ACCESSIBILITY"
echo "-------------------------"

check_service "Frontend" "http://localhost:3000"

echo "Testing frontend pages..."
if curl -f -s "http://localhost:3000" > /dev/null 2>&1; then
    echo "  ✓ Frontend main page accessible"
else
    echo "  ✗ Frontend main page not accessible"
fi

if curl -f -s "http://localhost:3000/nlp" > /dev/null 2>&1; then
    echo "  ✓ Frontend NLP page accessible"
else
    echo "  ✗ Frontend NLP page not accessible"
fi

if curl -f -s "http://localhost:3000/settings" > /dev/null 2>&1; then
    echo "  ✓ Frontend Settings page accessible"
else
    echo "  ✗ Frontend Settings page not accessible"
fi

echo ""
echo "5. DOCKER STACK CONFIGURATION"
echo "-----------------------------"

# Check if required compose files exist
files=("docker-compose.yml" "docker-compose.nlp.yml" "infra/ops/stacks.yaml")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
    fi
done

# Check if legacy service is removed
if [ ! -d "services/nlp-service" ]; then
    echo "  ✓ Legacy nlp-service directory removed/archived"
else
    echo "  ! Legacy nlp-service directory still exists"
fi

# Check if tests exist
if [ -f "tests/test_doc_entities_integration.py" ]; then
    echo "  ✓ New doc-entities integration tests exist"
else
    echo "  ✗ New integration tests missing"
fi

if [ -f "tests/test_nlp_integration.legacy.py" ]; then
    echo "  ✓ Legacy tests archived"
else
    echo "  ! Legacy tests not found"
fi

echo ""
echo "6. CONFIGURATION VALIDATION"  
echo "---------------------------"

# Check .env.example for required settings
if grep -q "IT_OPS_ENABLE=1" .env.example; then
    echo "  ✓ Operations controller enabled by default"
else
    echo "  ✗ Operations controller not enabled by default"
fi

if grep -q "OPS_CONTROLLER_URL" .env.example; then
    echo "  ✓ Operations controller URL configured"
else
    echo "  ✗ Operations controller URL not configured"
fi

if grep -q "IT_PORT_DOC_ENTITIES" .env.example; then
    echo "  ✓ Doc-entities port configured"
else
    echo "  ✗ Doc-entities port not configured"
fi

echo ""
echo "7. MIGRATION CLEANUP STATUS"
echo "---------------------------"

backup_count=$(find . -name "*.bak.*" 2>/dev/null | wc -l)
migration_count=$(find . -name "migration_*.log" 2>/dev/null | wc -l)

echo "  Backup files remaining: $backup_count"
echo "  Migration logs remaining: $migration_count"

if [ "$backup_count" -eq 0 ] && [ "$migration_count" -eq 0 ]; then
    echo "  ✓ Migration cleanup complete"
else
    echo "  ! Migration cleanup needed (run cleanup_backup_files.sh)"
fi

echo ""
echo "============================================="
echo "InfoTerminal v0.2.0 Validation Complete"
echo ""
echo "NEXT STEPS:"
echo "- If any tests failed, check service logs"
echo "- Run: docker-compose up -d"
echo "- Run: make test (for full test suite)"
echo "- Access Operations UI: http://localhost:3000/settings"
echo "- Test NLP functionality: http://localhost:3000/nlp"
echo ""
echo "For support issues:"
echo "- Check docker-compose logs [service-name]"
echo "- Verify .env file matches .env.example"
echo "- Ensure Docker daemon is running"
