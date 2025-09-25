"""Add relations tables linking extracted entities."""

from __future__ import annotations

from typing import List

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from .utils import (
    current_timestamp_default,
    drop_table,
    ensure_index,
    json_type,
    table_exists,
    uuid_type,
)

revision = "003"
down_revision = "002"
description = "Introduce relations and relation_resolutions tables."

_RELATIONS_BACKUP = "doc_entities_relations_backup"
_RELATION_RES_BACKUP = "doc_entities_relation_resolutions_backup"
_INDEXES = [
    ("idx_relations_doc_id", ["doc_id"]),
    ("idx_relations_subject_entity", ["subject_entity_id"]),
    ("idx_relations_object_entity", ["object_entity_id"]),
    ("idx_relations_predicate", ["predicate"]),
]


def _relations_table(conn: Connection, metadata: sa.MetaData | None = None) -> sa.Table:
    if metadata is None:
        metadata = sa.MetaData()
    return sa.Table(
        "relations",
        metadata,
        sa.Column("id", uuid_type(conn), primary_key=True),
        sa.Column(
            "doc_id",
            uuid_type(conn),
            sa.ForeignKey("documents.id", ondelete="CASCADE", link_to_name=True),
            nullable=False,
        ),
        sa.Column(
            "subject_entity_id",
            uuid_type(conn),
            sa.ForeignKey("entities.id", ondelete="CASCADE", link_to_name=True),
            nullable=False,
        ),
        sa.Column(
            "object_entity_id",
            uuid_type(conn),
            sa.ForeignKey("entities.id", ondelete="CASCADE", link_to_name=True),
            nullable=False,
        ),
        sa.Column("predicate", sa.Text, nullable=False),
        sa.Column("predicate_text", sa.Text, nullable=True),
        sa.Column("confidence", sa.Float, nullable=True),
        sa.Column("span_start", sa.Integer, nullable=True),
        sa.Column("span_end", sa.Integer, nullable=True),
        sa.Column("context", sa.Text, nullable=True),
        sa.Column("extraction_method", sa.Text, nullable=True),
        sa.Column("metadata", json_type(conn), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=current_timestamp_default(conn),
        ),
    )


def _relation_resolutions_table(
    conn: Connection, metadata: sa.MetaData | None = None
) -> sa.Table:
    if metadata is None:
        metadata = sa.MetaData()
    return sa.Table(
        "relation_resolutions",
        metadata,
        sa.Column(
            "relation_id",
            uuid_type(conn),
            sa.ForeignKey("relations.id", ondelete="CASCADE", link_to_name=True),
            primary_key=True,
        ),
        sa.Column("graph_edge_id", sa.Text, nullable=True),
        sa.Column("status", sa.Text, nullable=False),
        sa.Column("score", sa.Float, nullable=True),
        sa.Column("metadata", json_type(conn), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=current_timestamp_default(conn),
            server_onupdate=current_timestamp_default(conn),
        ),
    )


