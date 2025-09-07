# 🔐 InfoTerminal Security Blueprint

> Ziel: Robustes Security- & Incognito-Layer für Journalist:innen, Sicherheitsbehörden, Firmen und Forschung.  
> Motto: **Sicherheit, Anonymität, Nachvollziehbarkeit – je nach Modus.**

---

## 🎯 Grundsätze

- **Defense in Depth**: Sicherheit auf Netzwerk-, Speicher-, Auth-, Plugin- und Logging-Ebene.
- **Modus-Schalter**: Nutzer:innen wählen zwischen **Standard**, **Incognito** und **Forensics**.
- **Legal by Design**: robots.txt/ToS respektieren, PII-Redaktion optional.
- **Fail-Safe Defaults**: Egress-Blockade bei Proxy/Tor-Ausfall, niemals „leaken“.

---

## ⚙️ Betriebsmodi

| Modus         | Beschreibung                                   | Logging                       | Netzwerk                     | Speicher        | Zielgruppe          |
| ------------- | ---------------------------------------------- | ----------------------------- | ---------------------------- | --------------- | ------------------- |
| **Standard**  | Normalbetrieb, volle Funktionalität            | Persistent (Loki/Tempo)       | Direkt oder Proxy            | Normal FS       | Forschung           |
| **Incognito** | Keine Spuren, ephemerer Speicher, Tor/VPN only | In-Memory Buffer (no persist) | Nur über Tor/VPN/Proxy-Chain | tmpfs/overlayfs | Journalismus        |
| **Forensics** | Gerichtsfest, maximale Nachvollziehbarkeit     | Immutable Logs, WORM Buckets  | Direkt, voll transparent     | Hash+Sign       | Sicherheitsbehörden |

**UI-Schalter & Env-Flags:**

```bash
IT_MODE={standard|incognito|forensics}
IT_EGRESS={tor|vpn|proxy|tor+vpn}
IT_HTTP_PROXY=...
IT_SOCKS5_PROXY=...
IT_BLOCK_DNS=1
IT_DOH=1
IT_NO_LOG_PERSIST=1
IT_EPHEMERAL_FS=1
```

---

## 🌐 Netzwerk & Anonymität

### Egress-Gateway

- **Tor** (SOCKS5) mit obfs4-Bridges.
- **VPN** (WireGuard/OpenVPN) mit Kill-Switch (iptables/nftables).
- **Proxy-Chains** (Privoxy/Dante).
- **DNS-Härtung**: DoH/DoT oder Tor-DNS, blockiere Port 53.
- **Fail-Closed**: Bricht die Kette → kein Traffic.

### Umsetzung

- Alle Services (NiFi, n8n, Frontend, Plugins) nutzen zentrale Proxy-Umgebungsvariablen.
- NetworkPolicies: kein Direkt-Internet, nur über Egress-Gateway.

---

## 🕵️ Headless-Browser & Scraping

- **Remote Browser Pool** (Playwright/Chromium) in isolierten Containern.
- **Fingerprint-Minimierung**: WebRTC off, Canvas-Leak blocken, konsistente Profile.
- **Cookie-Jars pro Case**.
- **Research-Identities**: UA/Locale/Timezone Profile.
- **Compliance**: robots.txt-Enforcer, Backoff, Quell-Whitelist.

---

## 🔒 Speicher & Kryptografie

- **Incognito-Speicher**: tmpfs/overlayfs, Auto-Wipe nach Session.
- **At-rest Encryption**: Vault/KMS, AES-256 + Envelope.
- **In-transit**: TLS 1.3, mTLS für interne Services.
- **Hashes & Signaturen**: SHA-256 + sigstore/rekor für Forensics.
- **PII-Wächter**: Erkennung & optionale Schwärzung.

---

## 📑 Logging & Audit

- **Standard**: Structured JSON-Logs (Loki), Traces (Tempo).
- **Incognito**: Nur in-memory Ring-Buffer, keine Persistenz.
- **Forensics**: Immutable Audit (WORM Buckets, unveränderbar).
- **UI-Warnungen**: Hinweise, wenn Exporte Metadaten enthalten.

---

## 🧩 Plugins & Tools (Kali, Scraper, Analyzer)

- **Isolations-Stack**: Rootless OCI, seccomp, AppArmor, readonly FS, default **no-net**.
- **Resource Guards**: CPU/Mem Limits, Timeout/Kill, Quotas.
- **Manifest-Policy**: `plugin.yaml` deklariert benötigte CAPs/Netz/Secrets → OPA validiert.
- **Supply-Chain**: SBOM, Cosign Verify, Trivy-Scan in CI.

---

## 👤 Identitäten & Secrets

- **OIDC** mit pseudonymen Rollen (Research-Personas).
- **Secrets** über Vault/Param-Store, nie in Logs.
- **Admin-Härtung**: FIDO2/WebAuthn Hardware-Keys.

---

## 🧭 Rollen-Presets

- **Journalismus**: Incognito Default, Save-Nothing, Tor→VPN, PII-Redaktion.
- **Behörden/Firmen**: Forensics Default, Chain-of-Custody, Immutable Logs.
- **Forschung**: Standard Default, schnelle Umschaltung möglich.

---

## 🚨 Limitierungen

- Website-Fingerprinting/Timing-Korrelation schwer vollständig zu eliminieren.
- Dritte (CDNs/Analytics) können Muster erkennen.
- OPSEC-Fehler der Nutzer\:innen kompromittieren Anonymität.
- Rechtliche Vorgaben & ToS sind verbindlich.

---

## ✅ Tickets (Erweiterung zum TODO-Index)

- **\[SEC-EGRESS-1]** Egress-Gateway Container (Tor+VPN+Proxy), Kill-Switch, DNS-Sinkhole
- **\[SEC-EGRESS-2]** NetworkPolicy: alle Services nur via Egress-Gateway
- **\[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion
- **\[SEC-STORE-1]** Ephemeral FS für Incognito Sessions
- **\[SEC-STORE-2]** Vault-Integration + per-Tenant Keys
- **\[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte
- **\[SEC-BROWSER-1]** Remote Browser Pool + WebRTC-Off + Cookie-Jar pro Case
- **\[SEC-BROWSER-2]** Identity-Profiles (UA/Locale/Timezone)
- **\[SEC-BROWSER-3]** robots.txt-Enforcer + Whitelist
- **\[SEC-AUDIT-1]** Dual-Plane Logging: persistent vs. in-memory
- **\[SEC-SBX-1]** gVisor/Kata/Firecracker für Plugins, default no-net
- **\[SEC-SBX-2]** OPA-Validierung der `plugin.yaml`
- **\[SEC-SBX-3]** SBOM/Cosign/Trivy in CI

---

## 🚀 Nächste Schritte

1. Implementiere **Egress-Gateway + DNS-Härtung** (SEC-EGRESS-1..3).
2. Baue **Incognito-Speicher + Logging** (SEC-STORE-1 + SEC-AUDIT-1).
3. Sandbox für **Kali-Plugins** (SEC-SBX-1..3).
4. UI-Integration (Modus-Schalter + Warnungen).

---

## 👉 Dieser `SECURITY-BLUEPRINT.md` muss noch um **Compose/K8s Snippets für den Egress-Gateway (Tor+VPN+Proxy-Chain, Fail-Closed)** erweitert werden
