CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY,
    title TEXT,
    source TEXT,
    aleph_id TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS entities (
    id UUID PRIMARY KEY,
    doc_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    label TEXT NOT NULL,
    value TEXT NOT NULL,
    span_start INT,
    span_end INT,
    confidence FLOAT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS entity_resolutions (
    entity_id UUID PRIMARY KEY REFERENCES entities(id) ON DELETE CASCADE,
    node_id TEXT NULL,
    score FLOAT NULL,
    status TEXT NOT NULL,
    candidates JSONB NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);
