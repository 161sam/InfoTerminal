Act as Codex on server2 for the repo at /home/saschi/InfoTerminal.

Branch policy:
- git fetch --all
- git checkout main && git pull
- git checkout -b codex/docs-dedupe-and-merge || git checkout codex/docs-dedupe-and-merge
- Work ONLY on this branch in this run.

Goals (idempotent):
1) Implement REAL dedup + link-rewrite in scripts/docs_pipeline.py (the current step is a placeholder).
2) Run the pipeline: make docs.dedupe && make docs.analyze (to refresh reports).
3) Fix link/name issues reported by the pipeline (broken_links.md, naming_issues.md).
4) Commit atomic changes with clear messages; push the branch.

Dedup implementation details (update scripts/docs_pipeline.py):
- Input reports:
  - WORK-ON-new_docs/out/duplicates_report.md
  - WORK-ON-new_docs/out/todo_index.md
- Canonical targets (mapping rules):
  * RAG / Retrieval / Pipelines → docs/dev/guides/rag-systems.md
  * Frontend modernization/setup → docs/dev/guides/frontend-modernization.md
  * Preset profiles / personas → docs/dev/guides/preset-profiles.md
  * Flowise agents → docs/dev/guides/flowise-agents.md
  * Operability bits → docs/runbooks/stack.md
  * Strategy/Planning content → docs/dev/roadmap/*.md (keep only high-level; move detailed how-to content to guides)
- For each duplicate section candidate (similarity ≥ 0.88):
  1) Parse file A/B, extract exact section line ranges (start/end) and heading.
  2) Compute a normalized hash of the section to ensure idempotence.
  3) If the section (by hash) is already present at the canonical target, SKIP merge.
  4) Else: append full section 1:1 to the canonical target, with YAML front matter:
     ---
     merged_from:
       - <relative/source.md>#L<start>-L<end>
     merged_at: <UTC-ISO>
     ---
  5) Replace the original source section by a one-line pointer:
     "➡ Consolidated at: ../<target>.md#<heading-anchor>"
     Preserve surrounding structure. Record the exact replaced line span.
  6) Write an entry to WORK-ON-new_docs/out/migration_journal.md:
     - ACTION: merge+link
       SRC: <source.md>#L<start>-L<end>
       DST: <target.md>#<anchor>
       WHY: deduplicate
       DIFF: <hash-original> -> <hash-target>
- After dedup, run a cross-link updater:
  * Validate all relative Markdown links; fix broken anchors to new canonical headings.
  * Update any moved filenames (kebab-case renames); record in journal with ACTION: rename+relink.
- Ensure idempotence:
  * Use content-hash checks before writing.
  * When the exact “pointer line” already exists at source, do nothing.
  * When the merged section (by hash) already exists at target, do not insert duplicates.

Fix lint/tooling notes:
- If "make lint.safe" warned about missing patterns:
  * Update scripts/prettier_safe.list to include *.md under docs/.
  * In scripts/format_safe.sh, ensure xargs path handling is robust; no failure on empty sets.
  * Re-run scripts/format_safe.sh; do not block if prettier not installed; print a friendly hint instead.

Execute:
- make docs.dedupe
- make docs.analyze
- Inspect WORK-ON-new_docs/out/{migration_journal.md,broken_links.md,naming_issues.md}
- If broken links remain, run the updater again until clean.

Git:
- git add scripts/docs_pipeline.py scripts/format_safe.sh scripts/prettier_safe.list Makefile docs/ WORK-ON-new_docs/out/
- git commit -m "docs: implement real dedup + link rewrites with provenance; refresh indices and reports"
- git push -u origin codex/docs-dedupe-and-merge

Output for me:
- Summarize how many sections merged, how many sources replaced by links, and top 10 journal entries.
- Confirm branch name and latest commit hash.
