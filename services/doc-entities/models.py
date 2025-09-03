import uuid
from sqlalchemy import Column, Text, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=True)
    source = Column(Text, nullable=True)
    aleph_id = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Entity(Base):
    __tablename__ = "entities"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    label = Column(Text, nullable=False)
    value = Column(Text, nullable=False)
    span_start = Column(Integer)
    span_end = Column(Integer)
    confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EntityResolution(Base):
    __tablename__ = "entity_resolutions"
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True)
    node_id = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    status = Column(Text, nullable=False)
    candidates = Column(JSON, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
