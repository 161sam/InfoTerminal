# Ops GUI

Die Ops-GUI ermöglicht das Starten, Stoppen und Überwachen vordefinierter Docker-Stacks. Aktionen sind nur verfügbar, wenn `IT_OPS_ENABLE=1` gesetzt ist und der angemeldete Nutzer die Rolle `admin` oder `ops` besitzt.

## Funktionen
- Auflistung erlaubter Stacks (`/api/ops/stacks`)
- Statusabfrage und Logs je Stack
- Start, Stop, Restart und Scale einzelner Services

Alle Aktionen werden auditiert. In Produktivumgebungen sollte der Zugriff nur über VPN/SSO erfolgen. Der Docker-Socket erlaubt privilegierte Operationen.
