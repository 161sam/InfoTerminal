"""Add relations and relation_resolutions tables

Revision ID: 003
Create Date: 2025-09-16

"""

# revision identifiers
revision = '003'
down_revision = '002'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

def upgrade():
    # Create relations table
    op.create_table(
        'relations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('doc_id', UUID(as_uuid=True), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('subject_entity_id', UUID(as_uuid=True), sa.ForeignKey('entities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('object_entity_id', UUID(as_uuid=True), sa.ForeignKey('entities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('predicate', sa.Text, nullable=False),
        sa.Column('predicate_text', sa.Text, nullable=True),
        sa.Column('confidence', sa.Float, nullable=True),
        sa.Column('span_start', sa.Integer, nullable=True),
        sa.Column('span_end', sa.Integer, nullable=True),
        sa.Column('context', sa.Text, nullable=True),
        sa.Column('extraction_method', sa.Text, nullable=True),
        sa.Column('metadata', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Create relation_resolutions table
    op.create_table(
        'relation_resolutions',
        sa.Column('relation_id', UUID(as_uuid=True), sa.ForeignKey('relations.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('graph_edge_id', sa.Text, nullable=True),
        sa.Column('status', sa.Text, nullable=False),
        sa.Column('score', sa.Float, nullable=True),
        sa.Column('metadata', sa.JSON, nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Create indexes for better performance
    op.create_index('idx_relations_doc_id', 'relations', ['doc_id'])
    op.create_index('idx_relations_subject_entity', 'relations', ['subject_entity_id'])
    op.create_index('idx_relations_object_entity', 'relations', ['object_entity_id'])
    op.create_index('idx_relations_predicate', 'relations', ['predicate'])


def downgrade():
    op.drop_table('relation_resolutions')
    op.drop_table('relations')
