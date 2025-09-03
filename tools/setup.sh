# InfoTerminal Frontend Modernisierung - Schnellstart

# 1. Dependencies installieren
cd apps/frontend
npm install @tailwindcss/forms @tailwindcss/typography @tailwindcss/line-clamp
npm install @headlessui/react @heroicons/react # Optional für erweiterte Components

# 2. Ordnerstruktur erweitern
mkdir -p src/components/ui
mkdir -p src/components/layout
mkdir -p src/lib

# 3. Backup der wichtigsten bestehenden Dateien
cp pages/index.tsx pages/index.tsx.backup
cp pages/search.tsx pages/search.tsx.backup  
cp pages/docs/[id].tsx pages/docs/[id].tsx.backup
cp pages/graphx.tsx pages/graphx.tsx.backup
cp src/components/layout/Header.tsx src/components/layout/Header.tsx.backup

# 4. Neue Tailwind Config erstellen (verwende das bereitgestellte tailwind.config.js)

# 5. Design System Files erstellen
# - src/lib/theme.ts
# - src/components/layout/DashboardLayout.tsx

# 6. Neue Pages erstellen/ersetzen (verwende die bereitgestellten Komponenten)

# 7. Build testen
npm run build

# 8. Development Server starten
npm run dev

# 9. Tests durchführen
npm run test
npm run e2e

# 10. Linting und Formatierung
npm run lint
npm run typecheck

# Optional: Screenshots für Visual Regression Tests
npx playwright test --update-snapshots