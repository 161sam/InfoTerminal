# 📊 Feature-Mapping: Palantir Gotham vs. InfoTerminal

## 1. Ziele / Mission

**Palantir Gotham**

* Operative Entscheidungsunterstützung (militärisch, Polizei, Intelligence, Behörden).
* Integration verschiedenster Datenquellen (structured, unstructured, streaming).
* Analyse-Workflows: Ermittlungen, Missionsplanung, Risikoerkennung.
* Strikte Governance: Rollenrechte, Audit-Trails, Compliance.

**InfoTerminal (Stand 09/2025)**

* Open-Source Framework für Suche, Graph-Analyse, Dokumentenmanagement & KI.
* Fokus: Datenintegration, Recherche, Visualisierung → inspiriert von Gotham, aber offen.
* Governance/Audit-Mechanismen rudimentär (nur Rollen im Gateway/OPA).
* Zielgruppe breiter: Forschung, NGOs, Journalismus, Open-Data.

---

## 2. Architektur

**Palantir Gotham**

* Ontologie-Modell: Entities, Events, Relations als zentrales Datenmodell.
* Föderierte Abfragen (keine Pflicht zur ETL-Kopie aller Daten).
* Apps: Link/Network Analysis, Geospatial, CDR, Video, Dossier.
* Deployment: Cloud (public/private), HA, Backup/Restore.

**InfoTerminal**

* Graph-API (Neo4j), Search-API (OpenSearch), Graph-Views (Postgres).
* Erste Schritte Ontologie: Entities & Relations vorhanden, aber ohne visuelles Ontology-Modeling.
* Apps: Frontend-Suche, Graphx-View, Settings. (kein Video/CDR).
* Deployment: Docker Compose & Local Dev; HA/Backup noch nicht adressiert.

---

## 3. Protokolle & Schnittstellen

**Palantir Gotham**

* REST/HTTPS + JSON (alle APIs).
* OAuth2 (Bearer Tokens), SAML 2.0, OIDC für Auth/SSO.
* Kafka/SQL/JDBC für Data Connectors.
* Conjure (Palantir IDL → Codegen für SDKs).
* Keine offene Sandbox, nur kundenseitige APIs.

**InfoTerminal**

* REST/HTTPS (FastAPI-Services: /search, /graph, /views).
* Auth: aktuell rudimentär; OAuth2 & SSO noch nicht eingebaut.
* Data ingest: geplant über NiFi (Batch/Stream), n8n (Playbooks).
* Schnittstellen: noch keine formale IDL; Python & TS Clients müssen manuell gepflegt.
* API-Doc: automatisch via FastAPI OpenAPI (Swagger-UI).

---

## 4. Features

**Palantir Gotham**

* Graphanalyse (Link Charts, Centrality, Communities).
* Geospatial (Map Overlays, Bewegungsanalysen).
* CDR (Telekom-Records → soziale Netzwerke).
* Dossier (Berichte, dynamisch aus Daten generiert).
* Gaia (Missionskoordination).
* Video-Analyse (Realtime-Feeds mit ML-Detection).
* Audit/Compliance: Attribute-Level-Security, Immutable Logs.
* Collaboration: Multi-User-Editing, Workflows.

**InfoTerminal**

* Graphanalyse: Basis-Nachbarschaften; Centrality/Communities geplant (v0.2).
* Geospatial: noch nicht umgesetzt.
* CDR: nicht vorgesehen (nur generische Graphdaten).
* Dossier: noch nicht vorhanden → könnte mit Superset Reports oder Flowise Assistent entstehen.
* Missionskoordination: nicht geplant (außer durch Playbooks/Agents).
* Video: nicht geplant (Option über NiFi/FFmpeg/ML).
* Audit/Compliance: Logs & OPA, aber keine Attribute-Level-Security.
* Collaboration: rudimentär (Frontend UI + gemeinsamer DB-Zugriff).

---

## 5. Grenzen

**Palantir Gotham**

* Kein Datenprovider → benötigt externe Daten.
* Stark auf regulierte Umgebungen zugeschnitten.
* Proprietär, kein Open-Source, keine offene Sandbox.

**InfoTerminal**

* Noch frühes Stadium (v0.1.x).
* Kein Geospatial/CDR/Video-Stack.
* Kein Identity/SSO-Framework.
* Governance/Audit minimal.
* Aber: Offen, erweiterbar, Open-Source; breiter Fokus.

---

## 6. Mapping-Tabelle (Kurzfassung)

| Bereich          | Gotham                                  | InfoTerminal (09/2025)                     |
| ---------------- | --------------------------------------- | ------------------------------------------ |
| Datenmodell      | Ontologie (Entities/Events/Relations)   | Neo4j Graph, rudimentäre Ontologie         |
| Suche            | Föderiert, semantisch                   | OpenSearch, Basis-NLP geplant              |
| Graphanalyse     | Link/Network, Centrality, Communities   | Basis-Nachbarschaften, Algorithmen geplant |
| Geospatial       | Voll (Map, Movement)                    | Noch nicht                                 |
| CDR              | Speziell (Telco)                        | Nicht geplant                              |
| Dossier/Reports  | Dynamisch, integriert                   | Noch nicht, Superset geplant               |
| Mission/Planning | Gaia-App                                | Nicht geplant (Playbooks via n8n)          |
| Video            | Echtzeit-Analyse                        | Nicht vorgesehen                           |
| Security         | ACL bis Attribute, Immutable Audit Logs | OPA, Logs, keine Attribute-Level           |
| Auth/SSO         | OAuth2, SAML, OIDC                      | Basis, OAuth2 fehlt noch                   |
| APIs             | REST/HTTPS/JSON, Conjure SDK            | REST/HTTPS/JSON (FastAPI)                  |
| Deployment       | HA, Cloud-native, Backup/Restore        | Docker Compose, Local Dev                  |
