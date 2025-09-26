# Frontend Linting & Type Safety

This app enforces ESLint + TypeScript checks during builds.

## Quick commands

- Run lints: `cd apps/frontend && pnpm lint`
- Auto-fix (where safe): `pnpm lint:fix`
- Typecheck: `pnpm typecheck`
- Strict build (lint + typecheck + build): `pnpm build:strict`

## Repository helper

Use the idempotent helper to generate reports and optionally apply fixes:

```
DRY_RUN=1 ./scripts/fix_frontend_lints.sh     # default, no changes
DRY_RUN=0 ./scripts/fix_frontend_lints.sh     # apply eslint --fix
```

Reports are written to `reports/frontend/`.

## Common fixes

- Use `next/link` instead of `<a>` for page navigation.
- Escape quotes in JSX text: use `&quot;` or `&#39;`.
- Prefer `next/image` for images; ensure `alt` is set. Use `alt=""` for decorative images.
- Stabilize hooks: add missing deps or wrap functions with `useCallback`, memoize arrays/objects with `useMemo`.
- Replace direct `URLSearchParams({...})` with a helper like `toSearchParams(...)`.

