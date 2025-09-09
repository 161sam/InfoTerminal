# NiFi → Aleph Dokumenten-Pipeline

Ziel ist eine minimal lauffähige Strecke, die Dateien aus einem Watch-Folder
über NiFi nach Aleph überträgt und optional zur `doc-entities`‑API schickt.

```text
[data/inbox] --> [NiFi Flow] --> [Aleph] --> [doc-entities]
                           \--> [outbox]
```

## Setup

```bash
# Services starten
docker compose up -d aleph nifi doc-entities

# Beispiel .env
cat <<ENV > .env
ALEPH_API_KEY=<dev-token>
COLLECTION_ID=<id>
ENV
```

Der Watch-Folder befindet sich in `./data/inbox`, Artefakte landen in
`./data/outbox`.

## Template importieren & Flow starten

```bash
make nifi-template-import
make nifi-template-instantiate
make nifi-start
```

## Test

Kopiere eine Datei in den Watch-Folder:

```bash
cp examples/docs/demo1.pdf data/inbox/
```

Im Aleph UI sollte das Dokument erscheinen. Optional lassen sich die
Annotationen über `GET http://localhost:8006/docs/<id>` abfragen.

## Troubleshooting

- NiFi Bulletin Board prüfen (`http://localhost:8085/nifi`)
- `InvokeHTTP` 401 → API Key oder URL prüfen
- Große Dateien: `nifi.properties` anpassen (Speicher)
