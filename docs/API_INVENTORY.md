# API Inventory

_Generated on 2025-09-21T10:57:18Z by `scripts/generate_parity_reports.py`_

## agent-connector
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /healthz | 200 | — |  | services/agent-connector/app.py:11 |
| POST | /plugins/invoke/{plugin}/{tool} | 200 | — |  | services/agent-connector/plugins/loader.py:64 |
| GET | /plugins/registry | 200 | — |  | services/agent-connector/plugins/api.py:28 |
| GET | /plugins/state | 200 | — |  | services/agent-connector/plugins/api.py:33 |
| GET | /plugins/tools | 200 | — |  | services/agent-connector/plugins/loader.py:54 |
| GET | /plugins/{name}/config | 200 | — |  | services/agent-connector/plugins/api.py:71 |
| POST | /plugins/{name}/config | 200 | — |  | services/agent-connector/plugins/api.py:80 |
| POST | /plugins/{name}/enable | 200 | — |  | services/agent-connector/plugins/api.py:53 |
| GET | /plugins/{name}/health | 200 | — |  | services/agent-connector/plugins/api.py:95 |
| GET | /readyz | 200 | — |  | services/agent-connector/app.py:16 |

## archive
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /healthz | 200 | — |  | services/archive/nlp-service.backup.20250916/app.py:12 |
| POST | /ner | 200 | — |  | services/archive/nlp-service.backup.20250916/app.py:16 |
| POST | /summarize | 200 | — |  | services/archive/nlp-service.backup.20250916/app.py:23 |

