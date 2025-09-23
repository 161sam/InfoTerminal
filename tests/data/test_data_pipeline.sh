#!/bin/bash

# test_data_pipeline.sh
# InfoTerminal v1.0.0 - Test Data Management Pipeline
# Handles: Seed Data, Fixtures, Cleanup, Isolation

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}"
SEEDS_DIR="${DATA_DIR}/seeds"
FIXTURES_DIR="${DATA_DIR}/fixtures"
TEMP_DIR="${DATA_DIR}/temp"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Database configuration
NEO4J_URI="${IT_NEO4J_URI:-bolt://localhost:7687}"
NEO4J_USER="${IT_NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${IT_NEO4J_PASSWORD:-testpassword}"
OPENSEARCH_URL="${IT_OPENSEARCH_URL:-http://localhost:9200}"
POSTGRES_URL="${IT_POSTGRES_URL:-postgresql://test:testpass@localhost:5432/infoterminal_test}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging
log() {
    echo -e "$1" | tee -a "${DATA_DIR}/test_data_${TIMESTAMP}.log"
}

log_header() {
    echo ""
    echo "=================================================================="
    log "${BLUE}$1${NC}"
    echo "=================================================================="
    echo ""
}

log_info() {
    log "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    log "${GREEN}✅ $1${NC}"
}

log_warn() {
    log "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    log "${RED}❌ $1${NC}"
}

# Initialize directories
init_directories() {
    mkdir -p "$SEEDS_DIR" "$FIXTURES_DIR" "$TEMP_DIR"
    
    # Create gitignore for temp directory
    echo "*" > "$TEMP_DIR/.gitignore"
    echo "!.gitignore" >> "$TEMP_DIR/.gitignore"
}

