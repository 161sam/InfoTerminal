"""Add context column to entities for richer NLP snippets."""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.engine import Connection

revision = "002"
down_revision = "001"
description = "Add entities.context column"


def upgrade(conn: Connection) -> None:
    metadata = sa.MetaData()
    entities = sa.Table("entities", metadata, autoload_with=conn)

    if "context" not in entities.c:
        conn.execute(sa.text("ALTER TABLE entities ADD COLUMN context TEXT"))


def downgrade(conn: Connection) -> None:
    metadata = sa.MetaData()
    entities = sa.Table("entities", metadata, autoload_with=conn)

    if "context" in entities.c:
        conn.execute(sa.text("ALTER TABLE entities DROP COLUMN context"))


def backfill(conn: Connection) -> None:  # pragma: no cover - nothing to backfill yet
    """Nothing to backfill; column stays nullable."""
    return None
