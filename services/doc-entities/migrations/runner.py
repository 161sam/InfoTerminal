#!/usr/bin/env python3
"""Simple migration runner for the doc-entities service."""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import sqlalchemy as sa
from sqlalchemy.engine import Connection, Engine

MIGRATIONS_DIR = Path(__file__).resolve().parent
PACKAGE_NAME = "doc_entities_migrations"
VERSION_TABLE_NAME = "doc_entities_schema_migrations"


@dataclass
class Migration:
    revision: str
    down_revision: Optional[str]
    description: str
    module: types.ModuleType

    def upgrade(self, conn: Connection) -> None:
        self.module.upgrade(conn)

    def downgrade(self, conn: Connection) -> None:
        self.module.downgrade(conn)

    def backfill(self, conn: Connection) -> None:
        self.module.backfill(conn)


def _register_package() -> None:
    if PACKAGE_NAME in sys.modules:
        return
    package = types.ModuleType(PACKAGE_NAME)
    package.__path__ = [str(MIGRATIONS_DIR)]  # type: ignore[attr-defined]
    sys.modules[PACKAGE_NAME] = package


def _load_submodule(name: str) -> types.ModuleType:
    path = MIGRATIONS_DIR / f"{name}.py"
    if not path.exists():
        raise FileNotFoundError(f"migration module {name} not found at {path}")
    module_name = f"{PACKAGE_NAME}.{name}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load spec for {module_name}")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = PACKAGE_NAME
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _load_migration_modules() -> List[Migration]:
    _register_package()
    # Ensure utils is loaded so relative imports succeed.
    if f"{PACKAGE_NAME}.utils" not in sys.modules:
        _load_submodule("utils")

    migrations: List[Migration] = []
    for path in sorted(MIGRATIONS_DIR.glob("[0-9][0-9][0-9]_*.py")):
        module = _load_submodule(path.stem)
        revision = getattr(module, "revision", None)
        down_revision = getattr(module, "down_revision", None)
        description = getattr(module, "description", "")
        if revision is None:
            raise AttributeError(f"migration {path.name} missing revision identifier")
        migrations.append(
            Migration(
                revision=revision,
                down_revision=down_revision,
                description=description,
                module=module,
            )
        )
    return migrations


def _current_timestamp_default(conn: Connection) -> sa.sql.ClauseElement:
    if conn.dialect.name == "postgresql":
        return sa.func.now()
    return sa.text("CURRENT_TIMESTAMP")


