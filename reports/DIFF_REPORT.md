# Diff & Merge-Conflict Report

- Zeitpunkt: 2025-09-12T12:44:08+02:00
- Base: `origin/main`
- Analyse von: `169 168`

## PR/Branch Zusammenfassung

### 169

Metadaten:

```json
{"additions":2297,"author":{"id":"U_kgDOC8492g","is_bot":false,"login":"161sam","name":"saschi161"},"baseRefName":"main","changedFiles":41,"deletions":691,"headRefName":"backup/layout-migration-20250912-100731","mergeable":"CONFLICTING","number":169,"title":"backup/layout migration 20250912 100731","url":"https://github.com/161sam/InfoTerminal/pull/169"}
```

- Diff ggü `main`:

```
 apps/frontend/.env.local                           |   11 +
 apps/frontend/.env.local.example                   |    5 -
 apps/frontend/package.json                         |   16 +-
 apps/frontend/pages/_app.tsx                       |   18 +-
 apps/frontend/pages/_document.tsx                  |   35 +
 apps/frontend/pages/analytics.tsx                  |    6 +-
 apps/frontend/pages/apps/[app].tsx                 |   66 --
 apps/frontend/pages/documents/index.tsx            |   42 +-
 apps/frontend/pages/graphx.tsx                     |   34 +-
 apps/frontend/pages/search.tsx                     |   92 +-
 apps/frontend/pages/security.tsx                   |    1 -
 apps/frontend/pages/settings.tsx                   |   10 +-
 apps/frontend/src/App.tsx                          |   26 -
 apps/frontend/src/__tests__/GraphSnippet.test.tsx  |   38 +-
 .../src/components/GraphViewerCytoscape.tsx        |   56 +-
 apps/frontend/src/components/Layout.tsx            |   41 -
 .../src/components/analytics/GraphSnippet.tsx      |   76 +-
 .../src/components/forms/FormComponents.tsx        |   17 +-
 apps/frontend/src/components/layout/AppLayout.tsx  |   19 -
 .../src/components/layout/DashboardLayout.tsx      |   23 +-
 apps/frontend/src/components/layout/Panel.tsx      |  112 ++
 apps/frontend/src/components/layout/Sidebar.tsx    |   32 -
 apps/frontend/src/components/layout/index.ts       |    2 +
 apps/frontend/src/components/upload/UploadBox.tsx  |  109 +-
 apps/frontend/src/hooks/useHealth.ts               |    2 +-
 apps/frontend/src/lib/api.ts                       |  246 ++++-
 apps/frontend/src/pages/ExternalAppPage.test.tsx   |   22 -
 apps/frontend/src/pages/ExternalAppPage.tsx        |   76 --
 apps/frontend/src/pages/Home.tsx                   |   10 -
 apps/frontend/src/routes/appRoutes.ts              |   34 -
 apps/frontend/src/setupTests.ts                    |    1 +
 apps/frontend/src/styles/globals.css               | 1168 +++++++++++++++++++-
 apps/frontend/src/test/setupTests.tsx              |  140 +++
 apps/frontend/test-results/.last-run.json          |    9 +
 apps/frontend/tsconfig.json                        |   10 +-
 apps/frontend/tsconfig.tsbuildinfo                 |    1 +
 apps/frontend/vitest.config.ts                     |   39 +-
 apps/frontend/vitest.setup.ts                      |   65 ++
 package.json                                       |    9 +-
 pnpm-lock.yaml                                     |  236 +++-
 scripts/tailwind_v4_guard.sh                       |   33 +-
 41 files changed, 2297 insertions(+), 691 deletions(-)
```

- Top geänderte Dateien:

