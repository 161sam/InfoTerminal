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
    const { getNodeAutoInstrumentations } = require("@opentelemetry/auto-instrumentations-node");
    const exporterChoice = (process.env.IT_OTEL_EXPORTER || "otlp").toLowerCase();
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
    let traceExporter: any;
    if (exporterChoice === "jaeger") {
      try {
        const { JaegerExporter } = require("@opentelemetry/exporter-jaeger");
        traceExporter = new JaegerExporter({
          endpoint: process.env.OTEL_EXPORTER_JAEGER_ENDPOINT || "http://jaeger:14268/api/traces",
          username: process.env.OTEL_EXPORTER_JAEGER_USER,
          password: process.env.OTEL_EXPORTER_JAEGER_PASSWORD,
        });
      } catch (err) {
        console.warn("jaeger exporter unavailable, falling back to otlp", err);
        traceExporter = new OTLPTraceExporter({ url: endpoint });
      }
    } else {
      traceExporter = new OTLPTraceExporter({ url: endpoint });
    }
    process.env.OTEL_PROPAGATORS = process.env.OTEL_PROPAGATORS || "tracecontext,baggage";
    const sdk = new NodeSDK({
      resource: new Resource(attrs),
      traceExporter,
      sampler: new ParentBasedSampler({
        root: new TraceIdRatioBasedSampler(ratio),
      }),
      instrumentations: getNodeAutoInstrumentations({
        "@opentelemetry/instrumentation-http": {
          ignoreIncomingPaths: ["/healthz", "/readyz", "/metrics"],
        },
      }),
    });
    sdk.start();
    (global as any).__otelSdk = sdk;
  } catch (err) {
    console.warn("otel setup failed", err);
  }
}
