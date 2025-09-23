# Architecture Overview - InfoTerminal Frontend

## Overview
Architectural analysis of the InfoTerminal frontend codebase focusing on module organization, patterns, and system design.

**Generated:** 2025-09-20  
**Scope:** Phase 1 Analysis - Frontend Audit

---

## System Architecture

### Application Framework
- **Framework:** Next.js 14 (Pages Router)
- **Runtime:** React 18.3.1 with TypeScript 5.9.2
- **Styling:** Tailwind CSS 4.1.12
- **State Management:** React Context + Local State
- **UI Library:** Custom components + partial shadcn/ui

### Layout Hierarchy

```
App (_app.tsx)
├── NotificationProvider
├── AuthProvider  
├── ThemeProvider
└── ToastProvider
    └── Page Components
        ├── DashboardLayout (main wrapper)
        ├── PageLayout (content pages)
        └── TabbedPageLayout (multi-tab pages)
```

---

## Module Architecture

### 1. Provider Layer

#### Authentication (`src/components/auth/`)
- **AuthProvider.tsx** - Core auth context with user state management
- **Pattern:** Context-based state with localStorage persistence
- **Features:** Login/logout, token management, user switching

#### Theme System (`src/lib/theme-provider.tsx`)
- **Purpose:** Dark/light mode management
- **Integration:** Tailwind CSS variables + context
- **Storage:** localStorage with system preference detection

#### Notifications (`src/lib/notifications.tsx`)
- **Purpose:** System-wide notification state
- **Pattern:** Context + reducer for notification queue
- **UI:** Toast components for display

### 2. Layout Architecture

#### Primary Layouts
- **DashboardLayout** - Main application wrapper with header, sidebar
- **PageLayout** - Standard content pages
- **TabbedPageLayout** - Multi-tab interfaces (settings, graphx, agent)

#### Header System (`src/components/layout/Header.tsx`)
- **Navigation:** Main nav items with dropdown for overflow
- **User Management:** Avatar, dropdown menu, login button
- **Health Status:** Global service health indicator
- **Mobile:** Hamburger menu integration

#### Mobile Navigation (`src/components/mobile/MobileNavigation.tsx`)
- **Pattern:** Full-screen overlay + bottom tab bar
- **Features:** Expandable sub-items, notification badges
- **Responsive:** Hidden on desktop, primary on mobile

### 3. Navigation System

#### Configuration (`src/components/navItems.ts`)
```typescript
export type NavItem = {
  key: string;
  name: string;
  href: string;
  icon: LucideIcon;
  featureFlag?: string;
  category?: "core" | "analysis" | "intelligence" | "management";
  subItems?: NavItem[];
};
```

#### Navigation Functions
- `getMainNavItems()` - Primary navigation (header/mobile)
- `getCompactNavItems()` - Bottom tab navigation (mobile)
- `getNavItemsByCategory()` - Grouped navigation
- `isEnabled()` - Feature flag checking

#### Current Navigation Order
1. Dashboard (/)
2. Search (/search)  
3. Graph Analysis (/graphx) - with sub-items
4. NLP Analysis (/nlp)
5. AI Agents (/agent) - with sub-items
6. Verification (/verification)
7. Documents (/documents)
8. Entities (/entities)
9. Analytics (/analytics)
10. Data Sources (/data)
11. Collaboration (/collab)
12. Plugins (/plugins)
13. Settings (/settings) - footer only

---

## Component Patterns

### 1. UI Primitives

#### Dialog System (`src/components/ui/dialog.tsx`)
- **Pattern:** Portal-based modals with context management
- **Implementation:** Custom React Portal + React Context
- **Current State:** Good foundation, needs viewport guards
- **Usage:** LoginModal, confirmation dialogs

#### Form Components
- **Button:** CVA-based variants, consistent styling
- **Field:** Wrapper with label, validation states
- **Input/Select/Textarea:** Styled form controls
- **Switch/Checkbox:** Toggle components

### 2. Feature Components

#### Authentication UI
- **LoginModal.tsx** - Main login interface with dual modes
- **HeaderUserButton.tsx** - User avatar + dropdown menu  
- **Pattern:** Modal-based login, header integration

#### Settings Architecture
- **settings.tsx** - Main page with tab navigation
- **SecurityPanel.tsx** - Security configuration component
- **UserManagementPanel.tsx** - User administration (reusable)
- **Pattern:** Tab-based with URL state management

#### Graph Visualization
- **GraphExplorer.tsx** - Main graph interface
- **AnalysisPanel.tsx** - Graph analytics sidebar
- **Pattern:** Multiple visualization libraries (Cytoscape, deck.gl)

### 3. Data Flow Patterns