## auth-service
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | / | 200 | — | Service information and available endpoints. | services/auth-service/src/auth_service/app_v1.py:849 |
| GET | / | 200 | — | Root endpoint with service information. | services/auth-service/src/auth_service/app.py:216 |
| POST | /auth/change-password | 200 | SuccessResponse | Change user password. | services/auth-service/src/auth_service/api/auth.py:240 |
| POST | /auth/login | 200 | LoginResponse | Authenticate user and return access tokens. | services/auth-service/src/auth_service/api/auth.py:90 |
| POST | /auth/logout | 200 | SuccessResponse | Logout user by invalidating session. | services/auth-service/src/auth_service/api/auth.py:184 |
| GET | /auth/me | 200 | UserResponse | Get current user information. | services/auth-service/src/auth_service/api/auth.py:210 |
| POST | /auth/mfa/disable | 200 | SuccessResponse | Disable MFA after password verification. | services/auth-service/src/auth_service/api/auth.py:377 |
| POST | /auth/mfa/enable | 200 | SuccessResponse | Enable MFA after verifying setup token. | services/auth-service/src/auth_service/api/auth.py:346 |
| POST | /auth/mfa/setup | 200 | MFASetupResponse | Setup MFA for current user. | services/auth-service/src/auth_service/api/auth.py:310 |
| POST | /auth/refresh | 200 | RefreshTokenResponse | Refresh access token using refresh token. | services/auth-service/src/auth_service/api/auth.py:150 |
| POST | /auth/request-password-reset | 200 | SuccessResponse | Request password reset email. | services/auth-service/src/auth_service/api/auth.py:281 |
| GET | /health | 200 | HealthResponse | Health check endpoint. | services/auth-service/src/auth_service/app.py:177 |
| GET | /healthz | 200 | HealthChecker.health_check().__class__ | Health check endpoint (liveness probe). | services/auth-service/src/auth_service/app_v1.py:120 |
| POST | /login | 200 | — | DEPRECATED: Use /v1/auth/login instead. | services/auth-service/src/auth_service/app_v1.py:830 |
| GET | /metrics | 200 | — | Prometheus metrics endpoint. | services/auth-service/src/auth_service/app.py:206 |
| GET | /readyz | 200 | HealthChecker.ready_check().__class__ | Readiness check endpoint (readiness probe). | services/auth-service/src/auth_service/app_v1.py:125 |
| GET | /roles | 200 | List[RoleResponse] | Get list of all roles. | services/auth-service/src/auth_service/api/roles.py:40 |
| POST | /roles | 200 | RoleResponse | Create a new role (admin only). | services/auth-service/src/auth_service/api/roles.py:76 |
| GET | /roles/permissions/ | 200 | List[PermissionResponse] | Get list of all permissions. | services/auth-service/src/auth_service/api/roles.py:375 |
| GET | /roles/permissions/services | 200 | List[str] | Get list of all services with permissions. | services/auth-service/src/auth_service/api/roles.py:400 |
| GET | /roles/permissions/{permission_id} | 200 | PermissionResponse | Get permission by ID. | services/auth-service/src/auth_service/api/roles.py:418 |
| DELETE | /roles/{role_id} | 200 | SuccessResponse | Delete role (admin only). | services/auth-service/src/auth_service/api/roles.py:277 |
| GET | /roles/{role_id} | 200 | RoleResponse | Get role by ID. | services/auth-service/src/auth_service/api/roles.py:148 |
| PUT | /roles/{role_id} | 200 | RoleResponse | Update role information (admin only). | services/auth-service/src/auth_service/api/roles.py:182 |
| POST | /roles/{role_id}/permissions | 200 | SuccessResponse | Assign permissions to role (admin only). | services/auth-service/src/auth_service/api/roles.py:445 |
| DELETE | /roles/{role_id}/permissions/{permission_name} | 200 | SuccessResponse | Remove permission from role (admin only). | services/auth-service/src/auth_service/api/roles.py:512 |
| GET | /roles/{role_id}/users | 200 | List[Dict[str, Any]] | Get users assigned to a specific role (admin only). | services/auth-service/src/auth_service/api/roles.py:335 |
| GET | /users | 200 | UserListResponse | Get paginated list of users with filtering. | services/auth-service/src/auth_service/api/users.py:62 |
| POST | /users | 200 | UserResponse | Create a new user account. | services/auth-service/src/auth_service/api/users.py:128 |
| GET | /users/stats | 200 | UserStatsResponse | Get user statistics (admin only). | services/auth-service/src/auth_service/api/users.py:720 |
| DELETE | /users/{user_id} | 200 | SuccessResponse | Delete user account (admin only). | services/auth-service/src/auth_service/api/users.py:277 |
| GET | /users/{user_id} | 200 | UserResponse | Get user by ID. | services/auth-service/src/auth_service/api/users.py:181 |
| PUT | /users/{user_id} | 200 | UserResponse | Update user information. | services/auth-service/src/auth_service/api/users.py:222 |
| POST | /users/{user_id}/activate | 200 | SuccessResponse | Activate user account (admin only). | services/auth-service/src/auth_service/api/users.py:331 |
| GET | /users/{user_id}/api-keys | 200 | List[ApiKeyResponse] | Get user's API keys. | services/auth-service/src/auth_service/api/users.py:583 |
| POST | /users/{user_id}/api-keys | 200 | ApiKeyCreateResponse | Create API key for user. | services/auth-service/src/auth_service/api/users.py:613 |
| DELETE | /users/{user_id}/api-keys/{key_id} | 200 | SuccessResponse | Revoke API key. | services/auth-service/src/auth_service/api/users.py:678 |
| POST | /users/{user_id}/assign-roles | 200 | SuccessResponse | Assign roles to user (admin only). | services/auth-service/src/auth_service/api/users.py:438 |
| GET | /users/{user_id}/audit | 200 | AuditLogListResponse | Get user audit logs (admin only). | services/auth-service/src/auth_service/api/users.py:764 |
| POST | /users/{user_id}/deactivate | 200 | SuccessResponse | Deactivate user account (admin only). | services/auth-service/src/auth_service/api/users.py:378 |
| GET | /users/{user_id}/sessions | 200 | SessionListResponse | Get user's active sessions. | services/auth-service/src/auth_service/api/users.py:496 |
| DELETE | /users/{user_id}/sessions/{session_id} | 200 | SuccessResponse | Revoke a specific user session. | services/auth-service/src/auth_service/api/users.py:537 |
| POST | /v1/auth/change-password | 200 | — | Change password | services/auth-service/src/auth_service/app_v1.py:625 |
| POST | /v1/auth/login | 200 | LoginResponse | User login | services/auth-service/src/auth_service/app_v1.py:432 |
| POST | /v1/auth/logout | 200 | — | User logout | services/auth-service/src/auth_service/app_v1.py:527 |
| GET | /v1/auth/me | 200 | UserResponse | Get current user | services/auth-service/src/auth_service/app_v1.py:549 |
| POST | /v1/auth/register | 200 | UserResponse | Register new user | services/auth-service/src/auth_service/app_v1.py:364 |
| POST | /v1/auth/verify-token | 200 | TokenResponse | Verify token | services/auth-service/src/auth_service/app_v1.py:595 |
| GET | /v1/roles | 200 | List[RoleModel] | List roles | services/auth-service/src/auth_service/app_v1.py:793 |
| GET | /v1/users | 200 | PaginatedResponse[UserResponse] | List users | services/auth-service/src/auth_service/app_v1.py:671 |
| GET | /v1/users/{user_id} | 200 | UserResponse | Get user | services/auth-service/src/auth_service/app_v1.py:738 |