# Create realistic test datasets
create_seed_data() {
    log_header "Creating Seed Data"
    
    # OSINT-typical entities for graph testing
    cat > "$SEEDS_DIR/entities.json" << 'EOF'
{
  "entities": [
    {
      "id": "org_1",
      "name": "International Monetary Fund",
      "type": "organization",
      "aliases": ["IMF"],
      "properties": {
        "founded": "1944",
        "headquarters": "Washington D.C.",
        "type": "international_organization",
        "website": "https://www.imf.org"
      }
    },
    {
      "id": "org_2", 
      "name": "Federal Reserve System",
      "type": "organization",
      "aliases": ["Federal Reserve", "Fed", "US Central Bank"],
      "properties": {
        "founded": "1913",
        "headquarters": "Washington D.C.",
        "type": "central_bank",
        "website": "https://www.federalreserve.gov"
      }
    },
    {
      "id": "person_1",
      "name": "Jerome Powell",
      "type": "person",
      "properties": {
        "title": "Chair of the Federal Reserve",
        "appointed": "2018",
        "education": "Georgetown University",
        "previous_role": "Investment banker"
      }
    },
    {
      "id": "concept_1",
      "name": "Federal Funds Rate",
      "type": "economic_concept",
      "properties": {
        "definition": "Interest rate at which banks lend to each other overnight",
        "current_range": "5.25-5.50%",
        "last_change": "2024-07-31"
      }
    },
    {
      "id": "event_1",
      "name": "FOMC Meeting July 2024",
      "type": "event",
      "properties": {
        "date": "2024-07-30-31",
        "location": "Washington D.C.",
        "outcome": "Rate held at 5.25-5.50%",
        "next_meeting": "2024-09-17-18"
      }
    }
  ],
  "relationships": [
    {
      "from": "person_1",
      "to": "org_2",
      "type": "leads",
      "properties": {
        "since": "2018",
        "role": "Chairman"
      }
    },
    {
      "from": "org_2",
      "to": "concept_1",
      "type": "controls",
      "properties": {
        "mechanism": "Federal Open Market Committee",
        "frequency": "8 meetings per year"
      }
    },
    {
      "from": "event_1",
      "to": "concept_1",
      "type": "affected",
      "properties": {
        "decision": "no_change",
        "rationale": "inflation_monitoring"
      }
    },
    {
      "from": "org_1",
      "to": "org_2",
      "type": "cooperates_with",
      "properties": {
        "areas": ["global_financial_stability", "crisis_response"],
        "formal_agreements": true
      }
    }
  ]
}
EOF

    # Sample documents for NLP testing
    cat > "$SEEDS_DIR/documents.json" << 'EOF'
{
  "documents": [
    {
      "id": "doc_1",
      "title": "Federal Reserve Policy Statement July 2024",
      "content": "The Federal Open Market Committee decided to maintain the target range for the federal funds rate at 5-1/4 to 5-1/2 percent. The Committee continues to be highly attentive to inflation risks. Recent indicators suggest that economic activity has continued to expand at a solid pace. Job gains have remained strong, and the unemployment rate has remained low. Inflation remains elevated.",
      "source": "Federal Reserve System",
      "date": "2024-07-31",
      "type": "policy_statement",
      "url": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20240731a.htm"
    },
    {
      "id": "doc_2", 
      "title": "IMF World Economic Outlook Update",
      "content": "The International Monetary Fund projects global economic growth to slow to 3.1 percent in 2024 from 3.5 percent in 2023. Advanced economies are expected to see growth slow to 1.7 percent in 2024. Emerging market and developing economies are projected to grow by 4.1 percent. Inflation is expected to decline steadily, with global headline inflation forecast to fall to 5.8 percent in 2024.",
      "source": "International Monetary Fund",
      "date": "2024-07-16",
      "type": "economic_forecast",
      "url": "https://www.imf.org/en/Publications/WEO/Issues/2024/07/16/world-economic-outlook-update-july-2024"
    },
    {
      "id": "doc_3",
      "title": "Climate Policy and Economic Growth",
      "content": "Transitioning to renewable energy sources presents both challenges and opportunities for economic growth. Studies indicate that renewable energy investments can create more jobs per dollar spent than fossil fuel investments. However, the transition requires significant upfront capital and policy coordination. Carbon pricing mechanisms and green bonds are emerging as key financial instruments to support this transition.",
      "source": "Academic Research",
      "date": "2024-06-15",
      "type": "research_paper",
      "topics": ["climate_change", "renewable_energy", "economic_policy"]
    },
    {
      "id": "doc_4",
      "title": "Artificial Intelligence in Financial Services",
      "content": "Artificial intelligence and machine learning technologies are transforming financial services. Banks are using AI for fraud detection, risk assessment, and customer service automation. Regulatory bodies are developing frameworks to govern AI use in finance, focusing on transparency, fairness, and systemic risk management. The technology promises increased efficiency but raises concerns about algorithmic bias and job displacement.",
      "source": "FinTech Analysis",
      "date": "2024-08-10",
      "type": "industry_report",
      "topics": ["artificial_intelligence", "financial_services", "regulation"]
    }
  ]
}
EOF

    # Search index test data
    cat > "$SEEDS_DIR/search_data.json" << 'EOF'
{
  "search_entries": [
    {
      "id": "search_1",
      "title": "Federal Reserve Interest Rate Decision",
      "content": "The Federal Reserve maintains interest rates at 5.25-5.50% as inflation concerns persist",
      "source": "Financial News",
      "timestamp": "2024-07-31T14:00:00Z",
      "tags": ["federal_reserve", "interest_rates", "monetary_policy"],
      "relevance_score": 0.95
    },
    {
      "id": "search_2",
      "title": "IMF Global Growth Projections",
      "content": "International Monetary Fund lowers global growth forecast to 3.1% for 2024",
      "source": "Economic Report", 
      "timestamp": "2024-07-16T10:30:00Z",
      "tags": ["imf", "economic_growth", "global_economy"],
      "relevance_score": 0.89
    },
    {
      "id": "search_3",
      "title": "Renewable Energy Investment Trends",
      "content": "Global renewable energy capacity additions reached record levels in 2024",
      "source": "Energy Report",
      "timestamp": "2024-06-20T08:15:00Z",
      "tags": ["renewable_energy", "investment", "climate"],
      "relevance_score": 0.82
    },
    {
      "id": "search_4",
      "title": "AI in Banking Sector Analysis",
      "content": "Artificial intelligence adoption accelerates in financial services with focus on compliance",
      "source": "Technology News",
      "timestamp": "2024-08-05T16:45:00Z",
      "tags": ["artificial_intelligence", "banking", "fintech"],
      "relevance_score": 0.77
    }
  ]
}
EOF

    # Verification test claims
    cat > "$SEEDS_DIR/claims.json" << 'EOF'
{
  "claims": [
    {
      "id": "claim_1",
      "text": "The Federal Reserve maintains interest rates at 5.25-5.50% as of July 2024",
      "source": "Financial news",
      "confidence": 0.95,
      "verifiable": true,
      "category": "monetary_policy",
      "evidence_sources": ["federal_reserve_statement", "financial_press"],
      "stance": "factual"
    },
    {
      "id": "claim_2", 
      "text": "Global economic growth is projected to be 3.1% in 2024 according to the IMF",
      "source": "Economic report",
      "confidence": 0.91,
      "verifiable": true,
      "category": "economic_forecast",
      "evidence_sources": ["imf_weo", "economic_analysis"],
      "stance": "factual"
    },
    {
      "id": "claim_3",
      "text": "Renewable energy investments create more jobs than fossil fuel investments",
      "source": "Research study",
      "confidence": 0.73,
      "verifiable": true,
      "category": "economic_analysis",
      "evidence_sources": ["academic_research", "industry_studies"],
      "stance": "supported"
    },
    {
      "id": "claim_4",
      "text": "AI will replace all human jobs in financial services by 2030",
      "source": "Opinion article",
      "confidence": 0.15,
      "verifiable": false,
      "category": "technology_prediction", 
      "evidence_sources": [],
      "stance": "speculative"
    }
  ]
}
EOF

    log_success "Seed data created successfully"
}

