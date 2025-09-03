# 📍 InfoTerminal Roadmap

Diese Roadmap beschreibt den Entwicklungsweg von **v0.1.0 (MVP)** bis zur ersten stabilen **v1.0.0 (Production Ready)**.  
Sie ist als lebendes Dokument gedacht und wird regelmäßig angepasst.  

---

## 🎯 Langfristige Ziele

- **Framework-Charakter** wie *Palantir Gotham*, aber Open Source (Open-Core mit optionalen Enterprise-Features).
- **High Autonomous AI-Layer** mit Agents und Workflows.
- **Plugin-System** zur einfachen Erweiterung (z. B. Kali Linux Tools, externe Datenquellen).
- **Monetarisierbarkeit ab v0.5.0** (Early Adopters & Enterprise Add-ons).
- Fokus auf **Features, UX, Stabilität, Deployment**.

---

## 🔖 Versionen & Meilensteine

### v0.1.0 – MVP (aktueller Stand)
**Status:** in arbeit

- 🔎 **Search:** OpenSearch mit Facetten & API.
- 🌐 **Graph:** Neo4j-Integration + Viewer.
- 📄 **Dokumentenmanagement:** Aleph + OCR/NER-Pipeline.
- 📊 **Analytics:** Erste Dashboards (Superset, dbt, Airflow-DAGs).
- 🔐 **Security (Dev):** Keycloak-Login, OPA-Gateway-Policies.
- 🐳 **Deployment:** Docker Compose + Helm-Charts für Dev.
- 📂 **Docs:** Erste Setup- und Dev-Dokumentation.

👉 **Offen (v0.1.x Patches):** NLP-Service, NiFi→Aleph-Flow, Observability, Embedding-Reranking, Flowise-Agenten (Prototyp).

---

### v0.2.0 – KI-Assistent & Workflows
**Fokus:** Smarte Unterstützung, Automatisierung

- 🤖 **Flowise-Agent**: Investigation Assistant, LLM-gestützt, ruft Search/Graph/Docs-APIs auf.
- 🔄 **n8n-Workflows**: Automatisierte Playbooks (z. B. Financial Risk Assistant).
- 📊 **Dashboards**: Deep Links & Cross-Filters.
- 🧠 **NLP-UI**: Entitäten & Zusammenfassungen direkt sichtbar.

**Meilenstein:** Erste teilautonome Analysen per Chatbot + Playbooks.

---

### v0.3.0 – Erweiterte Analysen & Datenqualität
**Fokus:** Tiefe Analysen, Data Governance, Skalierung

- 📈 **Graph-Algorithmen:** Zentralität, Communities, Export/Share.
- ✅ **Data Quality:** dbt-Tests, erweiterte Validierungen.
- 📚 **Data Catalog** (optional): z. B. DataHub/Amundsen.
- ⚡ **ClickHouse**: Zeitreihen-/Big Data-Support.
- 🛠 **Refactoring & Load-Tests**: Stabilität erhöhen.

**Meilenstein:** InfoTerminal skaliert für Big Data und wird vertrauenswürdiger.

---

### v0.4.0 – UX-Optimierung & Plugin-System
**Fokus:** Benutzerfreundlichkeit & Erweiterbarkeit

- 🎨 **UX-Politur**: konsistentes UI, verbesserte Graph-/Doc-Viewer.
- 🔌 **Plugin-Framework**: Standard-Schnittstelle für Tools & Datenquellen.
- 🛡 **Audit-Logs für Plugins**: Nachvollziehbarkeit.
- 🧰 **Kali-Linux-Integration**: Security/OSINT-Tools als Plugins.
- 🧪 **End-to-End-Tests**: vollständige Pipelines prüfen.

**Meilenstein:** Beta-Version – für Pilotprojekte geeignet.

---

### v0.5.0 – Monetarisierung & Enterprise (Release Candidate)
**Fokus:** Open-Core & kommerzieller Betrieb

- 💼 **Enterprise-Modul**: RBAC/ABAC, Multi-Tenancy, spezielle Konnektoren.
- 🛠 **Monetarisierungs-Infrastruktur**: Lizenzsystem, CI/CD, Helm-Releases.
- 🚀 **Performance-Tuning**: HA-Cluster, Skalierungstests, Backup/Restore.
- 📖 **Benutzer-Dokumentation**: Admin- und User-Guides, Tutorials.
- 🧑‍🤝‍🧑 **Pilotkunden-Support**: Feedback-Zyklus für finale Features.

