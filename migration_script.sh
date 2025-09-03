#!/bin/bash
# InfoTerminal File Migration Script
# Verschiebt Frontend-Modernisierung Dateien von Downloads ins Projekt
# Autor: InfoTerminal Development Team
# Version: 1.0.0

set -euo pipefail

# Konfiguration
DOWNLOADS_DIR="/home/saschi/Downloads"
PROJECT_DIR="/home/saschi/InfoTerminal"
FRONTEND_DIR="${PROJECT_DIR}/apps/frontend"
BACKUP_SUFFIX=".backup.$(date +%Y%m%d_%H%M%S)"
LOG_FILE="${PROJECT_DIR}/migration_$(date +%Y%m%d_%H%M%S).log"

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging-Funktion
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}ERROR: $1${NC}" | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    echo -e "${YELLOW}WARNING: $1${NC}" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}SUCCESS: $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}INFO: $1${NC}" | tee -a "$LOG_FILE"
}

# Überprüfungen
check_prerequisites() {
    info "Überprüfe Voraussetzungen..."
    
    if [[ ! -d "$DOWNLOADS_DIR" ]]; then
        error "Downloads-Ordner existiert nicht: $DOWNLOADS_DIR"
    fi
    
    if [[ ! -d "$PROJECT_DIR" ]]; then
        error "Projekt-Ordner existiert nicht: $PROJECT_DIR"
    fi
    
    if [[ ! -d "$FRONTEND_DIR" ]]; then
        error "Frontend-Ordner existiert nicht: $FRONTEND_DIR"
    fi
    
    success "Alle Voraussetzungen erfüllt"
}

# Backup-Funktion
backup_existing_file() {
    local target_file="$1"
    if [[ -f "$target_file" ]]; then
        cp "$target_file" "${target_file}${BACKUP_SUFFIX}"
        warning "Backup erstellt: ${target_file}${BACKUP_SUFFIX}"
    fi
}

# Ordnerstruktur erstellen
create_directory_structure() {
    info "Erstelle Ordnerstruktur..."
    
    local dirs=(
        # Core Ordner
        "src/lib"
        "src/hooks"
        "src/types"
        "src/utils"
        
        # Komponenten-Ordner
        "src/components/ui"
        "src/components/forms"
        "src/components/auth"
        "src/components/charts"
        "src/components/mobile"
        "src/components/health"
        "src/components/layout"
        "src/components/search"
        "src/components/entities"
        "src/components/docs"
        "src/components/upload"
        
        # Styles & Assets
        "src/styles"
        "src/assets"
    )
    
    cd "$FRONTEND_DIR"
    
    for dir in "${dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            success "Ordner erstellt: $dir"
        fi
    done
}

# Hauptmigrationsfunktion
migrate_files() {
    info "Starte Dateimigration..."
    
    cd "$DOWNLOADS_DIR"
    
    # Array für Dateizuordnungen: "source_file:target_path:new_name"
    declare -A file_mappings=(
        # UI Komponenten
        ["command_palette.ts"]="src/components/ui:CommandPalette.tsx"
        ["advanced_data_table.ts"]="src/components/ui:DataTable.tsx"
        ["utility_components.ts"]="src/components/ui:UtilityComponents.tsx"
        ["notification_system.ts"]="src/lib:notifications.tsx"
        
        # Layout & Theme
        ["modern_layout.ts"]="src/components/layout:ModernLayout.tsx"
        ["design_system_theme.ts"]="src/lib:theme.ts"
        ["dark_mode_system.ts"]="src/lib:theme-provider.tsx"
        
        # Mobile
        ["mobile_navigation.ts"]="src/components/mobile:MobileNavigation.tsx"
        
        # Forms & Auth
        ["form_components.ts"]="src/components/forms:FormComponents.tsx"
        ["auth_components.ts"]="src/components/auth:AuthProvider.tsx"
        
        # Charts & Visualisierung
        ["advanced_charts.ts"]="src/components/charts:index.tsx"
        
        # Search & Pages
        ["modern_search_component.ts"]="src/components/search:ModernSearch.tsx"
        ["modern_document_detail.ts"]="src/components/docs:DocumentDetail.tsx"
        ["modern_graph_viewer.ts"]="src/components/entities:GraphViewer.tsx"
        ["modern_dashboard_page.ts"]="pages:index.tsx"
        
        # Konfiguration
        ["tailwind_config.js"]=".:tailwind.config.js"
    )
    
    # Python Scripts (Tools)
    declare -A script_mappings=(
        ["text-sanitizer.py"]="tools:text-sanitizer.py"
        ["quick_start_commands.sh"]="tools:setup.sh"
        ["env-optimized.sh"]="tools:env-setup.sh"
    )
    
    # Tools-Ordner erstellen
    mkdir -p "$PROJECT_DIR/tools"
    
    # Frontend-Dateien verschieben
    for source_file in "${!file_mappings[@]}"; do
        if [[ -f "$source_file" ]]; then
            local mapping="${file_mappings[$source_file]}"
            local target_dir=$(echo "$mapping" | cut -d: -f1)
            local target_name=$(echo "$mapping" | cut -d: -f2)
            local target_path="$FRONTEND_DIR/$target_dir"
            local target_file="$target_path/$target_name"
            
            # Zielordner erstellen falls nicht vorhanden
            mkdir -p "$target_path"
            
            # Backup bei bestehender Datei
            backup_existing_file "$target_file"
            
            # Datei verschieben
            mv "$source_file" "$target_file"
            success "Verschoben: $source_file → $target_dir/$target_name"
        else
            warning "Datei nicht gefunden: $source_file"
        fi
    done
    
    # Script-Dateien verschieben
    for source_file in "${!script_mappings[@]}"; do
        if [[ -f "$source_file" ]]; then
            local mapping="${script_mappings[$source_file]}"
            local target_dir=$(echo "$mapping" | cut -d: -f1)
            local target_name=$(echo "$mapping" | cut -d: -f2)
            local target_path="$PROJECT_DIR/$target_dir"
            local target_file="$target_path/$target_name"
            
            # Backup bei bestehender Datei
            backup_existing_file "$target_file"
            
            # Datei verschieben
            mv "$source_file" "$target_file"
            chmod +x "$target_file"  # Executable machen
            success "Verschoben: $source_file → $target_dir/$target_name"
        else
            warning "Script nicht gefunden: $source_file"
        fi
    done
}

