# Ops GUI

Die Ops-GUI ist unter `/settings?tab=ops` eingebunden (nur Rollen `admin` & `ops`). Sie ermöglicht:

- Anzeigen zulässiger Stacks (`/api/ops/stacks`).
- Start/Stop/Restart von Compose-Services.
- Abruf der letzten Logzeilen je Service.
- Anzeigen definierter Runbooks und Health-Indikatoren.

Voraussetzungen: `IT_OPS_ENABLE=1` und Zugriff auf den Docker-Socket. Alle Aktionen werden auditiert; in produktiven Setups nur über abgesicherte Verbindungen (VPN/SSO) verwenden.