## cache-manager
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| POST | /cache | 200 | — | Manually set cache item | services/cache-manager/main.py:670 |
| POST | /cache/invalidate | 200 | — | Invalidate cache items by tags or pattern | services/cache-manager/main.py:714 |
| GET | /cache/stats | 200 | — | Get cache performance statistics | services/cache-manager/main.py:733 |
| POST | /cache/warm | 200 | — | Warm cache with specified patterns | services/cache-manager/main.py:727 |
| DELETE | /cache/{key} | 200 | — | Delete cache item | services/cache-manager/main.py:708 |
| GET | /cache/{key} | 200 | — | Get cache item by key | services/cache-manager/main.py:683 |
| GET | /health | 200 | — | Health check endpoint | services/cache-manager/main.py:739 |

## collab-hub
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| POST | /audit | 200 | — |  | services/collab-hub/app/main.py:150 |
| GET | /healthz | 200 | — |  | services/collab-hub/app/main.py:62 |
| GET | /labels | 200 | — |  | services/collab-hub/app/main.py:140 |
| GET | /tasks | 200 | — |  | services/collab-hub/app/main.py:73 |
| POST | /tasks | 200 | — |  | services/collab-hub/app/main.py:78 |
| DELETE | /tasks/{task_id} | 200 | — |  | services/collab-hub/app/main.py:106 |
| POST | /tasks/{task_id}/move | 200 | — |  | services/collab-hub/app/main.py:89 |
| POST | /tasks/{task_id}/update | 200 | — |  | services/collab-hub/app/main.py:124 |

## doc-entities
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | / | 200 | — |  | services/doc-entities/app_v1.py:166 |
| GET | /healthz | 200 | — |  | services/doc-entities/routers/core_v1.py:21 |
| GET | /info | 200 | — |  | services/doc-entities/routers/core_v1.py:29 |
| POST | /ner | 200 | — |  | services/doc-entities/app_v1.py:146 |
| GET | /readyz | 200 | — |  | services/doc-entities/routers/core_v1.py:25 |
| POST | /summary | 200 | — |  | services/doc-entities/app_v1.py:159 |

## egress-gateway
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /healthz | 200 | — | Health check endpoint. | services/egress-gateway/app.py:120 |
| POST | /proxy/request | 200 | ProxyResponse | Execute an anonymous HTTP request through proxy infrastructure. | services/egress-gateway/app.py:137 |
| POST | /proxy/rotate | 200 | — | Manually rotate proxy/identity. | services/egress-gateway/app.py:253 |
| GET | /proxy/status | 200 | ProxyStatus | Get current proxy infrastructure status. | services/egress-gateway/app.py:231 |

## entity-resolution
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| POST | /dedupe | 200 | — |  | services/entity-resolution/.archive/app.py:50 |
| GET | /healthz | 200 | — |  | services/entity-resolution/.archive/app.py:23 |
| POST | /match | 200 | — |  | services/entity-resolution/.archive/app.py:38 |

## federation-proxy
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /healthz | 200 | — |  | services/federation-proxy/app/main.py:19 |
| GET | /remotes | 200 | — |  | services/federation-proxy/app/main.py:24 |

## feedback-aggregator
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /feedback | 200 | — | Get paginated list of feedback entries | services/feedback-aggregator/main.py:635 |
| POST | /feedback | 200 | FeedbackResponse | Create new feedback entry | services/feedback-aggregator/main.py:613 |
| GET | /feedback/stats | 200 | FeedbackStats | Get aggregated feedback statistics | services/feedback-aggregator/main.py:630 |
| POST | /feedback/{feedback_id}/vote | 200 | — | Vote on feedback entry | services/feedback-aggregator/main.py:621 |
| GET | /health | 200 | — | Health check endpoint | services/feedback-aggregator/main.py:678 |