# Workflow-Dateien behandeln
handle_workflow_files() {
    info "Verarbeite Workflow-Dateien..."
    
    cd "$DOWNLOADS_DIR"
    
    # GitHub Workflows
    if [[ -f "AutoGit_CommitAgent_Workflow_FIXED.json" ]]; then
        mkdir -p "$PROJECT_DIR/.github/workflows"
        local workflow_dir="$PROJECT_DIR/.github/workflows"
        
        backup_existing_file "$workflow_dir/auto-commit.yml"
        mv "AutoGit_CommitAgent_Workflow_FIXED.json" "$workflow_dir/auto-commit.json"
        success "GitHub Workflow verschoben"
    fi
    
    # Implementation Guide
    if [[ -f "implementation_guide.md" ]]; then
        local docs_dir="$PROJECT_DIR/docs/dev"
        mkdir -p "$docs_dir"
        
        backup_existing_file "$docs_dir/frontend_modernization_guide.md"
        mv "implementation_guide.md" "$docs_dir/frontend_modernization_guide.md"
        success "Implementation Guide verschoben"
    fi
}

# Spezielle Binärdateien behandeln
handle_binary_files() {
    info "Verarbeite Binär- und Asset-Dateien..."
    
    cd "$DOWNLOADS_DIR"
    
    # Assets Ordner erstellen
    mkdir -p "$FRONTEND_DIR/public/assets"
    mkdir -p "$PROJECT_DIR/tools/installers"
    
    # Installationsdateien
    local installers=(
        "claude-desktop_0.11.4_amd64.deb"
        "docker-desktop-amd64.deb"
        "LM-Studio-0.3.23-3-x64.AppImage"
        "goose_1.0.29_amd64.deb"
        "pia-linux-3.6.2-08398.run"
    )
    
    for installer in "${installers[@]}"; do
        if [[ -f "$installer" ]]; then
            mv "$installer" "$PROJECT_DIR/tools/installers/"
            success "Installer verschoben: $installer"
        fi
    done
    
    # Asset-Dateien
    if [[ -f "ChatGPT Image 2. Aug. 2025, 13_07_21.png" ]]; then
        mv "ChatGPT Image 2. Aug. 2025, 13_07_21.png" "$FRONTEND_DIR/public/assets/demo-image.png"
        success "Asset verschoben: demo-image.png"
    fi
    
    # Systemd Service Files
    if [[ -f "headscale.systemd.service" ]]; then
        mkdir -p "$PROJECT_DIR/deploy/systemd"
        mv "headscale.systemd.service" "$PROJECT_DIR/deploy/systemd/"
        success "Systemd Service verschoben"
    fi
}

