# API Inventory - Comprehensive Analysis

_Updated on 2025-09-21 by Claude for CLI/API Parity Project Phase 1_

## Executive Summary

**Total Services:** 24 microservices  
**Total Endpoints:** 280+ documented endpoints  
**API Maturity Distribution:**
- **Production Ready (/v1 + Standards):** 3 services (12.5%)
- **Partial Standards:** 8 services (33.3%)  
- **Legacy/Needs Migration:** 13 services (54.2%)

**Priority Issues:**
1. **Standards Gap:** 21/24 services lack complete /v1 namespace migration
2. **Error Handling:** Inconsistent error responses across services
3. **Documentation:** Missing OpenAPI schemas for 70% of endpoints
4. **Authentication:** Inconsistent auth implementation
5. **Health Checks:** Missing /readyz in 40% of services

## Service Classification by API Maturity

### 🟢 Production Ready (3 services)
Services with complete *_v1.py implementation and API standards:

#### auth-service
- **Status:** ✅ Complete v1 migration
- **Endpoints:** 51 total (21 v1 + 30 legacy)
- **Standards:** Error-Envelope, Pagination, Health/Ready, OpenAPI, JWT Auth
- **Coverage:** Users, Roles, Permissions, MFA, API Keys, Sessions
- **Port:** 8616 (Docker)

#### graph-api  
- **Status:** ✅ Complete v1 migration
- **Endpoints:** 40 total (6 v1 + 34 legacy)
- **Standards:** Error-Envelope, Pagination, Health/Ready, OpenAPI, Job API
- **Coverage:** Cypher, Analytics, Algorithms, Geospatial, Export
- **Port:** 8402 (Dev) / 8612 (Docker)

#### search-api
- **Status:** ✅ Partial v1 migration  
- **Endpoints:** 15 total (4 v1 + 11 legacy)
- **Standards:** Error-Envelope, Pagination, Health/Ready, OpenAPI
- **Coverage:** Document Search, Indexing, Retrieval
- **Port:** 8401 (Dev) / 8611 (Docker)

### 🟡 Partial Standards (8 services)
Services with some standardization but incomplete *_v1.py:

#### doc-entities
- **Endpoints:** 6 total
- **Has:** routers/core_v1.py with Health/Ready/Info
- **Missing:** Domain endpoints in *_v1.py format
- **Coverage:** NER, Summarization, Entity Resolution
- **Port:** 8613 (Docker)

#### verification
- **Endpoints:** 11 total  
- **Has:** routers/core_v1.py with Health/Ready/Info
- **Missing:** Domain endpoints in *_v1.py format
- **Coverage:** Claim extraction, Media analysis, Verification stats
- **Port:** TBD

#### graph-views
- **Endpoints:** 15 total
- **Has:** routers/core_v1.py with Health/Ready/Info  
- **Missing:** Domain endpoints in *_v1.py format
- **Coverage:** Ego views, Shortest path, Ontology, Geo
- **Port:** 8403 (Dev)

#### ops-controller
- **Endpoints:** 28 total
- **Has:** Basic health checks
- **Missing:** Complete standardization
- **Coverage:** Stack management, Security, Verification orchestration
- **Port:** TBD

#### cache-manager
- **Endpoints:** 7 total
- **Has:** Basic health checks
- **Missing:** Complete standardization  
- **Coverage:** Redis operations, Cache stats, Warming
- **Port:** TBD

#### websocket-manager
- **Endpoints:** 6 total
- **Has:** Basic health checks
- **Missing:** Complete standardization
- **Coverage:** Broadcasting, Real-time notifications
- **Port:** TBD

#### performance-monitor
- **Endpoints:** 5 total
- **Has:** Basic health checks
- **Missing:** Complete standardization
- **Coverage:** Metrics collection, Alerts, Performance stats
- **Port:** TBD

#### feedback-aggregator
- **Endpoints:** 5 total
- **Has:** Basic health checks
- **Missing:** Complete standardization
- **Coverage:** Feedback collection, Voting, Statistics
- **Port:** TBD

### 🔴 Legacy/Needs Migration (13 services)
Services requiring complete *_v1.py migration:

#### agent-connector (10 endpoints)
- **Missing:** All API standards
- **Coverage:** Plugin management, Agent tools, Registry
- **Priority:** HIGH (Agent functionality critical)

#### flowise-connector (8 endpoints) 
- **Missing:** All API standards
- **Coverage:** Flowise integration, Workflow management
- **Priority:** HIGH (Agent functionality critical)

#### rag-api (12 endpoints)
- **Missing:** All API standards
- **Coverage:** Retrieval, Legal context, Law indexing
- **Priority:** HIGH (RAG functionality critical)

#### media-forensics (6 endpoints)
- **Missing:** All API standards
- **Coverage:** Image analysis, Comparison, Forensic metadata
- **Priority:** HIGH (Verification critical)

#### forensics (5 endpoints)
- **Missing:** All API standards
- **Coverage:** Chain of custody, Receipt verification
- **Priority:** HIGH (Verification critical)