# Create test fixtures for specific scenarios
create_test_fixtures() {
    log_header "Creating Test Fixtures"
    
    # Verification workflow fixture
    cat > "$FIXTURES_DIR/verification_workflow.json" << 'EOF'
{
  "name": "Verification Workflow Test",
  "description": "End-to-end verification workflow with realistic data",
  "steps": [
    {
      "step": "claim_extraction",
      "input": {
        "text": "The Federal Reserve announced that it would maintain the federal funds rate at 5.25-5.50 percent during its July 2024 meeting. This decision reflects the committee's ongoing commitment to bringing inflation down to the 2 percent target.",
        "options": {
          "max_claims": 3,
          "confidence_threshold": 0.7
        }
      },
      "expected_output": {
        "claims": [
          "Federal Reserve maintains federal funds rate at 5.25-5.50 percent",
          "Decision made during July 2024 meeting",
          "Committee committed to bringing inflation to 2 percent target"
        ]
      }
    },
    {
      "step": "evidence_retrieval",
      "input": {
        "claim": "Federal Reserve maintains federal funds rate at 5.25-5.50 percent",
        "max_sources": 5
      },
      "expected_output": {
        "sources": [
          {
            "url": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20240731a.htm",
            "credibility": 0.98,
            "relevance": 0.95
          }
        ]
      }
    }
  ]
}
EOF

    # Search workflow fixture
    cat > "$FIXTURES_DIR/search_workflow.json" << 'EOF'
{
  "name": "Search Workflow Test",
  "description": "Search functionality with ranking and filtering",
  "test_cases": [
    {
      "query": "federal reserve interest rates",
      "filters": {
        "date_range": "2024-01-01:2024-12-31",
        "source_type": "official"
      },
      "expected_results": {
        "min_results": 1,
        "top_result_relevance": 0.9,
        "contains_terms": ["federal", "reserve", "interest", "rates"]
      }
    },
    {
      "query": "IMF economic growth forecast 2024",
      "filters": {
        "source_type": "economic"
      },
      "expected_results": {
        "min_results": 1,
        "top_result_relevance": 0.85,
        "contains_terms": ["IMF", "economic", "growth", "2024"]
      }
    }
  ]
}
EOF

    # Graph workflow fixture
    cat > "$FIXTURES_DIR/graph_workflow.json" << 'EOF'
{
  "name": "Graph Workflow Test", 
  "description": "Entity creation and relationship building",
  "entities": [
    {
      "name": "Test_Organization_Fed",
      "type": "organization",
      "properties": {
        "test_marker": "integration_test",
        "created_at": "2024-01-01T00:00:00Z"
      }
    },
    {
      "name": "Test_Person_Powell",
      "type": "person", 
      "properties": {
        "test_marker": "integration_test",
        "role": "central_banker"
      }
    }
  ],
  "relationships": [
    {
      "from": "Test_Person_Powell",
      "to": "Test_Organization_Fed",
      "type": "leads",
      "properties": {
        "test_marker": "integration_test",
        "since": "2018"
      }
    }
  ],
  "expected_analytics": {
    "min_nodes": 2,
    "min_relationships": 1,
    "connected_components": 1
  }
}
EOF

    # NLP workflow fixture  
    cat > "$FIXTURES_DIR/nlp_workflow.json" << 'EOF'
{
  "name": "NLP Workflow Test",
  "description": "Document processing and entity extraction",
  "documents": [
    {
      "text": "The International Monetary Fund (IMF) announced today that Jerome Powell, Chairman of the Federal Reserve, will participate in the upcoming Global Financial Stability meeting in Washington D.C. The meeting will address current monetary policy challenges and inflation targets.",
      "expected_entities": [
        {"text": "International Monetary Fund", "type": "ORGANIZATION"},
        {"text": "IMF", "type": "ORGANIZATION"}, 
        {"text": "Jerome Powell", "type": "PERSON"},
        {"text": "Federal Reserve", "type": "ORGANIZATION"},
        {"text": "Washington D.C.", "type": "LOCATION"},
        {"text": "Global Financial Stability meeting", "type": "EVENT"}
      ],
      "expected_relationships": [
        {"source": "Jerome Powell", "target": "Federal Reserve", "type": "AFFILIATED_WITH"},
        {"source": "Global Financial Stability meeting", "target": "Washington D.C.", "type": "LOCATED_IN"}
      ]
    }
  ]
}
EOF

    # Performance test fixture
    cat > "$FIXTURES_DIR/performance_baseline.json" << 'EOF'
{
  "name": "Performance Baseline",
  "description": "Expected performance thresholds for quality gates",
  "thresholds": {
    "api_endpoints": {
      "p95_response_time_ms": 200,
      "success_rate_percent": 99.0,
      "throughput_rps": 100
    },
    "search_queries": {
      "p95_response_time_ms": 500,
      "success_rate_percent": 97.0,
      "throughput_rps": 50
    },
    "graph_queries": {
      "p95_response_time_ms": 1000,
      "success_rate_percent": 95.0,
      "throughput_rps": 25
    },
    "nlp_processing": {
      "p95_response_time_ms": 2000,
      "success_rate_percent": 90.0,
      "throughput_rps": 10
    }
  },
  "resource_limits": {
    "memory_usage_percent": 80,
    "cpu_usage_percent": 70,
    "disk_io_mbps": 100
  }
}
EOF

    log_success "Test fixtures created successfully"
}

