# API ↔ CLI Parity Gap Report

_Generated on 2025-09-21T10:57:18Z by `scripts/generate_parity_reports.py`_

This report highlights API endpoints without a matching CLI command (and vice versa).

## agent-connector
- Total endpoints: 10
- CLI-covered endpoints: 0
- Missing CLI coverage: 10
- Endpoints without CLI coverage:
  - `GET` /healthz (services/agent-connector/app.py:11)
  - `POST` /plugins/invoke/{plugin}/{tool} (services/agent-connector/plugins/loader.py:64)
  - `GET` /plugins/registry (services/agent-connector/plugins/api.py:28)
  - `GET` /plugins/state (services/agent-connector/plugins/api.py:33)
  - `GET` /plugins/tools (services/agent-connector/plugins/loader.py:54)
  - `GET` /plugins/{name}/config (services/agent-connector/plugins/api.py:71)
  - `POST` /plugins/{name}/config (services/agent-connector/plugins/api.py:80)
  - `POST` /plugins/{name}/enable (services/agent-connector/plugins/api.py:53)
  - `GET` /plugins/{name}/health (services/agent-connector/plugins/api.py:95)
  - `GET` /readyz (services/agent-connector/app.py:16)

## archive
- Total endpoints: 3
- CLI-covered endpoints: 0
- Missing CLI coverage: 3
- Endpoints without CLI coverage:
  - `GET` /healthz (services/archive/nlp-service.backup.20250916/app.py:12)
  - `POST` /ner (services/archive/nlp-service.backup.20250916/app.py:16)
  - `POST` /summarize (services/archive/nlp-service.backup.20250916/app.py:23)

## auth-service
- Total endpoints: 51
- CLI-covered endpoints: 0
- Missing CLI coverage: 51
- Endpoints without CLI coverage:
  - `GET` / (services/auth-service/src/auth_service/app_v1.py:849)
  - `GET` / (services/auth-service/src/auth_service/app.py:216)
  - `POST` /auth/change-password (services/auth-service/src/auth_service/api/auth.py:240)
  - `POST` /auth/login (services/auth-service/src/auth_service/api/auth.py:90)
  - `POST` /auth/logout (services/auth-service/src/auth_service/api/auth.py:184)
  - `GET` /auth/me (services/auth-service/src/auth_service/api/auth.py:210)
  - `POST` /auth/mfa/disable (services/auth-service/src/auth_service/api/auth.py:377)
  - `POST` /auth/mfa/enable (services/auth-service/src/auth_service/api/auth.py:346)
  - `POST` /auth/mfa/setup (services/auth-service/src/auth_service/api/auth.py:310)
  - `POST` /auth/refresh (services/auth-service/src/auth_service/api/auth.py:150)
  - `POST` /auth/request-password-reset (services/auth-service/src/auth_service/api/auth.py:281)
  - `GET` /health (services/auth-service/src/auth_service/app.py:177)
  - `GET` /healthz (services/auth-service/src/auth_service/app_v1.py:120)
  - `POST` /login (services/auth-service/src/auth_service/app_v1.py:830)
  - `GET` /metrics (services/auth-service/src/auth_service/app.py:206)
  - `GET` /readyz (services/auth-service/src/auth_service/app_v1.py:125)
  - `GET` /roles (services/auth-service/src/auth_service/api/roles.py:40)
  - `POST` /roles (services/auth-service/src/auth_service/api/roles.py:76)
  - `GET` /roles/permissions/ (services/auth-service/src/auth_service/api/roles.py:375)
  - `GET` /roles/permissions/services (services/auth-service/src/auth_service/api/roles.py:400)
  - `GET` /roles/permissions/{permission_id} (services/auth-service/src/auth_service/api/roles.py:418)
  - `DELETE` /roles/{role_id} (services/auth-service/src/auth_service/api/roles.py:277)
  - `GET` /roles/{role_id} (services/auth-service/src/auth_service/api/roles.py:148)
  - `PUT` /roles/{role_id} (services/auth-service/src/auth_service/api/roles.py:182)
  - `POST` /roles/{role_id}/permissions (services/auth-service/src/auth_service/api/roles.py:445)
  - `DELETE` /roles/{role_id}/permissions/{permission_name} (services/auth-service/src/auth_service/api/roles.py:512)
  - `GET` /roles/{role_id}/users (services/auth-service/src/auth_service/api/roles.py:335)
  - `GET` /users (services/auth-service/src/auth_service/api/users.py:62)
  - `POST` /users (services/auth-service/src/auth_service/api/users.py:128)
  - `GET` /users/stats (services/auth-service/src/auth_service/api/users.py:720)
  - `DELETE` /users/{user_id} (services/auth-service/src/auth_service/api/users.py:277)
  - `GET` /users/{user_id} (services/auth-service/src/auth_service/api/users.py:181)
  - `PUT` /users/{user_id} (services/auth-service/src/auth_service/api/users.py:222)
  - `POST` /users/{user_id}/activate (services/auth-service/src/auth_service/api/users.py:331)
  - `GET` /users/{user_id}/api-keys (services/auth-service/src/auth_service/api/users.py:583)
  - `POST` /users/{user_id}/api-keys (services/auth-service/src/auth_service/api/users.py:613)
  - `DELETE` /users/{user_id}/api-keys/{key_id} (services/auth-service/src/auth_service/api/users.py:678)
  - `POST` /users/{user_id}/assign-roles (services/auth-service/src/auth_service/api/users.py:438)
  - `GET` /users/{user_id}/audit (services/auth-service/src/auth_service/api/users.py:764)
  - `POST` /users/{user_id}/deactivate (services/auth-service/src/auth_service/api/users.py:378)
  - `GET` /users/{user_id}/sessions (services/auth-service/src/auth_service/api/users.py:496)
  - `DELETE` /users/{user_id}/sessions/{session_id} (services/auth-service/src/auth_service/api/users.py:537)
  - `POST` /v1/auth/change-password (services/auth-service/src/auth_service/app_v1.py:625)
  - `POST` /v1/auth/login (services/auth-service/src/auth_service/app_v1.py:432)
  - `POST` /v1/auth/logout (services/auth-service/src/auth_service/app_v1.py:527)
  - `GET` /v1/auth/me (services/auth-service/src/auth_service/app_v1.py:549)
  - `POST` /v1/auth/register (services/auth-service/src/auth_service/app_v1.py:364)
  - `POST` /v1/auth/verify-token (services/auth-service/src/auth_service/app_v1.py:595)
  - `GET` /v1/roles (services/auth-service/src/auth_service/app_v1.py:793)
  - `GET` /v1/users (services/auth-service/src/auth_service/app_v1.py:671)
  - `GET` /v1/users/{user_id} (services/auth-service/src/auth_service/app_v1.py:738)

