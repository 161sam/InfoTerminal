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

## Example Parameter Context (`feeds_generic`)

- `opensearch.url = http://opensearch:9200`
- `index.name = feeds_generic`
- `json.path = $.[*]`
- `jolt.spec =` (Paste JSON spec contents, multi-line supported in NiFi)

For Mastodon:
- `mastodon.base.url = https://mastodon.social`
- `mastodon.token = <your-token>`

Then import one of the `*to_opensearch.xml` templates (or chain your feed → SplitJson → Jolt → PutElasticsearchHttp) and bind the Parameter Context.

Tip: For large documents, consider using `Record` processors with a JSONTreeReader + JoltTransformRecord.
