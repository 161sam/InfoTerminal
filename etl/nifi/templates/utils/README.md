# NiFi Normalization Utilities (Jolt → OpenSearch)

This folder provides a generic normalization pipeline using Jolt and convenience specs for common feeds.

## Templates

- `utils/jolt_normalize_to_opensearch.xml`
  - SplitJson (optional, param `json.path`, default `$.[*]`)
  - JoltTransformJSON (param `jolt.spec`)
  - PutElasticsearchHttp (params `opensearch.url`, `index.name`)

## Jolt Specs

- `jolt_specs/mastodon_to_generic.json`
  - id, content→text, created_at→ts, account.acct→author, url
  - default: `type=mastodon_status`
- `jolt_specs/github_to_generic.json`
  - id, type, created_at→ts, actor.login→author, repo.name→repo, payload passthrough
  - default: `source=github, kind=event`
- `jolt_specs/hn_to_generic.json`
  - Topstories array → id (note: details require additional fetch)
  - default: `type=hn_topstory, source=hackernews`
- `jolt_specs/telegram_to_generic.json`
  - update_id→id, message.text→text, message.date→ts, from.username→author, chat info
  - default: `type=telegram_update, source=telegram`
- `jolt_specs/shodan_to_generic.json`
  - maps host, port, ip_str, org to {id, host, port, ip, org}, default: `source=shodan, type=host`
- `jolt_specs/otx_to_generic.json`
  - maps pulse name, indicator to {id, name, indicator, ts}, default: `source=otx, type=pulse_indicator`
- `jolt_specs/rss_to_generic.json`
  - maps RSS entries to {id, title, link, ts}, default: `source=rss, type=item`

## Example Parameter Context (`feeds_generic`)

- `opensearch.url = http://opensearch:9200`
- `index.name = feeds_generic`
- `json.path = $.[*]`
- `jolt.spec =` (Paste JSON spec contents, multi-line supported in NiFi)

For Mastodon:
- `mastodon.base.url = https://mastodon.social`
- `mastodon.token = <your-token>`

Then import one of the `*to_opensearch.xml` templates (or chain your feed → SplitJson → Jolt → PutElasticsearchHttp) and bind the Parameter Context.

You can also import a ready Parameter Context via NiFi API using the export file:

- `param_contexts/feeds_generic.json`
  - POST it to `/nifi-api/parameter-contexts` or use it as a reference to create the context in UI

Example (via curl):
```
curl -X POST -H 'Content-Type: application/json' \
  -d @etl/nifi/templates/utils/param_contexts/feeds_generic.json \
  http://localhost:8080/nifi-api/parameter-contexts
```

Tip: For large documents, consider using `Record` processors with a JSONTreeReader + JoltTransformRecord.
