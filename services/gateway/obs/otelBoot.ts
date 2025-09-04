let initialized = false;

export function setupOtel(serviceName = "gateway"): void {
  if (initialized || process.env.IT_OTEL !== "1") {
    return;
  }
  initialized = true;
  try {
    const { NodeSDK } = require("@opentelemetry/sdk-node");
    const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-http");
    const { Resource } = require("@opentelemetry/resources");
    const { SemanticResourceAttributes } = require("@opentelemetry/semantic-conventions");
    const { ParentBasedSampler, TraceIdRatioBasedSampler } = require("@opentelemetry/sdk-trace-base");
    const endpoint = process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? "http://tempo:4318";
    const ratio = Number(process.env.OTEL_TRACES_SAMPLER_ARG ?? "0.1");
    const attrs: Record<string, string> = {
      [SemanticResourceAttributes.SERVICE_NAME]: process.env.OTEL_SERVICE_NAME || serviceName,
    };
    if (process.env.OTEL_RESOURCE_ATTRIBUTES) {
      for (const part of process.env.OTEL_RESOURCE_ATTRIBUTES.split(",")) {
        const [k, v] = part.split("=", 2);
        if (k && v) attrs[k] = v;
      }
    }
    const sdk = new NodeSDK({
      resource: new Resource(attrs),
      traceExporter: new OTLPTraceExporter({ url: endpoint }),
      sampler: new ParentBasedSampler({
        root: new TraceIdRatioBasedSampler(ratio),
      }),
    });
    sdk.start();
    (global as any).__otelSdk = sdk;
  } catch (err) {
    console.warn("otel setup failed", err);
  }
}
