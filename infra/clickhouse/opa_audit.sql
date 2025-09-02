CREATE DATABASE IF NOT EXISTS logs;

CREATE TABLE IF NOT EXISTS logs.opa_decisions
(
  ts           DateTime DEFAULT now(),
  path         String,
  decision_id  String,
  user         String,
  roles        Array(String),
  tenant       String,
  classification String,
  action       String,
  allowed      UInt8,
  policy_version String DEFAULT '',
  raw          String
)
ENGINE = MergeTree
ORDER BY (ts, path, user)
TTL ts + INTERVAL 30 DAY;
