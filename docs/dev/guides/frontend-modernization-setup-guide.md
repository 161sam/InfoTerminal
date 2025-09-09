---
merged_from:
  - docs/dev/Frontend-Modernisierung_Setup-Guide.md#L1-L472
merged_at: 2025-09-09T13:14:27.278990Z
---
<!-- markdownlint-disable MD013 -->

# 🚀 InfoTerminal Frontend Modernisierung - Kompletter Setup Guide

➡ Consolidated at: frontend-modernization.md#berblick-der-modernisierung
### ✨ Neue Features & Verbesserungen

- **🎨 Professionelles Design System** - Konsistente Farben, Typography, Spacing
➡ Consolidated at: frontend-modernization.md#dark-mode-support-automatisches-theme-switching-system-sync
- **Tailwind CSS** - Utility-first Styling
- **Component Architecture** - Wiederverwendbare Komponenten
- **State Management** - React Hooks + Context
- **Error Boundaries** - Graceful Error Handling
- **Loading States** - Skeleton Loaders + Spinners
- **Accessibility** - WCAG-konform
- **SEO Optimiert** - Meta Tags + Structured Data

## 🔧 Installation & Setup

### 1. Vorbereitung

```bash
cd apps/frontend
➡ Consolidated at: frontend-modernization.md#
npm install @tailwindcss/forms @tailwindcss/typography @tailwindcss/line-clamp

➡ Consolidated at: frontend-modernization.md#optional-advanced-components
# Development Dependencies
npm install --save-dev @types/node
➡ Consolidated at: frontend-modernization.md#section
➡ Consolidated at: frontend-modernization.md#bash
➡ Consolidated at: frontend-modernization.md#mkdir-p-src-lib
mkdir -p src/components/layout
mkdir -p src/components/search
mkdir -p src/components/entities
mkdir -p src/components/docs
➡ Consolidated at: frontend-modernization.md#mkdir-p-src-components-upload
2. **Theme Provider** → `src/lib/theme-provider.tsx`
3. **Notifications** → `src/lib/notifications.tsx`
4. **Command Palette** → `src/components/ui/CommandPalette.tsx`
5. **Real-time** → `src/lib/realtime.tsx`

#### Layout & Navigation

1. **Dashboard Layout** → `src/components/layout/DashboardLayout.tsx`
2. **Mobile Navigation** → `src/components/mobile/MobileNavigation.tsx`
3. **Settings Panel** → `src/components/mobile/SettingsPanel.tsx`
➡ Consolidated at: frontend-modernization.md#
1. **Form Components** → `src/components/forms/FormComponents.tsx`
2. **Authentication** → `src/components/auth/AuthProvider.tsx`
➡ Consolidated at: frontend-modernization.md#
1. **Data Table** → `src/components/ui/DataTable.tsx`
2. **Charts** → `src/components/charts/index.tsx`
➡ Consolidated at: frontend-modernization.md#3-error-boundary-src-components-ui-errorboundary-tsx
1. **Homepage** → `pages/index.tsx`
2. **Search** → `src/components/search/ModernSearch.tsx`
3. **Document Detail** → `pages/docs/[id].tsx`
4. **Graph Viewer** → `pages/graphx.tsx`

#### Configuration
➡ Consolidated at: frontend-modernization.md#
```javascript
// tailwind.config.js - Vollständig ersetzen
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
➡ Consolidated at: frontend-modernization.md#pages-js-ts-jsx-tsx-mdx
          50: "#f0f9ff",
          100: "#e0f2fe",
          500: "#0ea5e9",
          600: "#0284c7",
          700: "#0369a1",
          900: "#0c4a6e",
        },
        // ... weitere Farben
      },