## flowise-connector
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| POST | /chat | 200 | — | Main chat endpoint for agent interactions. | services/flowise-connector/app/main.py:548 |
| DELETE | /conversations/{conversation_id} | 200 | — | Clear conversation history and context. | services/flowise-connector/app/main.py:574 |
| GET | /conversations/{conversation_id}/history | 200 | — | Get conversation execution history. | services/flowise-connector/app/main.py:561 |
| GET | /healthz | 200 | — |  | services/flowise-connector/app/main.py:515 |
| GET | /readyz | 200 | — |  | services/flowise-connector/app/main.py:519 |
| GET | /tools | 200 | — | List all available tools for agent workflows. | services/flowise-connector/app/main.py:523 |
| POST | /tools/execute | 200 | — | Execute a single tool directly. | services/flowise-connector/app/main.py:541 |
| GET | /workflows | 200 | — | List available agent workflow types. | services/flowise-connector/app/main.py:582 |

## forensics
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /chain/report | 200 | — | Return the full append-only ledger. | services/forensics/app/main.py:92 |
| GET | /healthz | 200 | — |  | services/forensics/app/main.py:43 |
| POST | /ingest | 200 | — |  | services/forensics/app/main.py:48 |
| GET | /receipt/{sha256} | 200 | — | Return a signed receipt for a given SHA256 if present in ledger. | services/forensics/app/main.py:77 |
| POST | /verify | 200 | — |  | services/forensics/app/main.py:62 |

## gateway
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /healthz | 200 | — |  | services/gateway/app/app.py:130 |
| GET | /metrics | 200 | — |  | services/gateway/app/app.py:140 |
| GET | /readyz | 200 | — |  | services/gateway/app/app.py:135 |

