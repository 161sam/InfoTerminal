# RBAC Frontend Gates (K3)

InfoTerminal normalises authentication claims into four canonical roles:

| Role     | Claim Aliases (examples)                   | Primary Capabilities                                      |
|----------|---------------------------------------------|-----------------------------------------------------------|
| Admin    | `admin`, `administrator`, `superuser`       | Full platform control including Ops tooling and exports.  |
| Ops      | `ops`, `operator`, `operations`, `devops`   | Stack lifecycle actions, plugin execution & maintenance.  |
| Analyst  | `analyst`, `intelligence_analyst`, `investigator` | Analytical tooling (media forensics, dossier exports). |
| Viewer   | `viewer`, `guest`, `read`                   | Read-only access to dashboards & reports.                 |

Role values are extracted from multiple JWT attributes (`roles`, `realm_access.roles`,
`resource_access.account.roles`, `scope`, `scp`, and `X-Roles` headers). All values are
lowercased, split on `:`/`/`/`.` separators, mapped via aliases, deduplicated and
default to `viewer` when no explicit role is present. Permissions strings remain
untouched for fine-grained policies. See the regression tests in
`apps/frontend/tests/oidc-claims-mapping.spec.ts` for concrete claim examples.

## UI feature gates

The frontend enforces explicit role gates for critical actions. Users without access see a
standard notice (`Sie haben keine Berechtigung`) instead of inactive buttons.

| Feature / Surface        | Required Roles    | Behaviour without role |
|--------------------------|-------------------|------------------------|
| Ops settings tab (stacks)| Admin, Ops        | Replacement panel with permission notice. |
| Plugin runner & marketplace controls | Admin, Ops | Toggles/config/test buttons hidden; banner explains missing rights. |
| Video forensics uploads  | Admin, Analyst    | Locked panel with message; uploads blocked. |
| Dossier generation/export| Admin, Analyst    | Generate/export disabled, banner shown. |

The canonical matrix is covered by `apps/frontend/tests/rbac-matrix.spec.ts` to prevent
regressions.

## Status

- ✅ K3 milestone complete – RBAC mapping, UI gating and smoke coverage delivered.
- ✅ Snapshot tests document access expectations per role.
- ℹ️ Permission banners reuse the German copy from product guidelines (`Sie haben keine Berechtigung`).