class MigrationRunner:
    def __init__(self, engine: Engine):
        self.engine = engine
        self._migrations = _load_migration_modules()
        self._order = self._build_linear_order(self._migrations)
        self._revision_index: Dict[str, int] = {
            migration.revision: idx for idx, migration in enumerate(self._order)
        }
        self._version_table: Optional[sa.Table] = None

    @staticmethod
    def _build_linear_order(migrations: Iterable[Migration]) -> List[Migration]:
        migrations = list(migrations)
        if not migrations:
            return []

        by_revision: Dict[str, Migration] = {m.revision: m for m in migrations}
        starts = [m for m in migrations if m.down_revision in (None, "base")]
        if len(starts) != 1:
            raise RuntimeError(
                "Expected exactly one base migration (with down_revision=None)."
            )
        order: List[Migration] = []
        current = starts[0]
        while current:
            order.append(current)
            next_migration = next(
                (m for m in migrations if m.down_revision == current.revision), None
            )
            if next_migration is None:
                break
            current = next_migration
        if len(order) != len(migrations):
            missing = set(by_revision) - {m.revision for m in order}
            raise RuntimeError(
                f"Migrations are not linear – missing linkage for: {', '.join(sorted(missing))}"
            )
        return order

    # --- version table helpers -------------------------------------------------
    def _ensure_version_table(self, conn: Connection) -> sa.Table:
        if self._version_table is None:
            metadata = sa.MetaData()
            self._version_table = sa.Table(
                VERSION_TABLE_NAME,
                metadata,
                sa.Column("revision", sa.String(255), primary_key=True),
                sa.Column(
                    "applied_at",
                    sa.DateTime(timezone=True),
                    server_default=_current_timestamp_default(conn),
                ),
            )
        self._version_table.create(bind=conn, checkfirst=True)
        return self._version_table

    def _applied_revisions(self) -> List[str]:
        with self.engine.begin() as conn:
            table = self._ensure_version_table(conn)
            rows = (
                conn.execute(
                    sa.select(table.c.revision).order_by(table.c.applied_at)
                )
                .scalars()
                .all()
            )
        return list(rows)

    def _current_index(self) -> int:
        applied = self._applied_revisions()
        if not applied:
            return -1
        return self._revision_index[applied[-1]]

    # --- public API ------------------------------------------------------------
    def status(self) -> List[str]:
        applied = set(self._applied_revisions())
        lines = []
        for migration in self._order:
            marker = "✔" if migration.revision in applied else "…"
            desc = f" – {migration.description}" if migration.description else ""
            lines.append(f"{marker} {migration.revision}{desc}")
        return lines

    def upgrade(self, to_revision: Optional[str] = None, run_backfill: bool = False) -> None:
        target_index = self._resolve_target_index(to_revision or "head")
        current_index = self._current_index()
        if current_index >= target_index:
            print(f"Already at or beyond target revision {to_revision or 'head'}")
            return
        for migration in self._order[current_index + 1 : target_index + 1]:
            self._apply_migration(migration, run_backfill=run_backfill)

    def downgrade(self, to_revision: str) -> None:
        target_index = self._resolve_target_index(to_revision, allow_base=True)
        current_index = self._current_index()
        if target_index == current_index:
            print(f"Already at revision {to_revision}")
            return
        if target_index > current_index:
            raise ValueError(
                f"Cannot downgrade to {to_revision}; it is ahead of the current revision."
            )
        for migration in reversed(self._order[target_index + 1 : current_index + 1]):
            self._revert_migration(migration)

    def run_backfill(self, revision: Optional[str] = None) -> None:
        if revision is None or revision == "all":
            revisions = self._applied_revisions()
        elif revision == "head":
            applied = self._applied_revisions()
            revisions = applied[-1:] if applied else []
        else:
            if revision not in self._revision_index:
                raise ValueError(f"Unknown revision {revision}")
            revisions = [revision]
        for rev in revisions:
            migration = self._order[self._revision_index[rev]]
            print(f"Backfilling {rev}")
            with self.engine.begin() as conn:
                table = self._ensure_version_table(conn)
                migration.backfill(conn)
                # Touch the version row to update applied_at
                conn.execute(
                    sa.update(table)
                    .where(table.c.revision == rev)
                    .values(applied_at=_current_timestamp_default(conn))
                )

    # --- internals -------------------------------------------------------------
    def _resolve_target_index(self, revision: str, allow_base: bool = False) -> int:
        if revision in (None, "head"):
            return len(self._order) - 1 if self._order else -1
        if revision == "base":
            if not allow_base:
                raise ValueError("'base' is only valid for downgrade targets")
            return -1
        if revision not in self._revision_index:
            raise ValueError(f"Unknown revision {revision}")
        return self._revision_index[revision]

    def _apply_migration(self, migration: Migration, run_backfill: bool) -> None:
        print(f"Applying {migration.revision}")
        with self.engine.begin() as conn:
            table = self._ensure_version_table(conn)
            migration.upgrade(conn)
            conn.execute(table.insert().values(revision=migration.revision))
            if run_backfill:
                migration.backfill(conn)

    def _revert_migration(self, migration: Migration) -> None:
        print(f"Reverting {migration.revision}")
        with self.engine.begin() as conn:
            table = self._ensure_version_table(conn)
            migration.downgrade(conn)
            conn.execute(
                table.delete().where(table.c.revision == migration.revision)
            )


def _database_url_from_env() -> Optional[str]:
    return os.getenv("DOC_ENTITIES_DATABASE_URL") or os.getenv("DATABASE_URL")


def _create_engine(database_url: Optional[str], echo: bool = False) -> Engine:
    if not database_url:
        raise SystemExit("A database URL is required. Use --database-url or set DATABASE_URL.")
    return sa.create_engine(database_url, future=True, echo=echo)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-url", dest="database_url", help="SQLAlchemy database URL.")
    parser.add_argument("--echo", action="store_true", help="Enable SQLAlchemy SQL echo.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    upgrade_parser = subparsers.add_parser("upgrade", help="Apply migrations up to a target revision.")
    upgrade_parser.add_argument("--to", dest="to_revision", default="head")
    upgrade_parser.add_argument(
        "--run-backfill",
        dest="run_backfill",
        action="store_true",
        help="Run backfill immediately after each migration.",
    )

    downgrade_parser = subparsers.add_parser("downgrade", help="Rollback migrations down to a revision.")
    downgrade_parser.add_argument("--to", dest="to_revision", required=True)

    backfill_parser = subparsers.add_parser("backfill", help="Run backfill routines.")
    backfill_parser.add_argument(
        "--revision",
        default="all",
        help="Revision to backfill (default: all applied revisions).",
    )

    subparsers.add_parser("status", help="Show applied migrations.")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    database_url = args.database_url or _database_url_from_env()
    engine = _create_engine(database_url, echo=args.echo)
    runner = MigrationRunner(engine)

    if args.command == "status":
        for line in runner.status():
            print(line)
        return 0

    if args.command == "upgrade":
        runner.upgrade(to_revision=args.to_revision, run_backfill=args.run_backfill)
        return 0

    if args.command == "downgrade":
        runner.downgrade(to_revision=args.to_revision)
        return 0

    if args.command == "backfill":
        runner.run_backfill(revision=args.revision)
        return 0

    parser.error(f"Unknown command {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