#### plugin-runner (10 endpoints)
- **Missing:** All API standards
- **Coverage:** Plugin execution, Job management
- **Priority:** MEDIUM

#### egress-gateway (4 endpoints)
- **Missing:** All API standards
- **Coverage:** Proxy requests, Anonymization
- **Priority:** MEDIUM (Security feature)

#### collab-hub (8 endpoints)
- **Missing:** All API standards
- **Coverage:** Task management, Collaboration
- **Priority:** MEDIUM

#### xai (3 endpoints)
- **Missing:** All API standards
- **Coverage:** Explainable AI, Model cards
- **Priority:** MEDIUM

#### archive (3 endpoints)
- **Missing:** All API standards
- **Coverage:** Legacy NLP backup service
- **Priority:** LOW (Deprecated)

#### entity-resolution (3 endpoints)
- **Missing:** All API standards
- **Coverage:** Fuzzy matching (archived)
- **Priority:** LOW (Consolidated into doc-entities)

#### federation-proxy (2 endpoints)
- **Missing:** All API standards
- **Coverage:** Remote federation
- **Priority:** LOW

#### opa-audit-sink (4 endpoints)
- **Missing:** All API standards
- **Coverage:** Policy audit logging
- **Priority:** LOW

## API Standards Implementation Matrix

| Service | /v1 Namespace | Error-Envelope | Health/Ready | OpenAPI | Auth | Pagination |
|---------|---------------|----------------|--------------|---------|------|------------|
| auth-service | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| graph-api | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ |
| search-api | 🟡 | ✅ | ✅ | ✅ | 🟡 | ✅ |
| doc-entities | 🟡 | ❌ | ✅ | 🟡 | ❌ | ❌ |
| verification | 🟡 | ❌ | ✅ | 🟡 | ❌ | ❌ |
| graph-views | 🟡 | ❌ | ✅ | 🟡 | ❌ | ❌ |
| ops-controller | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ |
| cache-manager | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ |
| websocket-manager | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ |
| ... | ... | ... | ... | ... | ... | ... |

**Legend:** ✅ Complete, 🟡 Partial, ❌ Missing

## Port Configuration Matrix

| Service | Dev Port | Docker Port | Type | Status |
|---------|----------|-------------|------|--------|
| frontend | 3411 | 3411 | UI | ✅ |
| search-api | 8401 | 8611 | Core | ✅ |
| graph-api | 8402 | 8612 | Core | ✅ |
| graph-views | 8403 | - | Core | ✅ |
| doc-entities | 8406 | 8613 | Core | ✅ |
| auth-service | - | 8616 | Core | ✅ |
| gateway | - | 8610 | Infrastructure | ✅ |
| prometheus | - | 3412 | Observability | ✅ |
| grafana | - | 3413 | Observability | ✅ |
| flowise | - | 3417 | Agent | ✅ |

**Missing Port Assignments:** 15+ services need port allocation

## Domain Coverage Analysis

### Search & Retrieval (85% Complete)
- **search-api:** Document search, indexing ✅
- **rag-api:** Legal retrieval, context ⚠️ (needs v1)

### Graph & Analytics (70% Complete)  
- **graph-api:** Neo4j, algorithms, geospatial ✅
- **graph-views:** Visualization, export ⚠️ (needs v1)

### Authentication & Authorization (95% Complete)
- **auth-service:** Users, roles, permissions, MFA ✅
- **gateway:** OIDC integration ⚠️ (needs v1)

### NLP & Document Processing (60% Complete)
- **doc-entities:** NER, summarization ⚠️ (needs v1)
- **entity-resolution:** Fuzzy matching (archived) ❌
- **xai:** Explanations ❌ (needs v1)

### Verification & Forensics (40% Complete)
- **verification:** Claim extraction ⚠️ (needs v1)
- **forensics:** Chain of custody ❌ (needs v1)  
- **media-forensics:** Image analysis ❌ (needs v1)

### Agent & Workflow (30% Complete)
- **flowise-connector:** Agent orchestration ❌ (needs v1)
- **agent-connector:** Plugin management ❌ (needs v1)
- **plugin-runner:** Execution engine ❌ (needs v1)

### Operations & Infrastructure (25% Complete)
- **ops-controller:** Stack management ⚠️ (needs v1)
- **cache-manager:** Redis operations ❌ (needs v1)
- **websocket-manager:** Real-time ❌ (needs v1)
- **performance-monitor:** Metrics ❌ (needs v1)

## Next Steps for Phase 2

### Immediate Priorities (High Impact)
1. **Agent Services:** flowise-connector, agent-connector, plugin-runner
2. **Verification:** forensics, media-forensics  
3. **NLP:** Complete doc-entities v1 migration
4. **Search:** Complete search-api v1 migration

### Standards Implementation
1. Extend _shared/api_standards with Job API, Stream API patterns
2. Create service migration templates  
3. Implement port assignment automation
4. Add comprehensive OpenAPI documentation

### Quality Assurance
1. API contract testing for all v1 endpoints
2. Health check standardization verification
3. Error envelope compliance testing
4. Performance benchmarking

**Total Estimated Effort:** 4-6 weeks for complete API standardization across all 24 services.
