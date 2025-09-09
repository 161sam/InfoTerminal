# 6. Observability & Monitoring

Ein zentrales Prinzip von **InfoTerminal** ist **Transparenz**:
Alle wichtigen Dienste liefern **Metriken, Logs und Traces**, sodass der Systemzustand jederzeit nachvollziehbar ist.

---

## 6.1 Architektur der Observability

InfoTerminal nutzt ein **Observability-Profile**, das bei Bedarf gestartet werden kann:

```bash
docker compose --profile observability up -d
```

Die folgenden Tools sind vorkonfiguriert:

| Tool             | Funktion                          | Port |
| ---------------- | --------------------------------- | ---- |
| **Prometheus**   | Sammlung von Metriken             | 3412 |
| **Grafana**      | Dashboards & Visualisierung       | 3413 |
| **Alertmanager** | Alarme & Benachrichtigungen       | 3414 |
| **Loki**         | Log-Sammlung                      | 3415 |
| **Tempo**        | Tracing (Verfolgung von Requests) | 3416 |

👉 Alle Tools sind optional: Nutzer können nur jene starten, die benötigt werden.

---

## 6.2 Metriken

Jeder Service stellt eigene Metriken bereit, die über **Prometheus** gesammelt werden.

- **Zugriffspunkt**:

  ```http
  http://localhost:<port>/metrics
  ```

- **Sicherheits-Policy**: Metriken sind nur aktiv, wenn `IT_ENABLE_METRICS=1` gesetzt ist.
- **Beispiele**:
  - Anzahl aktiver Requests
  - Dauer von API-Aufrufen
  - Status von Datenbankverbindungen

---

## 6.3 Logs

Logs werden zentral über **Loki** gesammelt.

- **Standard-Format**: JSON mit `X-Request-Id` zur Nachverfolgung
- **Abfrage**: über Grafana oder CLI
- **Beispiel**:

  ```json
  {
    "time": "2025-09-05T11:30:14Z",
    "service": "graph-api",
    "level": "INFO",
    "request_id": "abc123",
    "message": "Cypher query executed"
  }
  ```

👉 So können alle Aktionen nachvollzogen werden, ohne dass lokale Logfiles durchsucht werden müssen.

---

## 6.4 Traces

Für die Analyse komplexer Abläufe werden **Distributed Traces** genutzt (über **Tempo**).

- Aktivierung:

  ```env
  IT_OTEL=1
  ```

- Verknüpfung von Requests über mehrere Services hinweg
- Hilfreich bei Performance-Analysen & Debugging

---

## 6.5 Dashboards

**Grafana** und **Superset** bieten nutzerfreundliche Visualisierung:

- **Grafana**:
  - Service-Status in Echtzeit
  - Logs & Traces integriert
  - Alerts konfigurieren

- **Superset**:
  - Business-Dashboards
  - KPI-Monitoring mit Cross-Filter
  - Deep-Links zu Graph- und Suchergebnissen

👉 Kombination: **Grafana** für **Technik**, **Superset** für **Inhalt**.

---

## 6.6 Best Practices

- Starte Observability nur, wenn du Monitoring benötigst → spart Ressourcen
- Nutze `it status` regelmäßig, um den Systemzustand abzufragen
- Richte Alerts ein, wenn du InfoTerminal produktiv betreibst
- Verknüpfe Logs & Traces mit Request-IDs für klare Nachvollziehbarkeit

---