```
- apps/frontend/.env.local
- apps/frontend/.env.local.example
- apps/frontend/package.json
- apps/frontend/pages/analytics.tsx
- apps/frontend/pages/apps/[app].tsx
- apps/frontend/pages/_app.tsx
- apps/frontend/pages/documents/index.tsx
- apps/frontend/pages/_document.tsx
- apps/frontend/pages/graphx.tsx
- apps/frontend/pages/search.tsx
- apps/frontend/pages/security.tsx
- apps/frontend/pages/settings.tsx
- apps/frontend/src/App.tsx
- apps/frontend/src/components/analytics/GraphSnippet.tsx
- apps/frontend/src/components/forms/FormComponents.tsx
- apps/frontend/src/components/GraphViewerCytoscape.tsx
- apps/frontend/src/components/layout/AppLayout.tsx
- apps/frontend/src/components/layout/DashboardLayout.tsx
- apps/frontend/src/components/layout/index.ts
- apps/frontend/src/components/layout/Panel.tsx
- apps/frontend/src/components/layout/Sidebar.tsx
- apps/frontend/src/components/Layout.tsx
- apps/frontend/src/components/upload/UploadBox.tsx
- apps/frontend/src/hooks/useHealth.ts
- apps/frontend/src/lib/api.ts
- apps/frontend/src/pages/ExternalAppPage.test.tsx
- apps/frontend/src/pages/ExternalAppPage.tsx
- apps/frontend/src/pages/Home.tsx
- apps/frontend/src/routes/appRoutes.ts
- apps/frontend/src/setupTests.ts
- apps/frontend/src/styles/globals.css
- apps/frontend/src/test/setupTests.tsx
- apps/frontend/src/__tests__/GraphSnippet.test.tsx
- apps/frontend/test-results/.last-run.json
- apps/frontend/tsconfig.json
- apps/frontend/tsconfig.tsbuildinfo
- apps/frontend/vitest.config.ts
- apps/frontend/vitest.setup.ts
- package.json
- pnpm-lock.yaml
- scripts/tailwind_v4_guard.sh
```

### 168

Metadaten:

```json
{"additions":800,"author":{"id":"U_kgDOC8492g","is_bot":false,"login":"161sam","name":"saschi161"},"baseRefName":"main","changedFiles":27,"deletions":539,"headRefName":"reset/frontend-rollback-163-164","mergeable":"CONFLICTING","number":168,"title":"Reset/frontend rollback 163 164","url":"https://github.com/161sam/InfoTerminal/pull/168"}
```

- Diff ggü `main`:

```
 apps/frontend/.env.local                           |  11 +
 apps/frontend/.env.local.example                   |   5 -
 apps/frontend/package.json                         |  16 +-
 apps/frontend/pages/_app.tsx                       |  18 +-
 apps/frontend/pages/apps/[app].tsx                 |  66 ------
 apps/frontend/src/App.tsx                          |  26 ---
 apps/frontend/src/__tests__/GraphSnippet.test.tsx  |  38 ++--
 .../src/components/GraphViewerCytoscape.tsx        |  56 ++---
 .../src/components/analytics/GraphSnippet.tsx      |  76 +++++--
 .../src/components/forms/FormComponents.tsx        |  17 +-
 apps/frontend/src/components/layout/AppLayout.tsx  |  19 --
 apps/frontend/src/components/layout/Sidebar.tsx    |  32 ---
 apps/frontend/src/components/upload/UploadBox.tsx  | 109 ++++++----
 apps/frontend/src/lib/api.ts                       | 199 +++++++++++++----
 apps/frontend/src/pages/ExternalAppPage.test.tsx   |  22 --
 apps/frontend/src/pages/ExternalAppPage.tsx        |  76 -------
 apps/frontend/src/pages/Home.tsx                   |  10 -
 apps/frontend/src/routes/appRoutes.ts              |  34 ---
 apps/frontend/src/setupTests.ts                    |   1 +
 apps/frontend/src/test/setupTests.tsx              | 140 ++++++++++++
 apps/frontend/test-results/.last-run.json          |   9 +
 apps/frontend/tsconfig.json                        |  12 +-
 apps/frontend/tsconfig.tsbuildinfo                 |   1 +
 apps/frontend/vitest.config.ts                     |  36 ++--
 apps/frontend/vitest.setup.ts                      |  65 ++++++
 package.json                                       |   9 +-
 pnpm-lock.yaml                                     | 236 ++++++++++++++++-----
 27 files changed, 800 insertions(+), 539 deletions(-)
```

- Top geänderte Dateien:

```
- apps/frontend/.env.local
- apps/frontend/.env.local.example
- apps/frontend/package.json
- apps/frontend/pages/apps/[app].tsx
- apps/frontend/pages/_app.tsx
- apps/frontend/src/App.tsx
- apps/frontend/src/components/analytics/GraphSnippet.tsx
- apps/frontend/src/components/forms/FormComponents.tsx
- apps/frontend/src/components/GraphViewerCytoscape.tsx
- apps/frontend/src/components/layout/AppLayout.tsx
- apps/frontend/src/components/layout/Sidebar.tsx
- apps/frontend/src/components/upload/UploadBox.tsx
- apps/frontend/src/lib/api.ts
- apps/frontend/src/pages/ExternalAppPage.test.tsx
- apps/frontend/src/pages/ExternalAppPage.tsx
- apps/frontend/src/pages/Home.tsx
- apps/frontend/src/routes/appRoutes.ts
- apps/frontend/src/setupTests.ts
- apps/frontend/src/test/setupTests.tsx
- apps/frontend/src/__tests__/GraphSnippet.test.tsx
- apps/frontend/test-results/.last-run.json
- apps/frontend/tsconfig.json
- apps/frontend/tsconfig.tsbuildinfo
- apps/frontend/vitest.config.ts
- apps/frontend/vitest.setup.ts
- package.json
- pnpm-lock.yaml
```

