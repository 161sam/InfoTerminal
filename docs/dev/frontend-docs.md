# Frontend Health Monitoring

The frontend exposes `GET /api/health` which pings core backend services and returns their status and latency.

```ts
GET /api/health -> {
  timestamp: string;
  services: {
    search: { state: 'ok'|'degraded'|'down'|'unreachable'; latencyMs: number|null };
    graph: { state: 'ok'|'degraded'|'down'|'unreachable'; latencyMs: number|null };
    docentities: { state: 'ok'|'degraded'|'down'|'unreachable'; latencyMs: number|null };
    nlp: { state: 'ok'|'degraded'|'down'|'unreachable'; latencyMs: number|null };
  }
}
```

The `GlobalHealth` widget polls this API every 15 seconds by default. States map to colored dots:

- **ok** – green
- **degraded** – yellow
- **down/unreachable** – red or gray

If the badge turns red, use the "Force refresh" option or check the Docker compose logs for the affected service.