def _backup_relations_table(conn: Connection) -> sa.Table:
    metadata = sa.MetaData()
    return sa.Table(
        _RELATIONS_BACKUP,
        metadata,
        sa.Column("id", uuid_type(conn), primary_key=True),
        sa.Column("doc_id", uuid_type(conn), nullable=False),
        sa.Column("subject_entity_id", uuid_type(conn), nullable=False),
        sa.Column("object_entity_id", uuid_type(conn), nullable=False),
        sa.Column("predicate", sa.Text, nullable=False),
        sa.Column("predicate_text", sa.Text, nullable=True),
        sa.Column("confidence", sa.Float, nullable=True),
        sa.Column("span_start", sa.Integer, nullable=True),
        sa.Column("span_end", sa.Integer, nullable=True),
        sa.Column("context", sa.Text, nullable=True),
        sa.Column("extraction_method", sa.Text, nullable=True),
        sa.Column("metadata", json_type(conn), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def _backup_relation_resolutions_table(conn: Connection) -> sa.Table:
    metadata = sa.MetaData()
    return sa.Table(
        _RELATION_RES_BACKUP,
        metadata,
        sa.Column("relation_id", uuid_type(conn), primary_key=True),
        sa.Column("graph_edge_id", sa.Text, nullable=True),
        sa.Column("status", sa.Text, nullable=False),
        sa.Column("score", sa.Float, nullable=True),
        sa.Column("metadata", json_type(conn), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def upgrade(conn: Connection) -> None:
    metadata = sa.MetaData()
    # register referenced tables for FK resolution
    sa.Table("documents", metadata, autoload_with=conn)
    sa.Table("entities", metadata, autoload_with=conn)
    relations = _relations_table(conn, metadata)
    relation_resolutions = _relation_resolutions_table(conn, metadata)

    relations.create(bind=conn, checkfirst=True)
    relation_resolutions.create(bind=conn, checkfirst=True)

    for name, columns in _INDEXES:
        ensure_index(conn, name, relations, columns)

    _restore_from_backup(conn, relations, relation_resolutions)


def _restore_from_backup(
    conn: Connection, relations: sa.Table, relation_resolutions: sa.Table
) -> None:
    metadata = sa.MetaData()

    if table_exists(conn, _RELATIONS_BACKUP):
        backup_relations = sa.Table(_RELATIONS_BACKUP, metadata, autoload_with=conn)
        rows = [dict(row._mapping) for row in conn.execute(sa.select(backup_relations))]
        if rows:
            existing_ids = set(conn.execute(sa.select(relations.c.id)).scalars().all())
            to_insert = [row for row in rows if row["id"] not in existing_ids]
            if to_insert:
                conn.execute(sa.insert(relations), to_insert)
        drop_table(conn, _RELATIONS_BACKUP)

    if table_exists(conn, _RELATION_RES_BACKUP):
        backup_res = sa.Table(_RELATION_RES_BACKUP, metadata, autoload_with=conn)
        rows = [dict(row._mapping) for row in conn.execute(sa.select(backup_res))]
        if rows:
            existing_ids = set(
                conn.execute(sa.select(relation_resolutions.c.relation_id))
                .scalars()
                .all()
            )
            to_insert = [row for row in rows if row["relation_id"] not in existing_ids]
            if to_insert:
                conn.execute(sa.insert(relation_resolutions), to_insert)
        drop_table(conn, _RELATION_RES_BACKUP)


def backfill(conn: Connection) -> None:
    if not table_exists(conn, "relations"):
        return

    metadata = sa.MetaData()
    relations = sa.Table("relations", metadata, autoload_with=conn)

    if "predicate_text" in relations.c:
        conn.execute(
            sa.update(relations)
            .where(relations.c.predicate_text.is_(None))
            .values(predicate_text=relations.c.predicate)
        )

    if not table_exists(conn, "relation_resolutions"):
        return

    relation_resolutions = sa.Table(
        "relation_resolutions", metadata, autoload_with=conn
    )

    missing_ids: List = (
        conn.execute(
            sa.select(relations.c.id)
            .select_from(
                relations.outerjoin(
                    relation_resolutions,
                    relation_resolutions.c.relation_id == relations.c.id,
                )
            )
            .where(relation_resolutions.c.relation_id.is_(None))
        )
        .scalars()
        .all()
    )

    if missing_ids:
        conn.execute(
            sa.insert(relation_resolutions),
            [
                {
                    "relation_id": rel_id,
                    "graph_edge_id": None,
                    "status": "pending",
                    "score": None,
                    "metadata": None,
                }
                for rel_id in missing_ids
            ],
        )


def downgrade(conn: Connection) -> None:
    if not table_exists(conn, "relations"):
        return

    relations = _relations_table(conn)
    relation_resolutions = _relation_resolutions_table(conn)

    _backup_current_data(conn, relations, relation_resolutions)

    if table_exists(conn, "relation_resolutions"):
        drop_table(conn, "relation_resolutions")
    drop_table(conn, "relations")


def _backup_current_data(
    conn: Connection, relations: sa.Table, relation_resolutions: sa.Table
) -> None:
    backup_relations = _backup_relations_table(conn)
    backup_resolutions = _backup_relation_resolutions_table(conn)

    backup_relations.create(bind=conn, checkfirst=True)
    backup_resolutions.create(bind=conn, checkfirst=True)

    relation_rows = [dict(row._mapping) for row in conn.execute(sa.select(relations))]
    if relation_rows:
        existing_backup_ids = set(
            conn.execute(sa.select(backup_relations.c.id)).scalars().all()
        )
        to_delete = [row["id"] for row in relation_rows if row["id"] in existing_backup_ids]
        if to_delete:
            conn.execute(
                backup_relations.delete().where(backup_relations.c.id.in_(to_delete))
            )
        conn.execute(sa.insert(backup_relations), relation_rows)

    resolution_rows: List[dict] = []
    if table_exists(conn, "relation_resolutions"):
        resolution_rows = [
            dict(row._mapping)
            for row in conn.execute(sa.select(relation_resolutions))
        ]
    if resolution_rows:
        existing_backup_rel_ids = set(
            conn.execute(sa.select(backup_resolutions.c.relation_id))
            .scalars()
            .all()
        )
        to_delete = [
            row["relation_id"]
            for row in resolution_rows
            if row["relation_id"] in existing_backup_rel_ids
        ]
        if to_delete:
            conn.execute(
                backup_resolutions.delete().where(
                    backup_resolutions.c.relation_id.in_(to_delete)
                )
            )
        conn.execute(sa.insert(backup_resolutions), resolution_rows)