## cache-manager
- Total endpoints: 7
- CLI-covered endpoints: 0
- Missing CLI coverage: 7
- Endpoints without CLI coverage:
  - `POST` /cache (services/cache-manager/main.py:670)
  - `POST` /cache/invalidate (services/cache-manager/main.py:714)
  - `GET` /cache/stats (services/cache-manager/main.py:733)
  - `POST` /cache/warm (services/cache-manager/main.py:727)
  - `DELETE` /cache/{key} (services/cache-manager/main.py:708)
  - `GET` /cache/{key} (services/cache-manager/main.py:683)
  - `GET` /health (services/cache-manager/main.py:739)

## collab-hub
- Total endpoints: 8
- CLI-covered endpoints: 0
- Missing CLI coverage: 8
- Endpoints without CLI coverage:
  - `POST` /audit (services/collab-hub/app/main.py:150)
  - `GET` /healthz (services/collab-hub/app/main.py:62)
  - `GET` /labels (services/collab-hub/app/main.py:140)
  - `GET` /tasks (services/collab-hub/app/main.py:73)
  - `POST` /tasks (services/collab-hub/app/main.py:78)
  - `DELETE` /tasks/{task_id} (services/collab-hub/app/main.py:106)
  - `POST` /tasks/{task_id}/move (services/collab-hub/app/main.py:89)
  - `POST` /tasks/{task_id}/update (services/collab-hub/app/main.py:124)

## doc-entities
- Total endpoints: 6
- CLI-covered endpoints: 0
- Missing CLI coverage: 6
- Endpoints without CLI coverage:
  - `GET` / (services/doc-entities/app_v1.py:166)
  - `GET` /healthz (services/doc-entities/routers/core_v1.py:21)
  - `GET` /info (services/doc-entities/routers/core_v1.py:29)
  - `POST` /ner (services/doc-entities/app_v1.py:146)
  - `GET` /readyz (services/doc-entities/routers/core_v1.py:25)
  - `POST` /summary (services/doc-entities/app_v1.py:159)

