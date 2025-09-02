const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { Resource } = require('@opentelemetry/resources');

const endpoint = process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://otel-collector.default.svc:4317';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({ url: endpoint }),
  instrumentations: [getNodeAutoInstrumentations()],
  resource: new Resource({
    'service.name': process.env.OTEL_SERVICE_NAME || 'gateway'
  })
});

sdk.start().catch(console.error);
