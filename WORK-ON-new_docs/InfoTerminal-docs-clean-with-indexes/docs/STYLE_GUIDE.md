# Documentation Style Guide

English is the primary language for all documentation.

---

## Language

- Write all main content in English.
- German may be added as an optional appendix under a `DE Notes` section separated by `---`.

## Tone

- Use a concise, imperative style, especially in runbooks.

## Markdown Conventions

- Use `#`-style headings with a blank line after.
- Fenced code blocks with language identifiers.
- Tables should use pipes and alignments.
- Wrap lines at 120 characters when possible.

## Internationalization (i18n) Policy

- **User Docs:** German (DE). File naming with numeric prefixes where applicable, e.g., `01-einfuehrung.md`.
- **Developer & API Docs:** English (EN). Use lowercase-kebab-case, e.g., `frontend-modernization.md`.
- **Cross-linking:** Always link across languages to the canonical counterpart where available.
- **Filenames:** ASCII only (umlauts to `ae/oe/ue`, `ß` to `ss`), avoid spaces & special chars.
