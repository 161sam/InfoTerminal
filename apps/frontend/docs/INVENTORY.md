# Frontend Code Inventory & Monolith Analysis

*Generated: September 20, 2025*

## Executive Summary

**Identified 8 major monolith files** that exceed 300-400 LOC targets and require modularization. Total size: **~290 KB** of monolithic code.

## Critical Monoliths (Immediate Action Required)

### 1. **pages/graphx.tsx** - 43.75 KB ⚠️ LARGEST
- **Purpose**: Graph analysis and visualization page
- **Complexity**: Multi-tab interface with 3D/2D graph rendering
- **Dependencies**: Cytoscape, DeckGL, complex state management
- **Import Hotspots**: Dynamic imports for 3D visualization, graph API calls
- **Modularization Priority**: **CRITICAL** - Break into:
  - `GraphVisualizationPanel` (3D/2D rendering)
  - `GraphControlsPanel` (filters, settings)
  - `GraphAnalysisPanel` (analytics, metrics)
  - `GraphExportPanel` (export functionality)

### 2. **pages/agent.tsx** - 37.54 KB ⚠️ HIGH
- **Purpose**: AI Agent dashboard and management
- **Complexity**: Agent status monitoring, chat interface, service management
- **Dependencies**: Agent API services, real-time updates
- **Import Hotspots**: Multiple agent service endpoints
- **Modularization Priority**: **HIGH** - Break into:
  - `AgentDashboardPanel`
  - `AgentChatPanel` 
  - `AgentStatusPanel`
  - `AgentConfigPanel`

### 3. **pages/nlp.tsx** - 35.52 KB ⚠️ HIGH  
- **Purpose**: NLP analysis interface
- **Complexity**: Text processing, analysis results, multiple renderers
- **Dependencies**: NLP service APIs, text processing
- **Import Hotspots**: NLP renderer components
- **Modularization Priority**: **HIGH** - Break into:
  - `NLPInputPanel`
  - `NLPAnalysisPanel`
  - `NLPResultsPanel`

### 4. **pages/entities.tsx** - 34.53 KB ⚠️ HIGH
- **Purpose**: Entity management and exploration
- **Complexity**: Entity CRUD, relationships, detailed views
- **Dependencies**: Entity API, graph connections
- **Import Hotspots**: Entity services, badge components
- **Modularization Priority**: **HIGH** - Break into:
  - `EntityListPanel`
  - `EntityDetailPanel`
  - `EntityRelationshipPanel`

### 5. **pages/collab.tsx** - 31.69 KB ⚠️ MEDIUM
- **Purpose**: Collaboration and team features
- **Complexity**: User management, shared workspaces
- **Dependencies**: Collaboration APIs, user services
- **Import Hotspots**: User management, workspace APIs
- **Modularization Priority**: **MEDIUM** - Break into:
  - `CollaborationPanel`
  - `WorkspacePanel`
  - `TeamManagementPanel`

### 6. **pages/dossier.tsx** - 24.62 KB ⚠️ MEDIUM
- **Purpose**: Dossier creation and management
- **Complexity**: Document compilation, export features
- **Dependencies**: Document APIs, export services
- **Import Hotspots**: Export utilities, document services
- **Modularization Priority**: **MEDIUM** - Break into:
  - `DossierBuilderPanel`
  - `DossierPreviewPanel`
  - `DossierExportPanel`

### 7. **pages/search.tsx** - 21.50 KB ⚠️ MEDIUM
- **Purpose**: Search interface and results
- **Complexity**: Advanced search, filters, result rendering
- **Dependencies**: Search APIs, faceting
- **Import Hotspots**: Search components, filter logic
- **Modularization Priority**: **MEDIUM** - Break into:
  - `SearchInputPanel`
  - `SearchFiltersPanel`
  - `SearchResultsPanel`

### 8. **components/MapPanelEnhanced.tsx** - 21.02 KB ⚠️ MEDIUM
- **Purpose**: Enhanced geographical mapping component
- **Complexity**: Map rendering, data overlays, interactions
- **Dependencies**: Mapping libraries, geospatial data
- **Import Hotspots**: Map rendering engines
- **Modularization Priority**: **MEDIUM** - Break into:
  - `MapRenderer`
  - `MapControls`
  - `MapDataOverlay`

## Well-Structured Components (No Action Needed)

### Components Directory Structure ✅
- **Organized by domain**: analytics, auth, docs, entities, graph, health, layout, search, etc.
- **Good size distribution**: Most components under 5 KB
- **Proper separation**: UI primitives in `/ui`, feature components in domain folders
- **shadcn/ui integration**: Consistent use of Radix-based components

### Successfully Refactored ✅
- **pages/settings.tsx**: 733 LOC → 130 LOC (82% reduction)
  - Extracted `SettingsOverview`, `SettingsTabNavigation`
  - Modular tab system with proper separation

## Import Hotspot Analysis

### High-Traffic Dependencies
1. **UI Components**: `/components/ui/*` - heavily imported across pages
2. **Layout Components**: `DashboardLayout`, `Panel` - used by all pages
3. **API Services**: `/lib/api.ts`, `/lib/endpoints.ts` - core data layer
4. **Navigation**: `/components/navigation/*` - routing and breadcrumbs

### Potential Circular Dependencies
- Monitor graph components importing each other
- Watch for shared state between large pages
- API service interdependencies

## Recommended Modularization Strategy

### Phase 1: Extract Largest Monoliths (Week 1)
1. **graphx.tsx** → Multiple panels
2. **agent.tsx** → Dashboard panels  
3. **nlp.tsx** → Analysis panels

### Phase 2: Complete Remaining Pages (Week 2)
4. **entities.tsx** → Entity management panels
5. **collab.tsx** → Collaboration panels
6. **dossier.tsx** → Dossier panels

### Phase 3: Polish & Components (Week 3)
7. **search.tsx** → Search panels
8. **MapPanelEnhanced.tsx** → Map component modules

## Quality Metrics Target

- **Max file size**: 15 KB per component
- **Max LOC**: 300-400 lines per file
- **Reusability**: Extract 3+ shared panels per monolith
- **Import reduction**: Reduce cross-page dependencies by 50%

## Naming Convention Compliance ✅

**Good**: No marketing terms found (no "enhanced", "advanced", "pro", "v2")
**Exception**: `MapPanelEnhanced.tsx` - should be renamed to `MapPanelComplex.tsx` or similar

## Risk Assessment

- **High**: graphx.tsx refactoring (complex 3D rendering)
- **Medium**: agent.tsx (real-time dependencies)
- **Low**: Other pages (standard CRUD patterns)

---

**Next Steps**: Begin Phase 1 with graphx.tsx modularization as highest priority.
