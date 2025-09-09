# Docs Pipeline

This utility script wraps common maintenance tasks for the documentation tree.

## Usage

Run the pipeline via make targets:

```sh
make docs.analyze       # generate analysis reports
make docs.consolidate   # ensure target directory structure
make docs.dedupe        # merge duplicate sections (placeholder)
make docs.all           # run all steps
```

Each run is idempotent: existing output files are replaced with fresh results and
no source documents are modified unless the consolidate or dedupe steps perform
changes. Any changes are tracked in `WORK-ON-new_docs/out/migration_journal.md`.