## egress-gateway
- Total endpoints: 4
- CLI-covered endpoints: 0
- Missing CLI coverage: 4
- Endpoints without CLI coverage:
  - `GET` /healthz (services/egress-gateway/app.py:120)
  - `POST` /proxy/request (services/egress-gateway/app.py:137)
  - `POST` /proxy/rotate (services/egress-gateway/app.py:253)
  - `GET` /proxy/status (services/egress-gateway/app.py:231)

## entity-resolution
- Total endpoints: 3
- CLI-covered endpoints: 0
- Missing CLI coverage: 3
- Endpoints without CLI coverage:
  - `POST` /dedupe (services/entity-resolution/.archive/app.py:50)
  - `GET` /healthz (services/entity-resolution/.archive/app.py:23)
  - `POST` /match (services/entity-resolution/.archive/app.py:38)

## federation-proxy
- Total endpoints: 2
- CLI-covered endpoints: 0
- Missing CLI coverage: 2
- Endpoints without CLI coverage:
  - `GET` /healthz (services/federation-proxy/app/main.py:19)
  - `GET` /remotes (services/federation-proxy/app/main.py:24)

## feedback-aggregator
- Total endpoints: 5
- CLI-covered endpoints: 0
- Missing CLI coverage: 5
- Endpoints without CLI coverage:
  - `GET` /feedback (services/feedback-aggregator/main.py:635)
  - `POST` /feedback (services/feedback-aggregator/main.py:613)
  - `GET` /feedback/stats (services/feedback-aggregator/main.py:630)
  - `POST` /feedback/{feedback_id}/vote (services/feedback-aggregator/main.py:621)
  - `GET` /health (services/feedback-aggregator/main.py:678)

## flowise-connector
- Total endpoints: 8
- CLI-covered endpoints: 0
- Missing CLI coverage: 8
- Endpoints without CLI coverage:
  - `POST` /chat (services/flowise-connector/app/main.py:548)
  - `DELETE` /conversations/{conversation_id} (services/flowise-connector/app/main.py:574)
  - `GET` /conversations/{conversation_id}/history (services/flowise-connector/app/main.py:561)
  - `GET` /healthz (services/flowise-connector/app/main.py:515)
  - `GET` /readyz (services/flowise-connector/app/main.py:519)
  - `GET` /tools (services/flowise-connector/app/main.py:523)
  - `POST` /tools/execute (services/flowise-connector/app/main.py:541)
  - `GET` /workflows (services/flowise-connector/app/main.py:582)

## forensics
- Total endpoints: 5
- CLI-covered endpoints: 0
- Missing CLI coverage: 5
- Endpoints without CLI coverage:
  - `GET` /chain/report (services/forensics/app/main.py:92)
  - `GET` /healthz (services/forensics/app/main.py:43)
  - `POST` /ingest (services/forensics/app/main.py:48)
  - `GET` /receipt/{sha256} (services/forensics/app/main.py:77)
  - `POST` /verify (services/forensics/app/main.py:62)

## gateway
- Total endpoints: 3
- CLI-covered endpoints: 0
- Missing CLI coverage: 3
- Endpoints without CLI coverage:
  - `GET` /healthz (services/gateway/app/app.py:130)
  - `GET` /metrics (services/gateway/app/app.py:140)
  - `GET` /readyz (services/gateway/app/app.py:135)