# Dependencies prüfen und vorschlagen
suggest_dependencies() {
    info "Prüfe Frontend-Dependencies..."
    
    cd "$FRONTEND_DIR"
    
    # Prüfe package.json
    if [[ -f "package.json" ]]; then
        local missing_deps=()
        
        # Liste der benötigten Dependencies
        local required_deps=(
            "@tailwindcss/forms"
            "@tailwindcss/typography"
            "@tailwindcss/line-clamp"
            "@headlessui/react"
            "@heroicons/react"
            "recharts"
            "lucide-react"
        )
        
        for dep in "${required_deps[@]}"; do
            if ! npm list "$dep" &>/dev/null; then
                missing_deps+=("$dep")
            fi
        done
        
        if [[ ${#missing_deps[@]} -gt 0 ]]; then
            warning "Fehlende Dependencies gefunden:"
            printf '%s\n' "${missing_deps[@]}"
            echo ""
            echo "Installiere mit:"
            echo "npm install ${missing_deps[*]}"
            echo ""
        else
            success "Alle Dependencies bereits installiert"
        fi
    fi
}

# Git Integration
update_git() {
    info "Aktualisiere Git Repository..."
    
    cd "$PROJECT_DIR"
    
    # Git Status prüfen
    if git status &>/dev/null; then
        # Unverfolgte Dateien hinzufügen
        git add -A
        
        # Commit mit detaillierter Nachricht
        local commit_msg="feat: Frontend modernization - migrate components and configurations

- Migrate TypeScript components from Downloads
- Update project structure for modern frontend
- Add theme system and dark mode support
- Integrate mobile navigation and responsive design
- Setup advanced charts and data tables
- Configure authentication components
- Add command palette and notifications
- Update Tailwind configuration

Migration performed by: $(basename "$0") on $(date)"

        if git diff --cached --quiet; then
            info "Keine Änderungen für Git Commit"
        else
            git commit -m "$commit_msg"
            success "Git Commit erstellt"
        fi
    else
        warning "Kein Git Repository gefunden"
    fi
}

# Zusammenfassung erstellen
create_summary() {
    info "Erstelle Migrationszusammenfassung..."
    
    local summary_file="$PROJECT_DIR/MIGRATION_SUMMARY.md"
    
    cat > "$summary_file" << EOF
# InfoTerminal Frontend Migration Summary

**Datum:** $(date)
**Script:** $(basename "$0")
**Log-Datei:** $LOG_FILE

## Migrationsergebnisse

### ✅ Verschobene Dateien

#### UI Komponenten
- CommandPalette.tsx → \`src/components/ui/\`
- DataTable.tsx → \`src/components/ui/\`
- UtilityComponents.tsx → \`src/components/ui/\`

#### Layout & Theme
- ModernLayout.tsx → \`src/components/layout/\`
- theme.ts → \`src/lib/\`
- theme-provider.tsx → \`src/lib/\`

#### Mobile Komponenten
- MobileNavigation.tsx → \`src/components/mobile/\`

#### Forms & Auth
- FormComponents.tsx → \`src/components/forms/\`
- AuthProvider.tsx → \`src/components/auth/\`

#### Charts & Visualisierung
- Charts/index.tsx → \`src/components/charts/\`

#### Konfiguration
- tailwind.config.js → Root-Level

### 🔧 Tools & Scripts
- text-sanitizer.py → \`tools/\`
- setup.sh → \`tools/\`
- env-setup.sh → \`tools/\`

### 📁 Erstellte Ordnerstruktur
\`\`\`
src/
├── components/
│   ├── ui/          # Wiederverwendbare UI-Komponenten
│   ├── forms/       # Form-Komponenten & Validation
│   ├── auth/        # Authentication Provider
│   ├── charts/      # Chart-Komponenten
│   ├── mobile/      # Mobile-spezifische Komponenten
│   ├── layout/      # Layout-Komponenten
│   ├── search/      # Search-Komponenten
│   ├── entities/    # Entity-Viewer
│   ├── docs/        # Dokument-Komponenten
│   └── upload/      # Upload-Komponenten
├── lib/             # Utilities & Provider
├── hooks/           # Custom React Hooks
├── types/           # TypeScript Type Definitionen
└── styles/          # Globale Styles
\`\`\`

## 🚀 Nächste Schritte

1. **Dependencies installieren:**
   \`\`\`bash
   cd apps/frontend
   npm install @tailwindcss/forms @tailwindcss/typography @headlessui/react @heroicons/react
   \`\`\`

2. **App-Level Integration:**
   - \`pages/_app.tsx\` aktualisieren für Provider
   - Environment Variables setzen

3. **Entwicklungsserver starten:**
   \`\`\`bash
   make apps-up
   \`\`\`

4. **Testing:**
   - UI-Komponenten testen
   - Mobile Responsiveness prüfen
   - Dark Mode Funktionalität

## 🔗 Dokumentation
- [Frontend Modernization Guide](docs/dev/frontend_modernization_guide.md)
- [Component Documentation](src/components/README.md)
- [Setup Instructions](tools/setup.sh)

---
**Migration abgeschlossen am:** $(date)
EOF

    success "Zusammenfassung erstellt: $summary_file"
}

# Hauptfunktion
main() {
    echo -e "${BLUE}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║               InfoTerminal File Migration                 ║
║          Frontend Modernization - Phase 1                ║
╚═══════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    log "Migration gestartet von: $(whoami)"
    log "Script-Pfad: $(realpath "$0")"
    
    # Schrittweise Ausführung
    check_prerequisites
    create_directory_structure
    migrate_files
    handle_workflow_files
    handle_binary_files
    suggest_dependencies
    update_git
    create_summary
    
    echo ""
    success "✅ Migration erfolgreich abgeschlossen!"
    info "📋 Log-Datei: $LOG_FILE"
    info "📄 Zusammenfassung: $PROJECT_DIR/MIGRATION_SUMMARY.md"
    
    echo ""
    echo -e "${YELLOW}🚀 Nächste Schritte:${NC}"
    echo "1. cd $FRONTEND_DIR"
    echo "2. npm install @tailwindcss/forms @tailwindcss/typography @headlessui/react"
    echo "3. make apps-up"
    echo "4. Öffne http://localhost:3000"
}

# Script ausführen
main "$@"