# Database seeding functions
seed_neo4j_database() {
    log_info "Seeding Neo4j database..."
    
    if ! command -v cypher-shell >/dev/null; then
        log_warn "cypher-shell not available, skipping Neo4j seeding"
        return 0
    fi
    
    # Check Neo4j connectivity
    if ! cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" "RETURN 1" >/dev/null 2>&1; then
        log_warn "Neo4j not accessible, skipping seeding"
        return 0
    fi
    
    # Clear test data first
    cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
        "MATCH (n) WHERE n.test_marker = 'integration_test' DETACH DELETE n" >/dev/null 2>&1 || true
    
    # Load entities
    if [[ -f "$SEEDS_DIR/entities.json" ]]; then
        jq -r '.entities[] | 
          "CREATE (:" + .type + " {" +
          "id: \"" + .id + "\", " +
          "name: \"" + .name + "\", " +
          "test_marker: \"integration_test\", " +
          (.properties | to_entries | map(.key + ": \"" + (.value | tostring) + "\"") | join(", ")) +
          "})"' "$SEEDS_DIR/entities.json" | while read -r cypher; do
            cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" "$cypher" >/dev/null 2>&1 || true
        done
    fi
    
    # Load relationships
    if [[ -f "$SEEDS_DIR/entities.json" ]]; then
        jq -r '.relationships[] |
          "MATCH (a {id: \"" + .from + "\"}), (b {id: \"" + .to + "\"}) " +
          "CREATE (a)-[:" + (.type | ascii_upcase) + " {" +
          (.properties | to_entries | map(.key + ": \"" + (.value | tostring) + "\"") | join(", ")) +
          "}]->(b)"' "$SEEDS_DIR/entities.json" | while read -r cypher; do
            cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" "$cypher" >/dev/null 2>&1 || true
        done
    fi
    
    log_success "Neo4j database seeded successfully"
}

