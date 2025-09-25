"""Initial schema for doc-entities."""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from .utils import current_timestamp_default, drop_table, json_type, uuid_type

revision = "001"
down_revision = None
description = "Create base tables for documents, entities, and resolutions."


def _documents_table(conn: Connection, metadata: sa.MetaData) -> sa.Table:
    return sa.Table(
        "documents",
        metadata,
        sa.Column("id", uuid_type(conn), primary_key=True),
        sa.Column("title", sa.Text, nullable=True),
        sa.Column("source", sa.Text, nullable=True),
        sa.Column("aleph_id", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=current_timestamp_default(conn),
        ),
    )


def _entities_table(conn: Connection, metadata: sa.MetaData) -> sa.Table:
    return sa.Table(
        "entities",
        metadata,
        sa.Column("id", uuid_type(conn), primary_key=True),
        sa.Column(
            "doc_id",
            uuid_type(conn),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("label", sa.Text, nullable=False),
        sa.Column("value", sa.Text, nullable=False),
        sa.Column("span_start", sa.Integer, nullable=True),
        sa.Column("span_end", sa.Integer, nullable=True),
        sa.Column("confidence", sa.Float, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=current_timestamp_default(conn),
        ),
    )


def _entity_resolutions_table(conn: Connection, metadata: sa.MetaData) -> sa.Table:
    return sa.Table(
        "entity_resolutions",
        metadata,
        sa.Column(
            "entity_id",
            uuid_type(conn),
            sa.ForeignKey("entities.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("node_id", sa.Text, nullable=True),
        sa.Column("score", sa.Float, nullable=True),
        sa.Column("status", sa.Text, nullable=False),
        sa.Column("candidates", json_type(conn), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=current_timestamp_default(conn),
            server_onupdate=current_timestamp_default(conn),
        ),
    )


def upgrade(conn: Connection) -> None:
    metadata = sa.MetaData()
    documents = _documents_table(conn, metadata)
    entities = _entities_table(conn, metadata)
    resolutions = _entity_resolutions_table(conn, metadata)

    for table in (documents, entities, resolutions):
        table.create(bind=conn, checkfirst=True)


def downgrade(conn: Connection) -> None:
    drop_table(conn, "entity_resolutions")
    drop_table(conn, "entities")
    drop_table(conn, "documents")


def backfill(conn: Connection) -> None:  # pragma: no cover - nothing to backfill yet
    """No backfill needed for the initial schema."""
    return None
