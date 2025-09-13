# n8n Automation Guide

The agent connector can trigger n8n workflows either via a preconfigured webhook URL or the REST API.

## Webhook

Set `N8N_WEBHOOK_URL` in the environment. The connector will POST the playbook parameters to this URL.

## REST API

Configure `N8N_BASE_URL` and `N8N_API_KEY`. The connector calls `POST /rest/workflows/run` with the given `params`.

Example for the `FinancialRiskAssistant`:

```json
{
  "name": "FinancialRiskAssistant",
  "params": {"account": "123"}
}
```

The response contains the trigger status and optional run information.
