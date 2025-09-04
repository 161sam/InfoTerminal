import type { Express, Request, Response, NextFunction } from "express";
import client from "prom-client";

export function enableMetrics(app: Express, path = "/metrics"): void {
  if (
    (process.env.IT_ENABLE_METRICS !== "1" && process.env.IT_OBSERVABILITY !== "1") ||
    (app as any).__metricsEnabled
  ) {
    return;
  }
  (app as any).__metricsEnabled = true;
  const metricsPath = process.env.IT_METRICS_PATH || path;
  const register = new client.Registry();
  client.collectDefaultMetrics({ register });
  const httpRequests = new client.Histogram({
    name: "http_request_duration_seconds",
    help: "HTTP request duration",
    labelNames: ["method", "route", "status"],
    buckets: [0.05, 0.1, 0.3, 0.5, 1, 2, 5, 10],
  });
  register.registerMetric(httpRequests);
  app.use((req: Request, res: Response, next: NextFunction) => {
    const start = process.hrtime.bigint();
    res.on("finish", () => {
      const dur = Number(process.hrtime.bigint() - start) / 1e9;
      httpRequests
        .labels(
          req.method,
          req.path.replace(/[0-9a-f-]{8,}/g, ":id"),
          String(res.statusCode)
        )
        .observe(dur);
    });
    next();
  });
  app.get(metricsPath, async (_req, res) => {
    res.set("Content-Type", register.contentType);
    res.end(await register.metrics());
  });
}
