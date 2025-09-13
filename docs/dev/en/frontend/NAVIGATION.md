# Frontend Navigation

The sidebar is driven by `NAV_ITEMS` in `apps/frontend/src/components/navItems.ts`. The list defines the order: *Agent* follows **Graph**, *NLP* follows **Documents**. Visibility is gated by the `NEXT_PUBLIC_FEATURE_AGENT` and `NEXT_PUBLIC_FEATURE_NLP` flags (unset ⇒ enabled in dev).

Both desktop and mobile menus consume the same filtered items and the mobile drawer closes on navigation.