seed_opensearch_index() {
    log_info "Seeding OpenSearch index..."
    
    if ! curl -s "$OPENSEARCH_URL" >/dev/null 2>&1; then
        log_warn "OpenSearch not accessible, skipping seeding"
        return 0
    fi
    
    # Create test index
    local test_index="infoterminal_test_$(date +%s)"
    
    curl -s -X PUT "$OPENSEARCH_URL/$test_index" \
        -H "Content-Type: application/json" \
        -d '{
          "mappings": {
            "properties": {
              "title": {"type": "text"},
              "content": {"type": "text"},
              "source": {"type": "keyword"},
              "timestamp": {"type": "date"},
              "tags": {"type": "keyword"},
              "relevance_score": {"type": "float"}
            }
          }
        }' >/dev/null 2>&1 || true
    
    # Index search data
    if [[ -f "$SEEDS_DIR/search_data.json" ]]; then
        jq -c '.search_entries[]' "$SEEDS_DIR/search_data.json" | while read -r entry; do
            local doc_id=$(echo "$entry" | jq -r '.id')
            curl -s -X PUT "$OPENSEARCH_URL/$test_index/_doc/$doc_id" \
                -H "Content-Type: application/json" \
                -d "$entry" >/dev/null 2>&1 || true
        done
    fi
    
    # Store index name for cleanup
    echo "$test_index" > "$TEMP_DIR/opensearch_test_index"
    
    log_success "OpenSearch index seeded successfully"
}