## graph-api
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | / | 200 | — | Service information and available endpoints. | services/graph-api/app/main_v1.py:935 |
| POST | /alg/betweenness | 200 | — | Compute betweenness centrality for nodes | services/graph-api/app/routes/alg.py:265 |
| GET | /alg/centrality-summary/{node_id} | 200 | — | Get a summary of all centrality measures for a specific node | services/graph-api/app/routes/alg.py:431 |
| POST | /alg/closeness | 200 | — | Compute closeness centrality for nodes | services/graph-api/app/routes/alg.py:286 |
| GET | /alg/community-stats | 200 | — | Get overall community statistics | services/graph-api/app/routes/alg.py:467 |
| POST | /alg/degree | 200 | — | Compute degree centrality for nodes | services/graph-api/app/routes/alg.py:219 |
| POST | /alg/label-propagation | 200 | — | Compute Label Propagation community detection | services/graph-api/app/routes/alg.py:373 |
| POST | /alg/louvain | 200 | — | Compute Louvain community detection | services/graph-api/app/routes/alg.py:349 |
| POST | /alg/pagerank | 200 | — | Compute PageRank centrality for nodes | services/graph-api/app/routes/alg.py:322 |
| POST | /alg/shortest | 200 | — | Find shortest path between two nodes | services/graph-api/app/routes/alg.py:397 |
| GET | /analytics/centrality/betweenness | 200 | — | Get betweenness centrality for nodes. | services/graph-api/app/routes/analytics.py:41 |
| GET | /analytics/centrality/degree | 200 | — | Get degree centrality for nodes. | services/graph-api/app/routes/analytics.py:18 |
| POST | /analytics/communities | 200 | — | Detect communities in the graph. | services/graph-api/app/routes/analytics.py:64 |
| GET | /analytics/embeddings/node2vec | 200 | — | Compute Node2Vec embeddings via Neo4j GDS (limited set). | services/graph-api/app/routes/analytics.py:98 |
| GET | /analytics/node/{node_id}/influence | 200 | — | Analyze a node's influence in its neighborhood. | services/graph-api/app/routes/analytics.py:174 |
| GET | /analytics/pagerank | 200 | — |  | services/graph-api/app/routes/analytics.py:118 |
| POST | /analytics/paths/shortest | 200 | — | Find shortest path between two nodes. | services/graph-api/app/routes/analytics.py:136 |
| GET | /analytics/summary | 200 | — | Get overall graph statistics. | services/graph-api/app/routes/analytics.py:84 |
| GET | /export/graphml | 200 | — |  | services/graph-api/app/routes/export.py:43 |
| GET | /export/json | 200 | — |  | services/graph-api/app/routes/export.py:35 |
| POST | /geo/batch-geocode | 200 | — | Start batch geocoding of nodes in the background. | services/graph-api/app/routes/geospatial.py:146 |
| GET | /geo/entities | 200 | — | Get entities within a bounding box. | services/graph-api/app/routes/geospatial.py:35 |
| POST | /geo/entities/nearby | 200 | — | Get entities near a specific point. | services/graph-api/app/routes/geospatial.py:68 |
| POST | /geo/geocode | 200 | — | Geocode a location string. | services/graph-api/app/routes/geospatial.py:97 |
| GET | /geo/heatmap | 200 | — | Generate heatmap data for entities in a bounding box. | services/graph-api/app/routes/geospatial.py:235 |
| POST | /geo/node/coordinates | 200 | — | Manually set coordinates for a node. | services/graph-api/app/routes/geospatial.py:202 |
| POST | /geo/node/geocode | 200 | — | Geocode a specific node and update it with coordinates. | services/graph-api/app/routes/geospatial.py:127 |
| GET | /geo/statistics | 200 | — | Get geospatial statistics. | services/graph-api/app/routes/geospatial.py:181 |
| GET | /healthz | 200 | — | Health check endpoint (legacy response schema). | services/graph-api/app/main_v1.py:137 |
| GET | /neighbors | 200 | — | DEPRECATED: Use /v1/nodes/{id}/neighbors instead. | services/graph-api/app/main_v1.py:895 |
| GET | /neo4j/ping | 200 | — | Legacy ping endpoint for Neo4j connectivity. | services/graph-api/app/main_v1.py:921 |
| POST | /query | 200 | — | DEPRECATED: Use /v1/cypher instead. | services/graph-api/app/main_v1.py:870 |
| GET | /readyz | 200 | — | Readiness check endpoint with legacy response schema. | services/graph-api/app/main_v1.py:143 |
| POST | /v1/algorithms/centrality | 200 | JobStatus | Run centrality algorithm | services/graph-api/app/main_v1.py:589 |
| POST | /v1/algorithms/communities | 200 | JobStatus | Run community detection | services/graph-api/app/main_v1.py:640 |
| POST | /v1/cypher | 200 | CypherResponse | Execute Cypher query | services/graph-api/app/main_v1.py:377 |
| DELETE | /v1/jobs/{job_id} | 200 | — | Cancel job | services/graph-api/app/main_v1.py:715 |
| GET | /v1/jobs/{job_id} | 200 | JobStatus | Get job status | services/graph-api/app/main_v1.py:691 |
| GET | /v1/nodes/{node_id}/neighbors | 200 | NeighborResponse | Get node neighbors | services/graph-api/app/main_v1.py:406 |
| POST | /v1/shortest-path | 200 | ShortestPathResponse | Find shortest path | services/graph-api/app/main_v1.py:492 |

## graph-views
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | / | 200 | — | Service information and available endpoints. | services/graph-views/app_v1.py:671 |
| POST | /dossier | 200 | — |  | services/graph-views/dossier/api.py:45 |
| GET | /geo/entities | 200 | — | Return a small set of sample entities as GeoJSON. | services/graph-views/geo.py:68 |
| GET | /geo/get | 200 | — |  | services/graph-views/geo.py:37 |
| GET | /geo/list | 200 | — |  | services/graph-views/geo.py:29 |
| GET | /geo/query | 200 | — |  | services/graph-views/geo.py:45 |
| POST | /geo/upload | 200 | — |  | services/graph-views/geo.py:13 |
| GET | /graphs/view/ego | 200 | — | DEPRECATED: Use /v1/views/ego instead. | services/graph-views/app_v1.py:599 |
| GET | /graphs/view/shortest-path | 200 | — | DEPRECATED: Use /v1/views/shortest-path instead. | services/graph-views/app_v1.py:631 |
| GET | /healthz | 200 | — |  | services/graph-views/routers/core_v1.py:21 |
| GET | /info | 200 | — |  | services/graph-views/routers/core_v1.py:29 |
| GET | /ontology/entities | 200 | — |  | services/graph-views/ontology/api.py:17 |
| GET | /ontology/relations | 200 | — |  | services/graph-views/ontology/api.py:21 |
| POST | /ontology/validate | 200 | — |  | services/graph-views/ontology/api.py:25 |
| GET | /readyz | 200 | — |  | services/graph-views/routers/core_v1.py:25 |

