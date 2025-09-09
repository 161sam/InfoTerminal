# Palantir Gotham – technische Recherche (Stand: 5. Sept 2025)

## Wofür ist Gotham gebaut? (Ziele & typische Einsätze)

* **Operative Entscheidungsunterstützung** in dynamischen Lagen (militärisch, Polizei, Nachrichtendienste) — Daten aus vielen Systemen zusammenführen, analysieren und in Maßnahmen übersetzen. Typische Workflows: Ermittlungen, Missionsplanung/-durchführung, Zielauswahl, After-Action-Analyse. ([Palantir][1])
* **„Needles in thousands of haystacks“**: Analyse sehr großer, verteilter Datentöpfe; Ursprung im Umfeld von Verteidigung/Intelligence (später auch in anderen Domänen eingesetzt). ([SEC][2])
* **Privatsphäre/Compliance**: Granulare Zugriffskontrollen, Audit-Trails, Einbindung in regulierte/klassifizierte Umgebungen. ([Wget 2014][3])

## Was kann Gotham? (Fähigkeiten in der Praxis)

* **Integriertes Datenmodell (Ontologie)**: Objekte/Ereignisse und Relationen statt reiner Tabellen; föderierter Zugriff auf externe Systeme; einheitliche Suche/Discovery.&#x20;
* **Analytik-Apps & Workspace** (im Browser/leichter Desktop-Client):
  **Link-/Netzwerkanalyse**, **Geospatial**, **CDR-Analyse**, **Object-/Entity-Analyse**, **Dossier** (dynamische Berichte), **Gaia** (Lagebild/Missionskoordination), **Video** (nahezu Echtzeit-Streams mit ML-Detektionen inkl. Feedback-Loop).&#x20;
* **Kollaboration & Sicherheit**: Feingranulare ACLs bis auf Attribut-Ebene, umfassende Audit-Logs (konfigurierbar manipulationssicher), Arbeiten über Sicherheitsdomänen und auch bei niedriger Bandbreite/Latenz.&#x20;
* **Offene Schnittstellen & Erweiterbarkeit**: Öffentliche APIs „auf jeder Ebene“, Export in offene Formate, Einbindung eigener/3rd-party-Modelle; monatliche Updates, HA/Backup/Rescue-Mechanismen. ([Apply to Supply][4])
* **Einsatzumgebungen**: Public/Private/Hybrid/Community-Cloud; Browser-GUI, optional leichter Windows-Client (JRE + JXBrowser). ([Apply to Supply][4])

## Welche Protokolle & Integrationsarten werden verwendet?

**Plattform- & API-Schicht**

* **REST über HTTPS mit JSON** als Standard-API-Stil für Gotham (inkl. Fehler-Semantik). ([Palantir][5])
* **OAuth 2.0 (Bearer Tokens)** für API-Auth (Third-party-App-Registrierung, OAuth2-Flows). ([Palantir][6])
* **SSO/IdP-Integration** über **SAML 2.0** und **OIDC 1.0** (plattformweit; in Palantir-Doku unter Foundry beschrieben, gilt für das gemeinsame Auth-Modell). ([Palantir][7])
* **OpenAPI/Swagger-Doku** verfügbar (kundenseitig, kein öffentliches Sandbox-API). ([Apply to Supply][4])

**Daten-/Connector-Schicht**
Gotham **inkorporiert Foundry-Fähigkeiten** für Datenanschluss & Pipelines; damit stehen industrienahe Standards zur Verfügung:

* **JDBC/ODBC/SQL** für DWH/DBs; **Flat-Files**, **HDFS**, **JSON/REST**. ([Apply to Supply][4])
* **Kafka** (inkl. TLS/SASL-Empfehlungen; Standard-Protokolle, keine proprietären Erweiterungen nötig). ([Palantir][8])

**Entwickler-Toolchain**

* **Conjure** (Palantirs eigener, **HTTP/JSON**-RPC-Toolchain) generiert Client/Server-Stubs (Java, TS, Python, Rust u. a.) aus YAML-Spezifikationen; breit in Palantir-Produkten genutzt. ([Palantir Blog][9], [GitHub][10])
* Offizielle SDKs/Libs (u. a. **Gotham Python SDK** via Palantir-PyPI-Profil). ([PyPI][11])

## Architektur-/Betriebsdetails (aus öffentlichen Unterlagen)

* **Datenhaltung & Indizes**: Sekundär-Indices/Views u. a. in **Elasticsearch** oder **Postgres**; Snapshots/Backups in S3/Azure/GCS. (Primäre Stores kundenspezifisch, Sekundäres rehydrierbar.)&#x20;
* **Updates & Support**: Regelmäßige Releases (monatlich); ältere, blockierte Versionen gelten als „unsupported“. ([Apply to Supply][4])
* **Preis/Kommerz**: G-Cloud listet eine Beispielgröße („£66,000 a unit“; Details vertraglich). ([Apply to Supply][4])

