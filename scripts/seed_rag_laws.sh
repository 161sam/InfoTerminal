#!/usr/bin/env bash
set -euo pipefail

# Seed rag-api with example law paragraphs (idempotent upserts)
# Usage: ./scripts/seed_rag_laws.sh [RAG_API_URL]
# Env: DRY_RUN=1 to print only

RAG_API_URL="${1:-${RAG_API_URL:-http://localhost:8622}}"

docs='[
  {"id":"arbSchG_23_1","title":"§23 ArbSchG – Verantwortlichkeiten","paragraph":"§23 (1)","text":"Der Arbeitgeber hat die erforderlichen Maßnahmen des Arbeitsschutzes zu treffen ...","domain":"Arbeitsrecht","source":"DE/ArbSchG","effective_date":"2013-01-01"},
  {"id":"stgb_263","title":"§263 StGB – Betrug","paragraph":"§263","text":"Wer in der Absicht, sich oder einem Dritten einen rechtswidrigen Vermögensvorteil zu verschaffen ...","domain":"Strafrecht","source":"DE/StGB","effective_date":"1998-04-01"},
  {"id":"eu_esg_2020","title":"EU-Verordnung 2020/852 – Taxonomie","paragraph":"Art. 9","text":"Ziel der Verordnung ist die Festlegung der Kriterien zur Bestimmung, ob eine wirtschaftliche Tätigkeit als ökologisch nachhaltig einzustufen ist ...","domain":"EU-Recht","source":"EU/2020/852","effective_date":"2020-06-22"}
]'

echo "Seeding rag-api at $RAG_API_URL"
for row in $(echo "$docs" | jq -c '.[]'); do
  id=$(echo "$row" | jq -r .id)
  echo "→ Index $id"
  if [ "${DRY_RUN:-0}" = "1" ]; then
    echo "POST $RAG_API_URL/law/index => $row"
  else
    curl -fsS -X POST "$RAG_API_URL/law/index" -H 'Content-Type: application/json' -d "$row" >/dev/null
  fi
done

echo "✅ Seed complete"

