# Deep link schema

Superset charts link to InfoTerminal frontend using the following templates:

```text
https://INFOTERMINAL_BASE_URL/asset/{asset_id}?from=YYYY-MM-DD&to=YYYY-MM-DD&tab=chart
https://INFOTERMINAL_BASE_URL/person/{person_id}?tab=graph
```

`from` and `to` are ISO dates limiting the displayed range.
The optional `tab` parameter selects the initial tab (`chart`, `graph`, `news`).

Example usage in Superset SQL:

```sql
concat('${INFOTERMINAL_BASE_URL}/asset/', asset_id,
       '?from=', format_datetime(ts, 'YYYY-MM-DD'),
       '&to=', format_datetime(ts, 'YYYY-MM-DD'))
```