**Meilenstein:** Release Candidate, monetarisierbar trotz „Experimental“-Status.

---

### v0.6.0 – Observability & DevOps
**Fokus:** Monitoring, CI/CD, Deployment-Optimierung

- 📊 **Observability-Stack**: Prometheus, Grafana, OpenTelemetry (Tracing + Metriken).
- 🛠 **DevOps-Tooling**: GitHub Actions/GitLab CI für Tests, Builds, Releases.
- 🐳 **Container Registry**: automatisiertes Build & Push für Docker/Helm.
- 🧩 **Staging-Cluster**: Dediziertes Test-Deployment für Release-Kandidaten.
- 📂 **Konfigurationsmanagement**: Standardisierte `.env`, Secrets-Management, Vault-Integration.

**Meilenstein:** Entwickler- & Operator-Erfahrung professionalisiert.

---

### v0.7.0 – Security & Compliance
**Fokus:** Sicherheit, Rechte, Governance

- 🔐 **Zero-Trust-Policies**: Feingranulare RBAC/ABAC mit OPA + Keycloak.
- 🕵️ **Audit-Trails**: Jede Aktion (Suche, Upload, Plugin, Agent) wird protokolliert.
- 📑 **Compliance-Module**: GDPR/DSGVO & Audit-Exports.
- 🔑 **Secrets-Management**: Rotation, Encryption at Rest, Secure Defaults.
- 🛡 **Penetration Testing** (inkl. Kali-Plugins) für Schwachstellenprüfung.

**Meilenstein:** Enterprise-Ready Security-Layer.

---

### v0.8.0 – Scaling & Federation
**Fokus:** Verteilte Deployments, Federation

- ⚡ **HA-Cluster** für OpenSearch, Neo4j, Postgres (Replication, Failover).
- 🌍 **Federation**: Mehrere InfoTerminal-Instanzen können Daten/Graphen synchronisieren.
- ☁️ **Hybrid/Cloud Support**: Kubernetes Operator, Helm Charts mit Multi-Cluster-Support.
- 📦 **Data Lake Integration**: S3/MinIO-Unterstützung für Archivierung großer Datenmengen.
- 🔄 **Async Pipelines**: Kafka/NiFi für Event-basierte Datenflüsse.

**Meilenstein:** Plattform skaliert horizontal und funktioniert in verteilten Umgebungen.

---

### v0.9.0 – Final Hardening & User Experience
**Fokus:** Letzte Vorbereitungen für 1.0

- 🎨 **UX-Politur**: Endgültiges UI-Design, konsistentes Styling, Dark/Light Mode.
- 🧪 **End-to-End QA**: Automatisierte Integrationstests aller Kern-Usecases.
- 🧑‍🤝‍🧑 **User Onboarding**: Guided Setup, Wizards, Demo-Daten verbessert.
- 📚 **Docs Freeze**: Alle Endnutzer-/Admin-Dokumente finalisieren.
- 🚀 **Release Candidate 2**: Feature-Freeze, nur noch Bugfixes & Security-Patches.

**Meilenstein:** Plattform ist funktionsvollständig, stabil und bereit für v1.0.

---

### v1.0.0 – Production Ready
**Fokus:** Sicherheit, Stabilität, Vollständigkeit

- 🔐 **Security Hardening**: TLS, sichere Defaults, regelmäßige Audits.
- 👥 **Multi-Tenancy**: finale Umsetzung mit Policies & Mandantentrennung.
- 📊 **Observability**: SLI/SLO-Dashboards, Monitoring, Incident-Runbooks.
- 💾 **Betrieb**: vollständige Backup-/Restore-Routinen, HA-Setup.
- 📚 **Dokumentation**: Installationshandbuch, Migrationspfade, Onboarding.
- 🌍 **Community**: Forum/Discord + Contributor Guidelines.

**Meilenstein:** Offiziell „Production Ready“ – stabil, sicher, erweiterbar.

---

## 📆 Hinweis
- Zeitrahmen flexibel – Meilensteine sind *feature-driven*, nicht kalendarisch fix.
- Priorität: **Funktionalität → Usability → Stabilität → Security → Monetarisierung**.

---

✍️ *Letzte Aktualisierung: September 2025*