## graph-api
- Total endpoints: 40
- CLI-covered endpoints: 4
- Missing CLI coverage: 36
- Endpoints without CLI coverage:
  - `GET` / (services/graph-api/app/main_v1.py:935)
  - `POST` /alg/betweenness (services/graph-api/app/routes/alg.py:265)
  - `GET` /alg/centrality-summary/{node_id} (services/graph-api/app/routes/alg.py:431)
  - `POST` /alg/closeness (services/graph-api/app/routes/alg.py:286)
  - `GET` /alg/community-stats (services/graph-api/app/routes/alg.py:467)
  - `POST` /alg/degree (services/graph-api/app/routes/alg.py:219)
  - `POST` /alg/label-propagation (services/graph-api/app/routes/alg.py:373)
  - `POST` /alg/louvain (services/graph-api/app/routes/alg.py:349)
  - `POST` /alg/pagerank (services/graph-api/app/routes/alg.py:322)
  - `POST` /alg/shortest (services/graph-api/app/routes/alg.py:397)
  - `GET` /analytics/centrality/betweenness (services/graph-api/app/routes/analytics.py:41)
  - `GET` /analytics/centrality/degree (services/graph-api/app/routes/analytics.py:18)
  - `POST` /analytics/communities (services/graph-api/app/routes/analytics.py:64)
  - `GET` /analytics/embeddings/node2vec (services/graph-api/app/routes/analytics.py:98)
  - `GET` /analytics/node/{node_id}/influence (services/graph-api/app/routes/analytics.py:174)
  - `GET` /analytics/pagerank (services/graph-api/app/routes/analytics.py:118)
  - `POST` /analytics/paths/shortest (services/graph-api/app/routes/analytics.py:136)
  - `GET` /analytics/summary (services/graph-api/app/routes/analytics.py:84)
  - `GET` /export/graphml (services/graph-api/app/routes/export.py:43)
  - `GET` /export/json (services/graph-api/app/routes/export.py:35)
  - `POST` /geo/batch-geocode (services/graph-api/app/routes/geospatial.py:146)
  - `GET` /geo/entities (services/graph-api/app/routes/geospatial.py:35)
  - `POST` /geo/entities/nearby (services/graph-api/app/routes/geospatial.py:68)
  - `POST` /geo/geocode (services/graph-api/app/routes/geospatial.py:97)
  - `GET` /geo/heatmap (services/graph-api/app/routes/geospatial.py:235)
  - `POST` /geo/node/coordinates (services/graph-api/app/routes/geospatial.py:202)
  - `POST` /geo/node/geocode (services/graph-api/app/routes/geospatial.py:127)
  - `GET` /geo/statistics (services/graph-api/app/routes/geospatial.py:181)
  - `GET` /neo4j/ping (services/graph-api/app/main_v1.py:921)
  - `POST` /query (services/graph-api/app/main_v1.py:870)
  - `GET` /readyz (services/graph-api/app/main_v1.py:143)
  - `POST` /v1/algorithms/centrality (services/graph-api/app/main_v1.py:589)
  - `POST` /v1/algorithms/communities (services/graph-api/app/main_v1.py:640)
  - `DELETE` /v1/jobs/{job_id} (services/graph-api/app/main_v1.py:715)
  - `GET` /v1/jobs/{job_id} (services/graph-api/app/main_v1.py:691)
  - `GET` /v1/nodes/{node_id}/neighbors (services/graph-api/app/main_v1.py:406)

## graph-views
- Total endpoints: 15
- CLI-covered endpoints: 0
- Missing CLI coverage: 15
- Endpoints without CLI coverage:
  - `GET` / (services/graph-views/app_v1.py:671)
  - `POST` /dossier (services/graph-views/dossier/api.py:45)
  - `GET` /geo/entities (services/graph-views/geo.py:68)
  - `GET` /geo/get (services/graph-views/geo.py:37)
  - `GET` /geo/list (services/graph-views/geo.py:29)
  - `GET` /geo/query (services/graph-views/geo.py:45)
  - `POST` /geo/upload (services/graph-views/geo.py:13)
  - `GET` /graphs/view/ego (services/graph-views/app_v1.py:599)
  - `GET` /graphs/view/shortest-path (services/graph-views/app_v1.py:631)
  - `GET` /healthz (services/graph-views/routers/core_v1.py:21)
  - `GET` /info (services/graph-views/routers/core_v1.py:29)
  - `GET` /ontology/entities (services/graph-views/ontology/api.py:17)
  - `GET` /ontology/relations (services/graph-views/ontology/api.py:21)
  - `POST` /ontology/validate (services/graph-views/ontology/api.py:25)
  - `GET` /readyz (services/graph-views/routers/core_v1.py:25)

## media-forensics
- Total endpoints: 6
- CLI-covered endpoints: 0
- Missing CLI coverage: 6
- Endpoints without CLI coverage:
  - `GET` /formats (services/media-forensics/app.py:355)
  - `GET` /healthz (services/media-forensics/app.py:88)
  - `POST` /image/analyze (services/media-forensics/app.py:233)
  - `POST` /image/compare (services/media-forensics/app.py:288)
  - `GET` /image/hash/{hash_value} (services/media-forensics/app.py:343)
  - `GET` /readyz (services/media-forensics/app.py:93)

## opa-audit-sink
- Total endpoints: 4
- CLI-covered endpoints: 0
- Missing CLI coverage: 4
- Endpoints without CLI coverage:
  - `POST` /audit (services/opa-audit-sink/app/main.py:11)
  - `GET` /healthz (services/opa-audit-sink/app.py:22)
  - `GET` /healthz (services/opa-audit-sink/app/main.py:7)
  - `POST` /logs (services/opa-audit-sink/app.py:45)

