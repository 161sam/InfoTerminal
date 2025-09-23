import uuid
from sqlalchemy import Column, Text, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import CHAR, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID as PGUUID

Base = declarative_base()


class GUID(TypeDecorator):
    """Platform-independent GUID type."""

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PGUUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return str(value)
        return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)


class Document(Base):
    __tablename__ = "documents"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=True)
    source = Column(Text, nullable=True)
    aleph_id = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Entity(Base):
    __tablename__ = "entities"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    doc_id = Column(GUID(), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    label = Column(Text, nullable=False)
    value = Column(Text, nullable=False)
    span_start = Column(Integer)
    span_end = Column(Integer)
    confidence = Column(Float)
    context = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EntityResolution(Base):
    __tablename__ = "entity_resolutions"
    entity_id = Column(GUID(), ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True)
    node_id = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    status = Column(Text, nullable=False)
    candidates = Column(JSON, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Relation(Base):
    __tablename__ = "relations"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    doc_id = Column(GUID(), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    subject_entity_id = Column(GUID(), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    object_entity_id = Column(GUID(), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    predicate = Column(Text, nullable=False)  # The relationship type (e.g., "WORKS_AT", "BORN_IN")
    predicate_text = Column(Text, nullable=True)  # The actual text that indicates the relationship
    confidence = Column(Float, nullable=True)
    span_start = Column(Integer, nullable=True)  # Start of the relation trigger text
    span_end = Column(Integer, nullable=True)    # End of the relation trigger text
    context = Column(Text, nullable=True)
    extraction_method = Column(Text, nullable=True)  # "dependency_parse", "pattern_match", "ml_model"
    metadata_json = Column("metadata", JSON, nullable=True)  # Additional extraction metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships for easy access
    subject_entity = relationship("Entity", foreign_keys=[subject_entity_id])
    object_entity = relationship("Entity", foreign_keys=[object_entity_id])


class RelationResolution(Base):
    __tablename__ = "relation_resolutions"
    relation_id = Column(GUID(), ForeignKey("relations.id", ondelete="CASCADE"), primary_key=True)
    graph_edge_id = Column(Text, nullable=True)  # ID of the created edge in Neo4j
    status = Column(Text, nullable=False)  # "pending", "resolved", "failed"
    score = Column(Float, nullable=True)
    metadata_json = Column("metadata", JSON, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
