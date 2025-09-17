# Feed Templates (NiFi)

This directory lists NiFi templates for common feeds. Use Parameter Contexts to avoid hardcoding URLs/keys.

Templates:
- rsshub_ingest.xml → `${rsshub.url}`
- otx_iocs.xml → `${otx.api.url}`, `${otx.api.key}`
- shodan_search.xml → `${shodan.api.url}` (include key in URL or via header)
- mqtt_consume.xml → `${mqtt.broker}`, `${mqtt.topic}`

Notes:
- Bind a Parameter Context (e.g. `feeds`) to the Process Group.
- For Tor/Hidden Services, route through your egress gateway/proxy and set `${egress.proxy.url}` accordingly.