## media-forensics
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /formats | 200 | — | Get supported image formats and limits. | services/media-forensics/app.py:355 |
| GET | /healthz | 200 | — |  | services/media-forensics/app.py:88 |
| POST | /image/analyze | 200 | ImageAnalysisResult | Analyze an uploaded image for forensic information. | services/media-forensics/app.py:233 |
| POST | /image/compare | 200 | ComparisonResult | Compare two images for similarity. | services/media-forensics/app.py:288 |
| GET | /image/hash/{hash_value} | 200 | — | Find similar images by perceptual hash (placeholder for database integration). | services/media-forensics/app.py:343 |
| GET | /readyz | 200 | — |  | services/media-forensics/app.py:93 |

## opa-audit-sink
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| POST | /audit | 200 | — |  | services/opa-audit-sink/app/main.py:11 |
| GET | /healthz | 200 | — |  | services/opa-audit-sink/app.py:22 |
| GET | /healthz | 200 | — |  | services/opa-audit-sink/app/main.py:7 |
| POST | /logs | 200 | — |  | services/opa-audit-sink/app.py:45 |

## ops-controller
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /api/system/performance | 200 | — | Get detailed system performance metrics. | services/ops-controller/app.py:494 |
| GET | /api/verification/health | 200 | OrchestrationHealthResponse | Get health status of all orchestration components. | services/ops-controller/verification_api.py:280 |
| POST | /api/verification/session-complete | 200 | — | Endpoint called by n8n workflow when verification is complete. | services/ops-controller/verification_api.py:250 |
| DELETE | /api/verification/session/{session_id} | 200 | — | Cancel and cleanup a verification session. | services/ops-controller/verification_api.py:182 |
| GET | /api/verification/sessions | 200 | — | List all verification sessions with optional filtering. | services/ops-controller/verification_api.py:157 |
| POST | /api/verification/start | 200 | VerificationSessionResponse | Start a new verification session with full orchestration. | services/ops-controller/verification_api.py:56 |
| GET | /api/verification/status/{session_id} | 200 | VerificationStatusResponse | Get detailed status of a verification session. | services/ops-controller/verification_api.py:139 |
| POST | /api/verification/trigger-demo | 200 | — | Trigger a demonstration of the verification pipeline. | services/ops-controller/verification_api.py:295 |
| POST | /api/verification/webhook/{session_id} | 200 | — | Webhook endpoint for receiving updates from orchestration tools. | services/ops-controller/verification_api.py:207 |
| GET | /health/comprehensive | 200 | — | Comprehensive health check with performance metrics. | services/ops-controller/app.py:422 |
| GET | /ops/stacks | 200 | — |  | services/ops-controller/app.py:107 |
| POST | /ops/stacks/{name}/down | 200 | — |  | services/ops-controller/app.py:138 |
| GET | /ops/stacks/{name}/logs | 200 | — |  | services/ops-controller/app.py:182 |
| POST | /ops/stacks/{name}/restart | 200 | — |  | services/ops-controller/app.py:152 |
| POST | /ops/stacks/{name}/scale | 200 | — |  | services/ops-controller/app.py:166 |
| GET | /ops/stacks/{name}/status | 200 | — |  | services/ops-controller/app.py:112 |
| POST | /ops/stacks/{name}/up | 200 | — |  | services/ops-controller/app.py:124 |
| GET | /security/containers/status | 200 | — | Get container security status. | services/ops-controller/app.py:230 |
| POST | /security/containers/{container_id}/restart | 200 | — | Restart a specific container. | services/ops-controller/app.py:361 |
| POST | /security/containers/{container_id}/stop | 200 | — | Stop a specific container. | services/ops-controller/app.py:382 |
| POST | /security/data-wipe/{category_id} | 200 | — | Wipe a specific data category. | services/ops-controller/app.py:341 |
| POST | /security/emergency-shutdown | 200 | — | Emergency shutdown with secure data wiping. | services/ops-controller/app.py:402 |
| POST | /security/incognito/start | 200 | — | Start a new incognito session. | services/ops-controller/app.py:244 |
| GET | /security/incognito/status | 200 | — | Get current incognito mode status. | services/ops-controller/app.py:206 |
| GET | /security/incognito/{session_id}/containers | 200 | — | Get containers for a specific incognito session. | services/ops-controller/app.py:314 |
| GET | /security/incognito/{session_id}/data-scan | 200 | — | Scan data categories for a session. | services/ops-controller/app.py:328 |
| POST | /security/incognito/{session_id}/stop | 200 | — | Stop an incognito session. | services/ops-controller/app.py:269 |
| POST | /security/incognito/{session_id}/wipe | 200 | — | Wipe all data for an incognito session. | services/ops-controller/app.py:290 |

