# NLP-Annotation

Die Seite **/nlp** bindet den Doc-Entities-Service ein.

## Ablauf

1. Text einfügen oder ein PDF/Docx hochladen.
2. Sprache wählen, optional Zusammenfassung und Relationsextraktion aktivieren.
3. **Annotate** ausführen – erkannte Entitäten werden farblich hervorgehoben, Relationen erscheinen im Tab *Relations*.
4. Über *Resolve Entities* wird eine Entitätsauflösung gestartet (Abgleich mit Neo4j).
5. Mit *Write to Graph* (sofern freigeschaltet) werden Relationen an die Graph-API gesendet.

## Hinweise

- Bei Fehlern (Service offline) erscheint ein Warnbanner; vorhandene Ergebnisse bleiben sichtbar.
- Der JSON-Tab zeigt die Rohantwort der API (`/v1/documents/annotate`).
- Zusammenfassungen und HTML-Anzeigen lassen sich in den Einstellungen deaktivieren (`DocEntitiesSettings`).