seed_postgres_database() {
    log_info "Seeding PostgreSQL database..."
    
    if ! command -v psql >/dev/null; then
        log_warn "psql not available, skipping PostgreSQL seeding"
        return 0
    fi
    
    # Test connectivity
    if ! psql "$POSTGRES_URL" -c "SELECT 1" >/dev/null 2>&1; then
        log_warn "PostgreSQL not accessible, skipping seeding"
        return 0
    fi
    
    # Create test tables
    psql "$POSTGRES_URL" << 'EOF' >/dev/null 2>&1 || true
CREATE TABLE IF NOT EXISTS test_claims (
    id VARCHAR PRIMARY KEY,
    text TEXT,
    source VARCHAR,
    confidence FLOAT,
    verifiable BOOLEAN,
    category VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS test_documents (
    id VARCHAR PRIMARY KEY,
    title VARCHAR,
    content TEXT,
    source VARCHAR,
    doc_date DATE,
    doc_type VARCHAR,
    url VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);
EOF
    
    # Insert claim data
    if [[ -f "$SEEDS_DIR/claims.json" ]]; then
        jq -r '.claims[] | 
          "INSERT INTO test_claims (id, text, source, confidence, verifiable, category) VALUES (" +
          "\"" + .id + "\", " +
          "\"" + (.text | gsub("\""; "\"\"")) + "\", " +
          "\"" + .source + "\", " +
          (.confidence | tostring) + ", " +
          (.verifiable | tostring) + ", " +
          "\"" + .category + "\"" +
          ") ON CONFLICT (id) DO NOTHING;"' "$SEEDS_DIR/claims.json" | while read -r sql; do
            psql "$POSTGRES_URL" -c "$sql" >/dev/null 2>&1 || true
        done
    fi
    
    # Insert document data
    if [[ -f "$SEEDS_DIR/documents.json" ]]; then
        jq -r '.documents[] |
          "INSERT INTO test_documents (id, title, content, source, doc_date, doc_type, url) VALUES (" +
          "\"" + .id + "\", " +
          "\"" + (.title | gsub("\""; "\"\"")) + "\", " +
          "\"" + (.content | gsub("\""; "\"\"")) + "\", " + 
          "\"" + .source + "\", " +
          "\"" + .date + "\", " +
          "\"" + .type + "\", " +
          "\"" + (.url // "") + "\"" +
          ") ON CONFLICT (id) DO NOTHING;"' "$SEEDS_DIR/documents.json" | while read -r sql; do
            psql "$POSTGRES_URL" -c "$sql" >/dev/null 2>&1 || true
        done
    fi
    
    log_success "PostgreSQL database seeded successfully"
}

# Cleanup functions
cleanup_test_data() {
    log_header "Cleaning Up Test Data"
    
    # Neo4j cleanup
    if command -v cypher-shell >/dev/null && \
       cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" "RETURN 1" >/dev/null 2>&1; then
        log_info "Cleaning Neo4j test data..."
        cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
            "MATCH (n) WHERE n.test_marker = 'integration_test' DETACH DELETE n" >/dev/null 2>&1 || true
        log_success "Neo4j test data cleaned"
    fi
    
    # OpenSearch cleanup
    if curl -s "$OPENSEARCH_URL" >/dev/null 2>&1 && [[ -f "$TEMP_DIR/opensearch_test_index" ]]; then
        local test_index=$(cat "$TEMP_DIR/opensearch_test_index")
        log_info "Cleaning OpenSearch test index: $test_index"
        curl -s -X DELETE "$OPENSEARCH_URL/$test_index" >/dev/null 2>&1 || true
        rm -f "$TEMP_DIR/opensearch_test_index"
        log_success "OpenSearch test data cleaned"
    fi
    
    # PostgreSQL cleanup
    if command -v psql >/dev/null && \
       psql "$POSTGRES_URL" -c "SELECT 1" >/dev/null 2>&1; then
        log_info "Cleaning PostgreSQL test data..."
        psql "$POSTGRES_URL" << 'EOF' >/dev/null 2>&1 || true
DROP TABLE IF EXISTS test_claims;
DROP TABLE IF EXISTS test_documents;
EOF
        log_success "PostgreSQL test data cleaned"
    fi
    
    # Clean temporary files
    rm -rf "$TEMP_DIR"/*
    log_success "Temporary files cleaned"
}

# Validate test data integrity
validate_test_data() {
    log_header "Validating Test Data Integrity"
    
    local validation_errors=0
    
    # Validate JSON files
    for json_file in "$SEEDS_DIR"/*.json "$FIXTURES_DIR"/*.json; do
        if [[ -f "$json_file" ]]; then
            if ! jq empty "$json_file" >/dev/null 2>&1; then
                log_error "Invalid JSON in $json_file"
                validation_errors=$((validation_errors + 1))
            else
                log_info "✓ Valid JSON: $(basename "$json_file")"
            fi
        fi
    done
    
    # Validate seed data structure
    if [[ -f "$SEEDS_DIR/entities.json" ]]; then
        local entity_count=$(jq '.entities | length' "$SEEDS_DIR/entities.json")
        local relationship_count=$(jq '.relationships | length' "$SEEDS_DIR/entities.json")
        log_info "✓ Entities: $entity_count, Relationships: $relationship_count"
    fi
    
    if [[ -f "$SEEDS_DIR/documents.json" ]]; then
        local document_count=$(jq '.documents | length' "$SEEDS_DIR/documents.json")
        log_info "✓ Documents: $document_count"
    fi
    
    if [[ -f "$SEEDS_DIR/claims.json" ]]; then
        local claim_count=$(jq '.claims | length' "$SEEDS_DIR/claims.json")
        log_info "✓ Claims: $claim_count"
    fi
    
    if [[ $validation_errors -eq 0 ]]; then
        log_success "All test data validation passed"
        return 0
    else
        log_error "$validation_errors validation errors found"
        return 1
    fi
}

# Export data for external tools
export_test_data() {
    local export_format="${1:-json}"
    local export_dir="${DATA_DIR}/exports"
    
    log_header "Exporting Test Data ($export_format format)"
    
    mkdir -p "$export_dir"
    
    case "$export_format" in
        "json")
            # Combine all seed data into a single export
            jq -n '
                {
                    "entities": input,
                    "documents": input,
                    "claims": input,
                    "search_data": input
                }
            ' \
            "$SEEDS_DIR/entities.json" \
            "$SEEDS_DIR/documents.json" \
            "$SEEDS_DIR/claims.json" \
            "$SEEDS_DIR/search_data.json" > "$export_dir/combined_test_data.json"
            ;;
        "csv")
            # Export entities as CSV
            if [[ -f "$SEEDS_DIR/entities.json" ]]; then
                jq -r '.entities[] | [.id, .name, .type, (.properties | @json)] | @csv' \
                    "$SEEDS_DIR/entities.json" > "$export_dir/entities.csv"
            fi
            
            # Export documents as CSV
            if [[ -f "$SEEDS_DIR/documents.json" ]]; then
                jq -r '.documents[] | [.id, .title, .source, .date, .type] | @csv' \
                    "$SEEDS_DIR/documents.json" > "$export_dir/documents.csv"
            fi
            ;;
        "sql")
            # Generate SQL insert statements
            cat > "$export_dir/test_data.sql" << 'EOF'
-- Test data SQL export
-- Generated by InfoTerminal test data pipeline

BEGIN;
EOF
            
            # Add entity inserts
            if [[ -f "$SEEDS_DIR/entities.json" ]]; then
                echo "" >> "$export_dir/test_data.sql"
                echo "-- Entities" >> "$export_dir/test_data.sql"
                jq -r -f - "$SEEDS_DIR/entities.json" >> "$export_dir/test_data.sql" <<'JQ'
.entities[] |
  "INSERT INTO entities (id, name, type, properties) VALUES ('"
  + (.id | tostring | gsub("'"; "''")) + "', '"
  + (.name | tostring | gsub("'"; "''")) + "', '"
  + (.type | tostring | gsub("'"; "''")) + "', '"
  + ((.properties | @json) | gsub("'"; "''")) + "');"
JQ
            fi
            
            echo "" >> "$export_dir/test_data.sql"
            echo "COMMIT;" >> "$export_dir/test_data.sql"
            ;;
    esac
    
    log_success "Test data exported to $export_dir"
}

# Main execution functions
seed_all_databases() {
    log_header "Seeding All Test Databases"
    
    seed_neo4j_database
    seed_opensearch_index
    seed_postgres_database
    
    log_success "All databases seeded successfully"
}

# Usage information
usage() {
    cat << 'EOF'
InfoTerminal Test Data Management Pipeline

Usage: ./test_data_pipeline.sh [COMMAND] [OPTIONS]

Commands:
  init              Initialize directories and create seed data
  seed              Seed all databases with test data
  seed-neo4j        Seed Neo4j database only
  seed-opensearch   Seed OpenSearch index only  
  seed-postgres     Seed PostgreSQL database only
  cleanup           Clean up all test data from databases
  validate          Validate test data integrity
  export [format]   Export test data (json, csv, sql)
  help              Show this help message

Examples:
  ./test_data_pipeline.sh init
  ./test_data_pipeline.sh seed
  ./test_data_pipeline.sh cleanup
  ./test_data_pipeline.sh export csv

Environment Variables:
  IT_NEO4J_URI      Neo4j connection URI
  IT_NEO4J_USER     Neo4j username
  IT_NEO4J_PASSWORD Neo4j password
  IT_OPENSEARCH_URL OpenSearch URL
  IT_POSTGRES_URL   PostgreSQL connection URL
EOF
}

# Main execution
main() {
    local command="${1:-help}"
    
    case "$command" in
        "init")
            init_directories
            create_seed_data
            create_test_fixtures
            validate_test_data
            ;;
        "seed")
            seed_all_databases
            ;;
        "seed-neo4j")
            seed_neo4j_database
            ;;
        "seed-opensearch")
            seed_opensearch_index
            ;;
        "seed-postgres")
            seed_postgres_database
            ;;
        "cleanup")
            cleanup_test_data
            ;;
        "validate")
            validate_test_data
            ;;
        "export")
            export_test_data "${2:-json}"
            ;;
        "help"|*)
            usage
            ;;
    esac
}

# Check dependencies
check_dependencies() {
    local missing_deps=()
    
    if ! command -v jq >/dev/null; then
        missing_deps+=("jq")
    fi
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies and try again"
        exit 1
    fi
}

# Initialize on script load
init_directories

# Run dependency check and main function
check_dependencies
main "$@"