## Merge-Simulation in Base (`origin/main`)

## Merge-Simulation: `tmp/pr-169` → `origin/main`

- Exit Code: `1` (0=kein Konflikt)
- Konfliktdateien:

```
apps/frontend/package.json
apps/frontend/pages/graphx.tsx
apps/frontend/src/components/GraphViewerCytoscape.tsx
apps/frontend/src/lib/api.ts
apps/frontend/src/routes/appRoutes.ts
apps/frontend/src/setupTests.ts
apps/frontend/tsconfig.json
apps/frontend/vitest.config.ts
pnpm-lock.yaml
```

### Konflikt-Hunks (Ausschnitte)
#### `apps/frontend/package.json`
```diff
    39	<<<<<<< HEAD
    43	=======
    47	>>>>>>> tmp/pr-169
```

#### `apps/frontend/pages/graphx.tsx`
```diff
    26	<<<<<<< HEAD
    29	=======
    32	>>>>>>> tmp/pr-169
```

#### `apps/frontend/src/components/GraphViewerCytoscape.tsx`
```diff
     4	<<<<<<< HEAD
    23	=======
    34	>>>>>>> tmp/pr-169
```

#### `apps/frontend/src/lib/api.ts`
```diff
     1	<<<<<<< HEAD
    32	=======
   234	>>>>>>> tmp/pr-169
```

#### `apps/frontend/src/routes/appRoutes.ts`
```diff
```

#### `apps/frontend/src/setupTests.ts`
```diff
     2	<<<<<<< HEAD
   154	=======
   155	>>>>>>> tmp/pr-169
```

#### `apps/frontend/tsconfig.json`
```diff
    32	<<<<<<< HEAD
    35	=======
    38	>>>>>>> tmp/pr-169
```

#### `apps/frontend/vitest.config.ts`
```diff
     3	<<<<<<< HEAD
    15	=======
    44	>>>>>>> tmp/pr-169
```

#### `pnpm-lock.yaml`
```diff
   154	<<<<<<< HEAD
   157	=======
   160	>>>>>>> tmp/pr-169
  2875	<<<<<<< HEAD
  2878	=======
  2881	>>>>>>> tmp/pr-169
  5741	<<<<<<< HEAD
  5743	=======
  5745	>>>>>>> tmp/pr-169
```


## Merge-Simulation: `tmp/pr-168` → `origin/main`

- Exit Code: `1` (0=kein Konflikt)
- Konfliktdateien:

```
apps/frontend/package.json
apps/frontend/src/components/GraphViewerCytoscape.tsx
apps/frontend/src/lib/api.ts
apps/frontend/src/routes/appRoutes.ts
apps/frontend/src/setupTests.ts
apps/frontend/tsconfig.json
apps/frontend/vitest.config.ts
pnpm-lock.yaml
```

### Konflikt-Hunks (Ausschnitte)
#### `apps/frontend/package.json`
```diff
    39	<<<<<<< HEAD
    43	=======
    47	>>>>>>> tmp/pr-168
```

#### `apps/frontend/src/components/GraphViewerCytoscape.tsx`
```diff
     4	<<<<<<< HEAD
    23	=======
    34	>>>>>>> tmp/pr-168
```

#### `apps/frontend/src/lib/api.ts`
```diff
     1	<<<<<<< HEAD
    32	=======
   185	>>>>>>> tmp/pr-168
```

#### `apps/frontend/src/routes/appRoutes.ts`
```diff
```

#### `apps/frontend/src/setupTests.ts`
```diff
     2	<<<<<<< HEAD
   154	=======
   155	>>>>>>> tmp/pr-168
```

#### `apps/frontend/tsconfig.json`
```diff
    32	<<<<<<< HEAD
    35	=======
    38	>>>>>>> tmp/pr-168
```

#### `apps/frontend/vitest.config.ts`
```diff
     3	<<<<<<< HEAD
    15	=======
    41	>>>>>>> tmp/pr-168
```