#### API Integration
- **Endpoints:** Centralized configuration in `/lib/endpoints.ts`
- **HTTP Client:** Custom fetch wrapper in `/lib/api.ts`
- **Health Monitoring:** Service status checking in `/hooks/useHealth.ts`

#### State Management
- **Local State:** React useState for component state
- **Global State:** React Context for auth, theme, notifications
- **URL State:** Next.js router for navigation and tab state
- **Persistence:** localStorage for settings, tokens

---

## Feature Integration

### 1. Consolidated Pages

#### Graph Analysis (/graphx)
- **Structure:** Tabbed interface with sub-routes
- **Tabs:** Graph View, 3D Visualization, ML Analytics
- **Integration:** Multiple visualization engines

#### NLP Analysis (/nlp)  
- **Structure:** Domain-based routing
- **Domains:** General, Legal, Documents, Ethics, Forensics
- **Pattern:** Dynamic routing with domain filtering

#### AI Agents (/agent)
- **Structure:** Two-tab interface
- **Tabs:** Agent Interaction (chat), Agent Management (admin)
- **Features:** Multi-agent support, capability system

### 2. Settings Integration
- **Pattern:** Single page with tab navigation
- **Tabs:** Endpoints, Operations, Gateway, Appearance, Notifications, Security, User Management, About
- **State:** URL-based tab state with query parameters
- **Persistence:** localStorage for configuration

### 3. User Management
- **Integration:** Header button → LoginModal → UserManagementPanel
- **Reusability:** UserManagementPanel used in both modal and settings
- **Authentication:** Context-based with multiple user support

---

## Build & Development Architecture

### TypeScript Configuration
- **Base:** Next.js TypeScript template
- **Strict Mode:** Enabled with comprehensive type checking
- **Paths:** Alias support (@/ prefix)

### Testing Strategy
- **Unit Tests:** Vitest with JSX Testing Library
- **E2E Tests:** Playwright for user workflows
- **Coverage:** Istanbul coverage reports

### Development Tools
- **Linting:** ESLint 9 with custom rules
- **Formatting:** Prettier with consistent config
- **Git Hooks:** Husky for pre-commit validation
- **Hot Reload:** Next.js development server

---

## Service Integration

### Backend Communication
- **Pattern:** API routes in `/pages/api/` as proxies
- **Authentication:** Header-based token passing
- **Error Handling:** Consistent error response format
- **Health Checks:** Per-service health monitoring

### External Services
- **Search:** OpenSearch/Elasticsearch integration
- **Graph:** Neo4j database for relationships
- **NLP:** Python-based processing services
- **Authentication:** OIDC/OAuth2 gateway integration

---

## Performance Architecture

### Code Splitting
- **Pages:** Automatic route-based splitting
- **Components:** Dynamic imports where appropriate
- **Libraries:** Heavy libraries (deck.gl, cytoscape) lazy-loaded

### Optimization
- **Images:** Next.js Image component optimization
- **Bundling:** Webpack optimizations via Next.js
- **Caching:** Browser caching for static assets
- **Prefetching:** Link prefetching for navigation

---

## Security Architecture

### Authentication
- **Pattern:** JWT tokens with refresh mechanism
- **Storage:** httpOnly cookies preferred, localStorage fallback
- **Multi-user:** Support for user switching
- **Permissions:** Role-based access control

### Content Security
- **CSP:** Content Security Policy headers
- **Sanitization:** Input sanitization for all forms
- **HTTPS:** Enforced in production
- **Incognito Mode:** Privacy features for sensitive data

---

## Known Architectural Issues

### 1. Component Duplication
- **Settings:** Multiple UserManagement components
- **Navigation:** Inconsistent nav item implementations
- **Dialog:** Mixed modal patterns

### 2. State Management Complexity
- **Authentication:** Multiple auth patterns coexist
- **Settings:** Mixed localStorage/context patterns
- **Theme:** Partial Tailwind variable integration

### 3. Import Dependencies
- **Circular Dependencies:** Some module circular references
- **Bundle Size:** Heavy libraries not always code-split
- **Type Imports:** Inconsistent type-only imports

---

## Recommendations

### Immediate Consolidation
1. **Dialog System** - Standardize on portal-based modals
2. **User Management** - Single reusable component
3. **Navigation** - Consolidate nav item functions
4. **Settings** - Single tab interface pattern

### Architecture Improvements
1. **State Management** - Consider Zustand for complex state
2. **Component Library** - Complete shadcn/ui migration
3. **Error Boundaries** - Implement error boundary components
4. **Loading States** - Standardize loading patterns

### Performance Optimizations
1. **Code Splitting** - Lazy load heavy visualization components
2. **Bundle Analysis** - Remove unused dependencies
3. **Cache Strategy** - Implement service worker for offline capability
4. **Image Optimization** - Optimize all asset loading