## ops-controller
- Total endpoints: 28
- CLI-covered endpoints: 0
- Missing CLI coverage: 28
- Endpoints without CLI coverage:
  - `GET` /api/system/performance (services/ops-controller/app.py:494)
  - `GET` /api/verification/health (services/ops-controller/verification_api.py:280)
  - `POST` /api/verification/session-complete (services/ops-controller/verification_api.py:250)
  - `DELETE` /api/verification/session/{session_id} (services/ops-controller/verification_api.py:182)
  - `GET` /api/verification/sessions (services/ops-controller/verification_api.py:157)
  - `POST` /api/verification/start (services/ops-controller/verification_api.py:56)
  - `GET` /api/verification/status/{session_id} (services/ops-controller/verification_api.py:139)
  - `POST` /api/verification/trigger-demo (services/ops-controller/verification_api.py:295)
  - `POST` /api/verification/webhook/{session_id} (services/ops-controller/verification_api.py:207)
  - `GET` /health/comprehensive (services/ops-controller/app.py:422)
  - `GET` /ops/stacks (services/ops-controller/app.py:107)
  - `POST` /ops/stacks/{name}/down (services/ops-controller/app.py:138)
  - `GET` /ops/stacks/{name}/logs (services/ops-controller/app.py:182)
  - `POST` /ops/stacks/{name}/restart (services/ops-controller/app.py:152)
  - `POST` /ops/stacks/{name}/scale (services/ops-controller/app.py:166)
  - `GET` /ops/stacks/{name}/status (services/ops-controller/app.py:112)
  - `POST` /ops/stacks/{name}/up (services/ops-controller/app.py:124)
  - `GET` /security/containers/status (services/ops-controller/app.py:230)
  - `POST` /security/containers/{container_id}/restart (services/ops-controller/app.py:361)
  - `POST` /security/containers/{container_id}/stop (services/ops-controller/app.py:382)
  - `POST` /security/data-wipe/{category_id} (services/ops-controller/app.py:341)
  - `POST` /security/emergency-shutdown (services/ops-controller/app.py:402)
  - `POST` /security/incognito/start (services/ops-controller/app.py:244)
  - `GET` /security/incognito/status (services/ops-controller/app.py:206)
  - `GET` /security/incognito/{session_id}/containers (services/ops-controller/app.py:314)
  - `GET` /security/incognito/{session_id}/data-scan (services/ops-controller/app.py:328)
  - `POST` /security/incognito/{session_id}/stop (services/ops-controller/app.py:269)
  - `POST` /security/incognito/{session_id}/wipe (services/ops-controller/app.py:290)

## performance-monitor
- Total endpoints: 5
- CLI-covered endpoints: 0
- Missing CLI coverage: 5
- Endpoints without CLI coverage:
  - `GET` /alerts (services/performance-monitor/main.py:555)
  - `GET` /health (services/performance-monitor/main.py:567)
  - `POST` /metrics (services/performance-monitor/main.py:532)
  - `GET` /metrics/{service_name}/summary (services/performance-monitor/main.py:549)
  - `GET` /metrics/{service_name}/{metric_type} (services/performance-monitor/main.py:561)

## plugin-runner
- Total endpoints: 10
- CLI-covered endpoints: 0
- Missing CLI coverage: 10
- Endpoints without CLI coverage:
  - `GET` /categories (services/plugin-runner/app.py:376)
  - `POST` /execute (services/plugin-runner/app.py:261)
  - `GET` /healthz (services/plugin-runner/app.py:195)
  - `GET` /jobs (services/plugin-runner/app.py:329)
  - `DELETE` /jobs/{job_id} (services/plugin-runner/app.py:352)
  - `GET` /jobs/{job_id} (services/plugin-runner/app.py:305)
  - `GET` /plugins (services/plugin-runner/app.py:222)
  - `GET` /plugins/{plugin_name} (services/plugin-runner/app.py:236)
  - `GET` /readyz (services/plugin-runner/app.py:200)
  - `GET` /statistics (services/plugin-runner/app.py:410)

