{{/*
Expand the name of the chart.
*/}}
{{- define "infoterminal.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "infoterminal.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "infoterminal.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "infoterminal.labels" -}}
helm.sh/chart: {{ include "infoterminal.chart" . }}
{{ include "infoterminal.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "infoterminal.selectorLabels" -}}
app.kubernetes.io/name: {{ include "infoterminal.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "infoterminal.serviceAccountName" -}}
{{- if .Values.security.serviceAccount.create }}
{{- default (include "infoterminal.fullname" .) .Values.security.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.security.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create a default fully qualified PostgreSQL name.
*/}}
{{- define "infoterminal.postgresql.fullname" -}}
{{- include "postgresql.primary.fullname" .Subcharts.postgresql }}
{{- end }}

{{/*
Create a default fully qualified Redis name.
*/}}
{{- define "infoterminal.redis.fullname" -}}
{{- include "redis.fullname" .Subcharts.redis }}
{{- end }}

{{/*
Create a default fully qualified Neo4j name.
*/}}
{{- define "infoterminal.neo4j.fullname" -}}
{{- if .Values.neo4j.enabled }}
{{- printf "%s-neo4j" (include "infoterminal.fullname" .) }}
{{- else }}
{{- printf "%s-neo4j" .Release.Name }}
{{- end }}
{{- end }}

{{/*
Create a default fully qualified OpenSearch name.
*/}}
{{- define "infoterminal.opensearch.fullname" -}}
{{- if .Values.opensearch.enabled }}
{{- printf "%s-opensearch-master" (include "infoterminal.fullname" .) }}
{{- else }}
{{- printf "%s-opensearch" .Release.Name }}
{{- end }}
{{- end }}

{{/*
Create PostgreSQL connection string
*/}}
{{- define "infoterminal.postgresql.connectionString" -}}
{{- if .Values.postgresql.enabled }}
{{- printf "postgresql://%s:%s@%s:5432/%s" .Values.postgresql.auth.username .Values.postgresql.auth.password (include "infoterminal.postgresql.fullname" .) .Values.postgresql.auth.database }}
{{- else }}
{{- printf "postgresql://%s:%s@%s:5432/%s" .Values.externalDatabase.user .Values.externalDatabase.password .Values.externalDatabase.host .Values.externalDatabase.database }}
{{- end }}
{{- end }}

{{/*
Create Redis connection string
*/}}
{{- define "infoterminal.redis.connectionString" -}}
{{- if .Values.redis.enabled }}
{{- if .Values.redis.auth.enabled }}
{{- printf "redis://:%s@%s-master:6379" .Values.redis.auth.password (include "infoterminal.redis.fullname" .) }}
{{- else }}
{{- printf "redis://%s-master:6379" (include "infoterminal.redis.fullname" .) }}
{{- end }}
{{- else }}
{{- printf "redis://%s:%d" .Values.externalRedis.host .Values.externalRedis.port }}
{{- end }}
{{- end }}

{{/*
Create Neo4j connection string
*/}}
{{- define "infoterminal.neo4j.connectionString" -}}
{{- if .Values.neo4j.enabled }}
{{- printf "bolt://neo4j:%s@%s:7687" .Values.neo4j.neo4j.password (include "infoterminal.neo4j.fullname" .) }}
{{- else }}
{{- printf "bolt://%s:%s@%s:7687" .Values.externalNeo4j.user .Values.externalNeo4j.password .Values.externalNeo4j.host }}
{{- end }}
{{- end }}

{{/*
Create OpenSearch connection string
*/}}
{{- define "infoterminal.opensearch.connectionString" -}}
{{- if .Values.opensearch.enabled }}
{{- printf "https://%s:9200" (include "infoterminal.opensearch.fullname" .) }}
{{- else }}
{{- printf "https://%s:9200" .Values.externalOpenSearch.host }}
{{- end }}
{{- end }}

{{/*
Create image name for a service
*/}}
{{- define "infoterminal.image" -}}
{{- $registry := .Values.image.registry -}}
{{- $repository := .Values.image.repository -}}
{{- $tag := .Values.image.tag | default .Chart.AppVersion -}}
{{- $service := .service -}}
{{- if .Values.global.imageRegistry }}
{{- $registry = .Values.global.imageRegistry -}}
{{- end }}
{{- printf "%s/%s/%s:%s" $registry $repository $service $tag }}
{{- end }}

{{/*
Create common environment variables
*/}}
{{- define "infoterminal.commonEnvVars" -}}
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: {{ include "infoterminal.fullname" . }}-secrets
      key: database-url
- name: REDIS_URL
  value: {{ include "infoterminal.redis.connectionString" . | quote }}
- name: NEO4J_URI
  value: {{ include "infoterminal.neo4j.connectionString" . | quote }}
- name: OPENSEARCH_URL
  value: {{ include "infoterminal.opensearch.connectionString" . | quote }}
- name: JWT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ include "infoterminal.fullname" . }}-secrets
      key: jwt-secret
- name: LOG_LEVEL
  value: {{ .Values.config.logging.level | quote }}
- name: LOG_FORMAT
  value: {{ .Values.config.logging.format | quote }}
- name: METRICS_ENABLED
  value: {{ .Values.config.observability.metrics.enabled | quote }}
- name: TRACING_ENABLED
  value: {{ .Values.config.observability.tracing.enabled | quote }}
{{- if .Values.config.observability.tracing.enabled }}
- name: JAEGER_ENDPOINT
  value: {{ .Values.config.observability.tracing.jaeger.endpoint | quote }}
{{- end }}
{{- end }}

{{/*
Create security context
*/}}
{{- define "infoterminal.securityContext" -}}
{{- if .Values.security.containerSecurityContext }}
securityContext:
  {{- toYaml .Values.security.containerSecurityContext | nindent 2 }}
{{- else }}
securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
{{- end }}
{{- end }}

{{/*
Create pod security context
*/}}
{{- define "infoterminal.podSecurityContext" -}}
{{- if .Values.security.securityContext }}
securityContext:
  {{- toYaml .Values.security.securityContext | nindent 2 }}
{{- else }}
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000
{{- end }}
{{- end }}

{{/*
Create resource specifications
*/}}
{{- define "infoterminal.resources" -}}
{{- $serviceName := .service -}}
{{- $resources := index .Values.resources $serviceName -}}
{{- if $resources }}
resources:
  {{- toYaml $resources | nindent 2 }}
{{- end }}
{{- end }}

{{/*
Create standard volume mounts
*/}}
{{- define "infoterminal.volumeMounts" -}}
- name: config
  mountPath: /app/config
  readOnly: true
- name: tmp
  mountPath: /tmp
- name: cache
  mountPath: /app/cache
{{- with .Values.extraVolumeMounts }}
{{- toYaml . | nindent 0 }}
{{- end }}
{{- end }}

{{/*
Create standard volumes
*/}}
{{- define "infoterminal.volumes" -}}
- name: config
  configMap:
    name: {{ include "infoterminal.fullname" . }}-config
- name: tmp
  emptyDir: {}
- name: cache
  emptyDir: {}
{{- with .Values.extraVolumes }}
{{- toYaml . | nindent 0 }}
{{- end }}
{{- end }}

{{/*
Create network policy rules
*/}}
{{- define "infoterminal.networkPolicyRules" -}}
{{- if .Values.networkPolicy.enabled }}
- to:
  - podSelector:
      matchLabels:
        app.kubernetes.io/name: {{ include "infoterminal.name" . }}
- to:
  - podSelector:
      matchLabels:
        app: postgresql
  ports:
  - protocol: TCP
    port: 5432
- to:
  - podSelector:
      matchLabels:
        app: redis
  ports:
  - protocol: TCP
    port: 6379
- to:
  - podSelector:
      matchLabels:
        app: neo4j
  ports:
  - protocol: TCP
    port: 7687
- to:
  - podSelector:
      matchLabels:
        app: opensearch
  ports:
  - protocol: TCP
    port: 9200
{{- end }}
{{- end }}

{{/*
Create service monitor labels
*/}}
{{- define "infoterminal.serviceMonitor.labels" -}}
{{- include "infoterminal.labels" . }}
{{- if .Values.monitoring.prometheus.serviceMonitor.labels }}
{{- toYaml .Values.monitoring.prometheus.serviceMonitor.labels | nindent 0 }}
{{- end }}
{{- end }}

{{/*
Validate required values
*/}}
{{- define "infoterminal.validateValues" -}}
{{- if not .Values.postgresql.enabled }}
  {{- if not .Values.externalDatabase.host }}
    {{- fail "PostgreSQL is disabled but no external database host is provided" }}
  {{- end }}
{{- end }}
{{- if not .Values.redis.enabled }}
  {{- if not .Values.externalRedis.host }}
    {{- fail "Redis is disabled but no external Redis host is provided" }}
  {{- end }}
{{- end }}
{{- if .Values.ingress.enabled }}
  {{- if not .Values.ingress.hosts }}
    {{- fail "Ingress is enabled but no hosts are defined" }}
  {{- end }}
{{- end }}
{{- end }}

{{/*
Create anti-affinity rules
*/}}
{{- define "infoterminal.antiAffinity" -}}
{{- if .Values.affinity }}
affinity:
  {{- toYaml .Values.affinity | nindent 2 }}
{{- else }}
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            {{- include "infoterminal.selectorLabels" . | nindent 12 }}
            app.kubernetes.io/component: {{ .component }}
        topologyKey: kubernetes.io/hostname
{{- end }}
{{- end }}