## performance-monitor
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /alerts | 200 | — | Get recent performance alerts | services/performance-monitor/main.py:555 |
| GET | /health | 200 | — | Health check endpoint | services/performance-monitor/main.py:567 |
| POST | /metrics | 200 | — | Record a custom performance metric | services/performance-monitor/main.py:532 |
| GET | /metrics/{service_name}/summary | 200 | ServiceSummaryResponse | Get performance summary for a service | services/performance-monitor/main.py:549 |
| GET | /metrics/{service_name}/{metric_type} | 200 | — | Get recent metrics for a service and metric type | services/performance-monitor/main.py:561 |

## plugin-runner
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | /categories | 200 | — | Get available plugin categories. | services/plugin-runner/app.py:376 |
| POST | /execute | 200 | — | Execute a plugin with given parameters. | services/plugin-runner/app.py:261 |
| GET | /healthz | 200 | — |  | services/plugin-runner/app.py:195 |
| GET | /jobs | 200 | — | List recent plugin execution jobs. | services/plugin-runner/app.py:329 |
| DELETE | /jobs/{job_id} | 200 | — | Cancel a queued or running job. | services/plugin-runner/app.py:352 |
| GET | /jobs/{job_id} | 200 | — | Get status and results of a plugin execution job. | services/plugin-runner/app.py:305 |
| GET | /plugins | 200 | — | List available plugins with optional category filter. | services/plugin-runner/app.py:222 |
| GET | /plugins/{plugin_name} | 200 | — | Get detailed information about a specific plugin. | services/plugin-runner/app.py:236 |
| GET | /readyz | 200 | — |  | services/plugin-runner/app.py:200 |
| GET | /statistics | 200 | — | Get plugin execution statistics. | services/plugin-runner/app.py:410 |

## rag-api
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| POST | /events/extract | 200 | — |  | services/rag-api/app/main.py:211 |
| POST | /feedback/label | 200 | — |  | services/rag-api/app/main.py:225 |
| POST | /graph/law/upsert | 200 | — | Upsert a Law node and optional relations in Neo4j (LEGAL-2). | services/rag-api/app/main.py:195 |
| GET | /healthz | 200 | — |  | services/rag-api/app/main.py:54 |
| POST | /index/knn/ef_search | 200 | — |  | services/rag-api/app/main.py:167 |
| GET | /law/context | 200 | ContextResponse | Return relevant laws for an entity. Tries graph links; falls back to text retrieval by entity name. | services/rag-api/app/main.py:174 |
| POST | /law/hybrid | 200 | RetrieveResponse |  | services/rag-api/app/main.py:132 |
| POST | /law/index | 200 | — | Index a law paragraph into OpenSearch (idempotent upsert). | services/rag-api/app/main.py:186 |
| GET | /law/knn | 200 | RetrieveResponse |  | services/rag-api/app/main.py:106 |
| POST | /law/knn_vector | 200 | RetrieveResponse |  | services/rag-api/app/main.py:118 |
| GET | /law/retrieve | 200 | RetrieveResponse | Retrieve relevant law paragraphs from OpenSearch index. | services/rag-api/app/main.py:92 |
| GET | /readyz | 200 | — |  | services/rag-api/app/main.py:59 |