## Was kann die Software – und was nicht?

### Kann (Auswahl)

* **End-to-End-Workflows** für Ermittlungen, Operationen, Lagebilder; skalierbare Analysen (Graph, Geo, CDR, Video/ML); rollenbasierte Freigaben, lückenlose Nachvollziehbarkeit.&#x20;
* **Interop ohne Vendor-Lock-in** laut Anbieter: offene Formate, öffentliche APIs, Export/Offboarding prozessual verankert. ([Apply to Supply][4])

### Kann nicht / Grenzen

* **Liefert keine „eigenen Daten“**: Gotham ist Software, kein Datenhändler oder Web-Crawler; Mehrwert entsteht erst durch die (rechtssichere) Anbindung deiner Quellen. ([WIRED][12])
* **Ersetzt keine rechtliche Governance**: Einsatz unterliegt lokalem Recht; in Deutschland wurden automatisierte Analysebefugnisse gesetzlich begrenzt (BVerfG-Urteil mit Auswirkungen auf Gotham-Nutzung). ([WIRED][13])
* **Kein offener Developer-Spielplatz**: APIs sind kundenseitig, **kein öffentliches Sandbox-Environment**; Mobile-Funktionalität eingeschränkt ggü. Desktop. ([Apply to Supply][4])

## Kurzvergleich „Marketing vs. belastbare Details“

* **Marketingseiten** betonen „AI-ready OS für Entscheidungen“; die **G-Cloud-Unterlagen** liefern harte Fakten: konkrete Apps (Dossier, Gaia, Video), Ontologie-Modellierung, REST/OAuth2, Export/Offboarding, Backup/Rescue und technische Mindestanforderungen. ([Palantir][14], [Apply to Supply][4])

---

### Takeaways für eine eigene „Gotham-ähnliche“ Plattform

* **API-Stil**: REST/HTTPS + JSON, OAuth2; SSO via SAML/OIDC. **Toolchain**: Conjure-ähnliche IDL/Codegen spart Integrationskosten. ([Palantir][5], [Palantir Blog][9])
* **Datenmodell**: Objekt-/Ereignis-Graph mit Föderation; First-class-Apps für Graph/Geo/Video & Berichtswesen.&#x20;
* **Ops**: Regelmäßige Updates, HA/Backups, Export-Garantien → reduziert Lock-in-Risiko. ([Apply to Supply][4])


[1]: https://www.palantir.com/platforms/gotham/?utm_source=chatgpt.com "Gotham"
[2]: https://www.sec.gov/Archives/edgar/data/1321655/000119312520230013/d904406ds1.htm?utm_source=chatgpt.com "Registration Statement on Form S-1"
[3]: https://wget2014.files.wordpress.com/2014/04/16_palantir-gotham-upholding-data-protection-regulations-in-the-european-union.pdf?utm_source=chatgpt.com "PALANTIR GOTHAM"
[4]: https://www.applytosupply.digitalmarketplace.service.gov.uk/g-cloud/services/801146272055049 "
  Palantir Platform: Gotham - Digital Marketplace
"
[5]: https://palantir.com/docs/gotham/api/general/overview/introduction//?utm_source=chatgpt.com "Introduction • API Reference"
[6]: https://palantir.com/docs/gotham/api/general/overview/authentication//?utm_source=chatgpt.com "Authentication • API Reference"
[7]: https://palantir.com/docs/foundry/authentication/overview/?utm_source=chatgpt.com "Authentication • Overview"
[8]: https://palantir.com/docs/foundry/available-connectors/kafka/?utm_source=chatgpt.com "Available connectors • Kafka"
[9]: https://blog.palantir.com/introducing-conjure-palantirs-toolchain-for-http-json-apis-2175ec172d32?utm_source=chatgpt.com "Introducing Conjure, Palantir's toolchain for HTTP/JSON ..."
[10]: https://github.com/palantir/conjure?utm_source=chatgpt.com "palantir/conjure: Strongly typed HTTP/JSON APIs ..."
[11]: https://pypi.org/user/palantir-pypi/?utm_source=chatgpt.com "Profile of palantir-pypi"
[12]: https://www.wired.com/story/palantir-what-the-company-does?utm_source=chatgpt.com "What Does Palantir Actually Do?"
[13]: https://www.wired.com/story/palantir-germany-gotham-dragnet?utm_source=chatgpt.com "Germany Raises Red Flags About Palantir's Big Data Dragnet"
[14]: https://www.palantir.com/platforms/?utm_source=chatgpt.com "Palantir Platforms"
