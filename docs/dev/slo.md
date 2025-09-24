# Core Service SLOs & Alerting

This playbook defines the service level objectives (SLOs) for the four core InfoTerminal APIs (gateway, search-api, graph-api, doc-entities) and explains how to operate the new Grafana panels and Prometheus alerts.

## Target Summary

| Service | Availability (30d rolling) | Latency Objective (p95) | Error Budget | Notes |
| --- | --- | --- | --- | --- |
| `gateway` | 99.5% | ≤ 350 ms | 0.5% | Front-door for all user traffic; alerts block release train when breached. |
| `search-api` | 99.5% | ≤ 400 ms | 0.5% | Covers both query and rerank paths; latency measured via `http_server_duration_seconds`. |
| `graph-api` | 99.5% | ≤ 500 ms | 0.5% | Includes geo routers; slow queries should prefer async jobs over synchronous calls. |
| `doc-entities` | 99.0% | ≤ 600 ms | 1.0% | NLP workloads are heavier; error budget doubled to reflect model variability. |

> **Why 30 days?** Prometheus evaluates the ratios on 1h/6h windows, but the burn-rate thresholds are calibrated against a 30 day SLO window. Staying below the burn thresholds guarantees we do not consume more than the configured error budget over the SLO period.

## Grafana Panels (dashboard `API SLO`)

The Grafana dashboard at `grafana/dashboards/api-slo.json` now exposes SLI panels per service:

- **Availability** – percentage of successful requests (`status!~"5.."`) over the last 5 minutes.
- **Latency p95** – computed from `http_server_duration_seconds_bucket` per service.
- **Error rate** – 5xx ratio per service.

Use the standard Grafana share link to export a PDF for incident reviews. When Tempo is enabled, the existing trace panels help correlate request spikes with slow spans.

## Prometheus Alert Rules

`monitoring/alerts/performance-alerts.yml` contains three new alert definitions under the `infoterminal.slo` group:

1. **`CoreServiceAvailabilityFastBurn`** – triggers when any core service spends more than 2% of its monthly error budget in one hour (burn-rate > 4× for a 99.5% SLO).
2. **`CoreServiceAvailabilitySlowBurn`** – warns when 5% of the monthly budget would be depleted within six hours (burn-rate > 10×). This keeps on-call aware of prolonged degradation.
3. **`CoreServiceP95LatencyBreached`** – fires if the p95 latency stays above the service-specific thresholds (350/400/500/600 ms) for 5 minutes.

All alerts share the `team=platform` label so PagerDuty and Slack routing rules can stay consistent with the existing performance alerts. Burn-rate rules rely on `http_requests_total` and assume request metrics expose the `service` label (already enforced by `_shared.obs.metrics_boot`).

## Testing the Alerts (Fake Series)

For development or demos you can inject temporary metrics through the Pushgateway profile exposed in `charts/infoterminal/values.yaml`. Example commands:

```bash
# Send a fake 3% error ratio for search-api (triggers fast burn + slow burn)
cat <<'METRICS' | curl -sS --data-binary @- \
  http://localhost:9091/metrics/job/slo-test/service/search-api
it_slo_fake_error_ratio{service="search-api"} 0.03
METRICS

# Push a 0.7s p95 latency for doc-entities (triggers latency alert)
cat <<'METRICS' | curl -sS --data-binary @- \
  http://localhost:9091/metrics/job/slo-test/service/doc-entities
it_slo_fake_p95_seconds{service="doc-entities"} 0.7
METRICS
```

Remove the fake series by deleting the Pushgateway job once testing is complete:

```bash
curl -X DELETE http://localhost:9091/metrics/job/slo-test
```

Prometheus will pick up the new samples within the next scrape cycle and the alerts become visible in Grafana's **Alerting → Alert rules** page. Clear the Pushgateway job after the dry run to avoid flapping notifications.

## Escalation Path

1. **Fast burn (critical)** – Page the on-call engineer immediately. Mitigate within the 30-minute target. Escalate to the staff engineer on duty if the alert is still active after 15 minutes.
2. **Slow burn (warning)** – Investigate within business hours, but create an incident if two consecutive slow-burn alerts appear in 24 hours.
3. **Latency breach (warning)** – Confirm with Tempo traces whether a single downstream dependency is responsible. If multiple services degrade, coordinate with the infrastructure team for capacity adjustments.

Document the resolution in the incident tracker and add a postmortem entry when burn-rate alerts page.

## Tuning & Maintenance

- **Adjusting thresholds** – Update the SLO table above and the alert thresholds together. For latency alerts, modify the constant vectors in `CoreServiceP95LatencyBreached` so the documentation and alert logic stay aligned.
- **Adding services** – Extend the `service=~"(...)"` regex in both Grafana queries and alert rules, then append the new service to the SLO table.
- **Validating math** – Use `promtool test rules monitoring/alerts/performance-alerts.yml` with recorded series for regression tests before shipping major changes.
- **Dashboard reviews** – Snapshot the `API SLO` dashboard each quarter and archive it in the ops wiki to keep historical SLO compliance evidence.

Keeping SLO definitions, dashboard panels, and alert math in sync ensures the platform meets the observability DoD for roadmap item **J3**.