## rag-api
- Total endpoints: 12
- CLI-covered endpoints: 0
- Missing CLI coverage: 12
- Endpoints without CLI coverage:
  - `POST` /events/extract (services/rag-api/app/main.py:211)
  - `POST` /feedback/label (services/rag-api/app/main.py:225)
  - `POST` /graph/law/upsert (services/rag-api/app/main.py:195)
  - `GET` /healthz (services/rag-api/app/main.py:54)
  - `POST` /index/knn/ef_search (services/rag-api/app/main.py:167)
  - `GET` /law/context (services/rag-api/app/main.py:174)
  - `POST` /law/hybrid (services/rag-api/app/main.py:132)
  - `POST` /law/index (services/rag-api/app/main.py:186)
  - `GET` /law/knn (services/rag-api/app/main.py:106)
  - `POST` /law/knn_vector (services/rag-api/app/main.py:118)
  - `GET` /law/retrieve (services/rag-api/app/main.py:92)
  - `GET` /readyz (services/rag-api/app/main.py:59)

## search-api
- Total endpoints: 15
- CLI-covered endpoints: 2
- Missing CLI coverage: 13
- Endpoints without CLI coverage:
  - `GET` / (services/search-api/src/search_api/app/main_v1.py:812)
  - `GET` /healthz (services/search-api/src/search_api/app/main_v1.py:114)
  - `POST` /query (services/search-api/src/search_api/app/main_v1.py:779)
  - `GET` /readyz (services/search-api/src/search_api/app/main_v1.py:120)
  - `POST` /v1/audio/transcriptions (services/search-api/.venv/lib/python3.11/site-packages/transformers/commands/serving.py:677)
  - `POST` /v1/chat/completions (services/search-api/.venv/lib/python3.11/site-packages/transformers/commands/serving.py:658)
  - `DELETE` /v1/documents/{doc_id} (services/search-api/src/search_api/app/main_v1.py:601)
  - `GET` /v1/documents/{doc_id} (services/search-api/src/search_api/app/main_v1.py:538)
  - `POST` /v1/index/documents (services/search-api/src/search_api/app/main_v1.py:449)
  - `GET` /v1/models (services/search-api/.venv/lib/python3.11/site-packages/transformers/commands/serving.py:696)
  - `OPTIONS` /v1/models (services/search-api/.venv/lib/python3.11/site-packages/transformers/commands/serving.py:695)
  - `POST` /v1/responses (services/search-api/.venv/lib/python3.11/site-packages/transformers/commands/serving.py:668)
  - `POST` /v1/search (services/search-api/src/search_api/app/main_v1.py:261)

## verification
- Total endpoints: 11
- CLI-covered endpoints: 0
- Missing CLI coverage: 11
- Endpoints without CLI coverage:
  - `GET` / (services/verification/app_v1.py:114)
  - `GET` /healthz (services/verification/app_legacy.py:238)
  - `GET` /healthz (services/verification/routers/core_v1.py:20)
  - `GET` /info (services/verification/routers/core_v1.py:28)
  - `GET` /readyz (services/verification/routers/core_v1.py:24)
  - `POST` /summary (services/verification/app_v1.py:108)
  - `POST` /verify/extract-claims (services/verification/app_v1.py:103)
  - `POST` /verify/extract-claims (services/verification/app_legacy.py:257)
  - `POST` /verify/image (services/verification/app_legacy.py:310)
  - `POST` /verify/image-similarity (services/verification/app_legacy.py:382)
  - `GET` /verify/stats (services/verification/app_legacy.py:461)

## websocket-manager
- Total endpoints: 6
- CLI-covered endpoints: 0
- Missing CLI coverage: 6
- Endpoints without CLI coverage:
  - `POST` /broadcast (services/websocket-manager/main.py:587)
  - `POST` /broadcast/entity-discovered (services/websocket-manager/main.py:641)
  - `POST` /broadcast/plugin-status (services/websocket-manager/main.py:604)
  - `POST` /broadcast/system-alert (services/websocket-manager/main.py:667)
  - `GET` /health (services/websocket-manager/main.py:696)
  - `GET` /stats (services/websocket-manager/main.py:691)

## xai
- Total endpoints: 3
- CLI-covered endpoints: 0
- Missing CLI coverage: 3
- Endpoints without CLI coverage:
  - `POST` /explain/text (services/xai/app/main.py:21)
  - `GET` /healthz (services/xai/app/main.py:16)
  - `GET` /model-card (services/xai/app/main.py:47)

## model-dump-json
- CLI commands reference this service, but no API endpoints were discovered.

## views-api
- CLI commands reference this service, but no API endpoints were discovered.
