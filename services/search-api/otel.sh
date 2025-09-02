#!/usr/bin/env bash
export OTEL_SERVICE_NAME=search-api
export OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector.observability.svc.cluster.local:4317
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_TRACES_SAMPLER=parentbased_traceidratio
export OTEL_TRACES_SAMPLER_ARG=0.2
opentelemetry-instrument uvicorn app:app --host 0.0.0.0 --port 8080