## search-api
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | / | 200 | — | Service information and available endpoints. | services/search-api/src/search_api/app/main_v1.py:812 |
| GET | /healthz | 200 | — | Health check endpoint (legacy response schema). | services/search-api/src/search_api/app/main_v1.py:114 |
| POST | /query | 200 | — | DEPRECATED: Use /v1/search instead. | services/search-api/src/search_api/app/main_v1.py:779 |
| GET | /readyz | 200 | — | Readiness check endpoint with legacy response schema. | services/search-api/src/search_api/app/main_v1.py:120 |
| GET | /search | 200 | — | DEPRECATED: Use /v1/search instead. | services/search-api/src/search_api/app/main_v1.py:715 |
| POST | /search | 200 | — | DEPRECATED: Use /v1/search instead. | services/search-api/src/search_api/app/main_v1.py:716 |
| POST | /v1/audio/transcriptions | 200 | — |  | services/search-api/.venv/lib/python3.11/site-packages/transformers/commands/serving.py:677 |
| POST | /v1/chat/completions | 200 | — |  | services/search-api/.venv/lib/python3.11/site-packages/transformers/commands/serving.py:658 |
| DELETE | /v1/documents/{doc_id} | 200 | — | Delete document by ID | services/search-api/src/search_api/app/main_v1.py:601 |
| GET | /v1/documents/{doc_id} | 200 | DocumentResponse | Get document by ID | services/search-api/src/search_api/app/main_v1.py:538 |
| POST | /v1/index/documents | 200 | IndexResponse | Index documents | services/search-api/src/search_api/app/main_v1.py:449 |
| GET | /v1/models | 200 | — |  | services/search-api/.venv/lib/python3.11/site-packages/transformers/commands/serving.py:696 |
| OPTIONS | /v1/models | 200 | — |  | services/search-api/.venv/lib/python3.11/site-packages/transformers/commands/serving.py:695 |
| POST | /v1/responses | 200 | — |  | services/search-api/.venv/lib/python3.11/site-packages/transformers/commands/serving.py:668 |
| POST | /v1/search | 200 | PaginatedResponse[SearchResult] | Search documents | services/search-api/src/search_api/app/main_v1.py:261 |

## verification
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| GET | / | 200 | — |  | services/verification/app_v1.py:114 |
| GET | /healthz | 200 | — | Health check endpoint. | services/verification/app_legacy.py:238 |
| GET | /healthz | 200 | — |  | services/verification/routers/core_v1.py:20 |
| GET | /info | 200 | — |  | services/verification/routers/core_v1.py:28 |
| GET | /readyz | 200 | — |  | services/verification/routers/core_v1.py:24 |
| POST | /summary | 200 | — |  | services/verification/app_v1.py:108 |
| POST | /verify/extract-claims | 200 | — |  | services/verification/app_v1.py:103 |
| POST | /verify/extract-claims | 200 | List[ClaimResponse] | Extract verifiable claims from text. | services/verification/app_legacy.py:257 |
| POST | /verify/image | 200 | MediaAnalysisResponse | Analyze uploaded image for forensic indicators and metadata. | services/verification/app_legacy.py:310 |
| POST | /verify/image-similarity | 200 | — | Compare two images for similarity using perceptual hashing. | services/verification/app_legacy.py:382 |
| GET | /verify/stats | 200 | — | Get verification service statistics. | services/verification/app_legacy.py:461 |

## websocket-manager
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| POST | /broadcast | 200 | — | Broadcast message via REST API | services/websocket-manager/main.py:587 |
| POST | /broadcast/entity-discovered | 200 | — | Broadcast new entity discovery | services/websocket-manager/main.py:641 |
| POST | /broadcast/plugin-status | 200 | — | Broadcast plugin execution status | services/websocket-manager/main.py:604 |
| POST | /broadcast/system-alert | 200 | — | Broadcast system alert | services/websocket-manager/main.py:667 |
| GET | /health | 200 | — | Health check endpoint | services/websocket-manager/main.py:696 |
| GET | /stats | 200 | — | Get WebSocket manager statistics | services/websocket-manager/main.py:691 |

## xai
| Method | Path | Status Codes | Response Model | Summary | Source |
|---|---|---|---|---|---|
| POST | /explain/text | 200 | — |  | services/xai/app/main.py:21 |
| GET | /healthz | 200 | — |  | services/xai/app/main.py:16 |
| GET | /model-card | 200 | — |  | services/xai/app/main.py:47 |
