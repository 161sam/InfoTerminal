#!/bin/bash
# InfoTerminal Migration Cleanup Script
# Verschiebt fälschlicherweise migrierte Dateien zurück
# Autor: InfoTerminal Development Team
# Version: 1.0.0

set -euo pipefail

# Konfiguration
PROJECT_DIR="/home/saschi/InfoTerminal"
DOWNLOADS_DIR="/home/saschi/Downloads"
INSTALLERS_DIR="$PROJECT_DIR/tools/installers"

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

error() {
    echo -e "${RED}ERROR: $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

info() {
    echo -e "${BLUE}INFO: $1${NC}"
}

main() {
    echo -e "${BLUE}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║            InfoTerminal Migration Cleanup                ║
║     Entfernung von fälschlich migrierten Dateien        ║
╚═══════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"

    info "Starte Cleanup der fälschlich migrierten Dateien..."
    
    # Prüfe ob Installer-Ordner existiert
    if [[ ! -d "$INSTALLERS_DIR" ]]; then
        warning "Installer-Ordner existiert nicht: $INSTALLERS_DIR"
        exit 0
    fi
    
    # Liste der fälschlich migrierten Dateien
    local files_to_restore=(
        "claude-desktop_0.11.4_amd64.deb"
        "docker-desktop-amd64.deb"
        "LM-Studio-0.3.23-3-x64.AppImage"
        "goose_1.0.29_amd64.deb"
        "pia-linux-3.6.2-08398.run"
    )
    
    cd "$INSTALLERS_DIR"
    
    info "Verschiebe persönliche Software zurück nach Downloads..."
    
    for file in "${files_to_restore[@]}"; do
        if [[ -f "$file" ]]; then
            # Prüfe ob Datei bereits in Downloads existiert
            if [[ -f "$DOWNLOADS_DIR/$file" ]]; then
                warning "Datei existiert bereits in Downloads: $file"
                warning "Lösche Duplikat aus tools/installers/"
                rm "$file"
                success "Duplikat entfernt: $file"
            else
                # Verschiebe zurück nach Downloads
                mv "$file" "$DOWNLOADS_DIR/"
                success "Zurück verschoben: $file → Downloads/"
            fi
        else
            info "Datei nicht gefunden (bereits verschoben?): $file"
        fi
    done
    
    # Auch das demo-image.png könnte problematisch sein
    local frontend_assets="$PROJECT_DIR/apps/frontend/public/assets"
    if [[ -f "$frontend_assets/demo-image.png" ]]; then
        warning "Prüfe demo-image.png..."
        info "Falls das ChatGPT-Bild nicht zum Projekt gehört:"
        echo "rm '$frontend_assets/demo-image.png'"
    fi
    
    # Prüfe ob installers-Ordner jetzt leer ist
    if [[ -d "$INSTALLERS_DIR" ]] && [[ -z "$(ls -A "$INSTALLERS_DIR")" ]]; then
        info "Installer-Ordner ist leer, entferne ihn..."
        rmdir "$INSTALLERS_DIR"
        success "Leeren Ordner entfernt: tools/installers/"
    fi
    
    # Git Update
    info "Aktualisiere Git Repository..."
    cd "$PROJECT_DIR"
    
    if git status --porcelain | grep -q .; then
        git add -A
        git commit -m "fix: cleanup migration - remove personal software from project

- Move personal installers back to Downloads
- Remove accidentally migrated binaries from tools/installers/
- Keep only project-relevant files

Files restored to Downloads:
$(printf '- %s\n' "${files_to_restore[@]}")

Cleanup performed by: $(basename "$0") on $(date)"
        success "Git Commit für Cleanup erstellt"
    else
        info "Keine Git-Änderungen für Commit"
    fi
    
    echo ""
    success "✅ Cleanup erfolgreich abgeschlossen!"
    info "Persönliche Software ist wieder in Downloads/"
    info "Nur projekt-relevante Dateien bleiben im InfoTerminal-Ordner"
    
    echo ""
    echo -e "${YELLOW}📋 Was übrig bleibt im Projekt:${NC}"
    echo "✅ Frontend-Komponenten (src/components/*)"
    echo "✅ Theme & Configuration (src/lib/*, tailwind.config.js)"
    echo "✅ Projekt-Tools (tools/setup.sh, tools/env-setup.sh)"
    echo "✅ Dokumentation (docs/dev/frontend_modernization_guide.md)"
    echo "❌ Persönliche Software (zurück in Downloads/)"
}