#### `pnpm-lock.yaml`
```diff
   154	<<<<<<< HEAD
   157	=======
   160	>>>>>>> tmp/pr-168
  2875	<<<<<<< HEAD
  2878	=======
  2881	>>>>>>> tmp/pr-168
  5741	<<<<<<< HEAD
  5743	=======
  5745	>>>>>>> tmp/pr-168
```


## Cross-Merge Simulation (Stacking)

### Reihenfolge: 169 → 168 (auf Base: `main`)

- Exit Code (B auf A): `128`
- Konfliktdateien:

```
(keine)
```

### Reihenfolge: 168 → 169 (auf Base: `main`)

- Exit Code (A auf B): `128`
- Konfliktdateien:

```
(keine)
```

## Heuristische Risiko-Bewertung

- Hohe Konfliktgefahr bei Dateien:

```
apps/frontend/.env.local
apps/frontend/.env.local.example
apps/frontend/package.json
apps/frontend/pages/_app.tsx
apps/frontend/pages/_document.tsx
apps/frontend/pages/analytics.tsx
apps/frontend/pages/apps/[app].tsx
apps/frontend/pages/documents/index.tsx
apps/frontend/pages/graphx.tsx
apps/frontend/pages/search.tsx
apps/frontend/pages/security.tsx
apps/frontend/pages/settings.tsx
apps/frontend/src/App.tsx
apps/frontend/src/__tests__/GraphSnippet.test.tsx
apps/frontend/src/components/GraphViewerCytoscape.tsx
apps/frontend/src/components/Layout.tsx
apps/frontend/src/components/analytics/GraphSnippet.tsx
apps/frontend/src/components/forms/FormComponents.tsx
apps/frontend/src/components/layout/AppLayout.tsx
apps/frontend/src/components/layout/DashboardLayout.tsx
apps/frontend/src/components/layout/Panel.tsx
apps/frontend/src/components/layout/Sidebar.tsx
apps/frontend/src/components/layout/index.ts
apps/frontend/src/components/upload/UploadBox.tsx
apps/frontend/src/hooks/useHealth.ts
apps/frontend/src/lib/api.ts
apps/frontend/src/pages/ExternalAppPage.test.tsx
apps/frontend/src/pages/ExternalAppPage.tsx
apps/frontend/src/pages/Home.tsx
apps/frontend/src/routes/appRoutes.ts
apps/frontend/src/setupTests.ts
apps/frontend/src/styles/globals.css
apps/frontend/src/test/setupTests.tsx
apps/frontend/test-results/.last-run.json
apps/frontend/tsconfig.json
apps/frontend/tsconfig.tsbuildinfo
apps/frontend/vitest.config.ts
apps/frontend/vitest.setup.ts
package.json
pnpm-lock.yaml
scripts/tailwind_v4_guard.sh
apps/frontend/.env.local
apps/frontend/.env.local.example
apps/frontend/package.json
apps/frontend/pages/_app.tsx
apps/frontend/pages/apps/[app].tsx
apps/frontend/src/App.tsx
apps/frontend/src/__tests__/GraphSnippet.test.tsx
apps/frontend/src/components/GraphViewerCytoscape.tsx
apps/frontend/src/components/analytics/GraphSnippet.tsx
apps/frontend/src/components/forms/FormComponents.tsx
apps/frontend/src/components/layout/AppLayout.tsx
apps/frontend/src/components/layout/Sidebar.tsx
apps/frontend/src/components/upload/UploadBox.tsx
apps/frontend/src/lib/api.ts
apps/frontend/src/pages/ExternalAppPage.test.tsx
apps/frontend/src/pages/ExternalAppPage.tsx
apps/frontend/src/pages/Home.tsx
apps/frontend/src/routes/appRoutes.ts
apps/frontend/src/setupTests.ts
apps/frontend/src/test/setupTests.tsx
apps/frontend/test-results/.last-run.json
apps/frontend/tsconfig.json
apps/frontend/tsconfig.tsbuildinfo
apps/frontend/vitest.config.ts
apps/frontend/vitest.setup.ts
package.json
pnpm-lock.yaml
```

- Besondere Aufmerksamkeit für:
  - apps/frontend/src/components/layout/DashboardLayout.tsx (Layout, Theme, Sidebar)
  - apps/frontend/src/styles/globals.css (Tailwind v4 & Theme-Base)
  - apps/frontend/pages/_document.tsx (pre-hydration theme init)
  - apps/frontend/src/lib/theme-provider.tsx (global theme state)
  - apps/frontend/src/components/layout/Panel.tsx (dark-surface Konsistenz)

