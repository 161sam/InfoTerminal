# Plugins verwalten

Unter `/plugins` lassen sich installierte Plugins einsehen und verwalten. Jede Karte zeigt Name, Version und Anbieter des Plugins.

## Aktivieren/Deaktivieren

Mit dem Schalter kann ein Plugin pro Benutzer aktiviert oder deaktiviert werden. Administratoren können Einstellungen global setzen.

## Konfiguration

Nicht sensible Optionen werden über ein Formular gespeichert. Geheimnisse wie Tokens oder Passwörter müssen weiterhin über Umgebungsvariablen oder einen Vault hinterlegt werden.

## Health

Über den Health‑Check wird der Zustand eines Plugins geprüft. Bei Problemen erscheint eine Warnung.

## Iframe‑Fallback

Einige Plugins stellen eine eigene Oberfläche bereit. Sollte die Einbettung per Iframe scheitern, wird ein Link angeboten, um die Seite in einem neuen Tab zu öffnen.
