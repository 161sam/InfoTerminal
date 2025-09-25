"""Utility helpers for doc-entities migrations.

These helpers keep the migration scripts small and provide
cross-database compatibility so that our smoke tests can run on SQLite
while production keeps using PostgreSQL.
"""

from __future__ import annotations

import contextlib
from typing import Iterable, Sequence

import sqlalchemy as sa
from sqlalchemy.engine import Connection


def uuid_type(conn: Connection) -> sa.types.TypeEngine:
    """Return a UUID-compatible type for the current connection."""

    if conn.dialect.name == "postgresql":
        from sqlalchemy.dialects.postgresql import UUID

        return UUID(as_uuid=True)
    return sa.String(36)


def json_type(conn: Connection) -> sa.types.TypeEngine:
    """Return a JSON-compatible column type."""

    if conn.dialect.name == "postgresql":
        from sqlalchemy.dialects.postgresql import JSONB

        return JSONB()
    return sa.JSON()


def current_timestamp_default(conn: Connection) -> sa.sql.ClauseElement:
    """Return a server default for the current timestamp."""

    if conn.dialect.name == "postgresql":
        return sa.func.now()
    return sa.text("CURRENT_TIMESTAMP")


def ensure_index(
    conn: Connection,
    name: str,
    table: sa.Table,
    columns: Sequence[str],
) -> None:
    """Create an index if it does not yet exist."""

    index = sa.Index(name, *[table.c[col] for col in columns])
    index.create(bind=conn, checkfirst=True)


def drop_index(conn: Connection, name: str, table_name: str) -> None:
    inspector = sa.inspect(conn)
    existing = {idx["name"] for idx in inspector.get_indexes(table_name)}
    if name in existing:
        sa.Index(name).drop(bind=conn)


def table_exists(conn: Connection, table_name: str) -> bool:
    return sa.inspect(conn).has_table(table_name)


def drop_table(conn: Connection, table_name: str) -> None:
    metadata = sa.MetaData()
    table = sa.Table(table_name, metadata)
    table.drop(bind=conn, checkfirst=True)


def reflect_table(conn: Connection, table_name: str) -> sa.Table:
    metadata = sa.MetaData()
    return sa.Table(table_name, metadata, autoload_with=conn)


def delete_rows(conn: Connection, table: sa.Table, ids: Iterable) -> None:
    ids = list(ids)
    if not ids:
        return
    conn.execute(table.delete().where(table.c.id.in_(ids)))


@contextlib.contextmanager
def transactional_connection(engine: sa.engine.Engine):
    with engine.begin() as conn:
        yield conn