➡ Consolidated at: frontend-modernization.md#fontfamily
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
  ],
};
➡ Consolidated at: frontend-modernization.md#
```typescript
import '@/styles/globals.css'
import { Inter } from 'next/font/google'
import { ThemeProvider } from '../src/lib/theme-provider'
import { NotificationProvider } from '../src/lib/notifications'
➡ Consolidated at: frontend-modernization.md#import-commandpaletteprovider-from-src-components-ui-commandpalette
const inter = Inter({ subsets: ['latin'] })

export default function App({ Component, pageProps }: any) {
  return (
➡ Consolidated at: frontend-modernization.md#div-classname-inter-classname
                <CommandPaletteProvider>
                  <Component {...pageProps} />
                </CommandPaletteProvider>
              </NotificationProvider>
            </RealtimeProvider>
➡ Consolidated at: frontend-modernization.md#authprovider

➡ Consolidated at: frontend-modernization.md#environment-variables
# .env.local
➡ Consolidated at: frontend-modernization.md#next-public-search-api-http-localhost-8001
➡ Consolidated at: frontend-modernization.md#next-public-nlp-api-http-localhost-8003

## 🎯 Schritt-für-Schritt Migration

### Phase 1: Design System (Tag 1-2)

- ✅ Theme System installieren
- ✅ Tailwind Config updaten
- ✅ Dark Mode implementieren
- ✅ Basic Layout testen

➡ Consolidated at: frontend-modernization.md#phase-2-navigation-layout-tag-3-4
### Phase 3: Core Components (Tag 5-7)

- ✅ Form System implementieren
- ✅ Data Table hinzufügen
- ✅ Charts integrieren
- ✅ Error Boundaries einbauen
➡ Consolidated at: frontend-modernization.md#section

### Phase 5: Pages Migration (Tag 11-12)

- ✅ Homepage modernisieren
- ✅ Search Page übarbeiten
- ✅ Document Detail optimieren
➡ Consolidated at: frontend-modernization.md#graph-viewer-erweitern
- ✅ Browser Compatibility

## 🧪 Testing & Validation

### Development Testing

➡ Consolidated at: frontend-modernization.md#bash

➡ Consolidated at: frontend-modernization.md#type-check
➡ Consolidated at: frontend-modernization.md#unit-tests
# E2E Tests
➡ Consolidated at: frontend-modernization.md#npm-run-e2e
- [ ] **Mobile Navigation** - Hamburger Menu + Bottom Tabs
- [ ] **Dark/Light Mode** - Toggle funktioniert
- [ ] **Command Palette** - Cmd+K öffnet Palette
- [ ] **Search Functionality** - Faceted Search + Results
- [ ] **Form Validation** - Error States + Success
- [ ] **Real-time Updates** - WebSocket Connection
➡ Consolidated at: frontend-modernization.md#notifications-toast-messages
### Build Optimizations

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,
➡ Consolidated at: frontend-modernization.md#swcminify-true

### Performance Checklist

- [ ] **Bundle Size** < 500KB gzipped
- [ ] **First Contentful Paint** < 1.8s
- [ ] **Largest Contentful Paint** < 2.5s
- [ ] **Cumulative Layout Shift** < 0.1
➡ Consolidated at: frontend-modernization.md#first-input-delay-100ms

➡ Consolidated at: frontend-modernization.md#performance-monitoring
  enableErrorTracking: true,
};
```

### Key Metrics zu verfolgen
➡ Consolidated at: frontend-modernization.md#section
  },
➡ Consolidated at: frontend-modernization.md#
// src/components/ui/Button.tsx
export const buttonVariants = {
  primary: "bg-primary-600 hover:bg-primary-700",
  secondary: "bg-gray-600 hover:bg-gray-700",
  // Weitere Varianten
};
➡ Consolidated at: frontend-modernization.md#

```bash
➡ Consolidated at: frontend-modernization.md#typescript-errors
# Dependencies
➡ Consolidated at: frontend-modernization.md#rm-rf-node-modules-package-lock-json
rm -rf .next
```

➡ Consolidated at: frontend-modernization.md#3-performance-issues
# Bundle Analyzer
➡ Consolidated at: frontend-modernization.md#npm-install-save-dev-next-bundle-analyzer
➡ Consolidated at: frontend-modernization.md#4-mobile-issues
2. **Style Guide** - Design System Regeln
➡ Consolidated at: frontend-modernization.md#3-api-reference-hook-utility-dokumentation

1. **Figma Components** - Design System für Designer
➡ Consolidated at: frontend-modernization.md#2-brand-guidelines-farben-typography-spacing
## 🎯 Success Metrics

➡ Consolidated at: frontend-modernization.md#vor-der-modernisierung-baseline
- ❌ Keine Konsistenz im Design
- ❌ Grundlegende Funktionalität nur

➡ Consolidated at: frontend-modernization.md#nach-der-modernisierung-ziel
- [ ] **Cross-Browser getestet** (Chrome, Firefox, Safari, Edge)
- [ ] **User Acceptance Testing** abgeschlossen
- [ ] **Documentation aktualisiert**
- [ ] **Deployment Pipeline getestet**
- [ ] **Monitoring Setup** aktiv
- [ ] **Rollback Plan** definiert
➡ Consolidated at: frontend-modernization.md#section
➡ Consolidated at: frontend-modernization.md#herzlichen-gl-ckwunsch
### Was Sie erreicht haben

➡ Consolidated at: frontend-modernization.md#10x-bessere-user-experience
- 🔧 **Wartbarer Code**
- 🛡️ **Enterprise Security**
- 📊 **Advanced Features**

Die Modernisierung positioniert InfoTerminal als **professionelle Intelligence-Plattform**, die sowohl für kleine Teams als auch große Enterprise-Umgebungen geeignet ist.
