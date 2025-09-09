# Architecture

## Final Architecture (v1.0)
![Final Architecture v1.0](final_architecture_v1.png)

### How to read this diagram
1. **Flows von oben nach unten:** Datenquellen → NiFi Ingest → Processing/Storage → Verification → Intelligence Packs → Frontend/Dossiers.
2. **Seitliche Pfeile:** zeigen **Pipeline-Sequenzen** (z. B. Claim → Evidence → RTE → Geo/Temporal/Media → Aggregation).
3. **Farb-Codierung:**
   - Grün: **Quellen**
   - Orange: **Ingest (NiFi)**
   - Blau: **Processing/Storage (APIs/DBs)**
   - Rosa: **Verification-Module**
   - Gelb: **Intelligence Packs (Beyond Gotham)**
   - Hellblau: **Security**
   - Hellgrün: **Frontend/Collaboration**
   - Violett: **Dossier-Templates & Observability**
4. **Presets/Profiles** beeinflussen **Security-Defaults** und **Frontend-Ansichten** (Pfeile zwischen den Ebenen).
5. **Release-Legende (unten):** ordnet Module den Meilensteinen v0.2, v0.3, v0.5, v1.0 zu.
