import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- PG ENV Fallbacks (injected) ---
def _pg_env(*names, default=None):
    for n in names:
        v = os.getenv(n)
        if v:
            return v
    return default
PG_HOST = _pg_env("PG_HOST","PGHOST","POSTGRES_HOST","DB_HOST","DATABASE_HOST","PGHOSTADDR","HOST", default="127.0.0.1")
PG_PORT = int(_pg_env("PG_PORT","PGPORT","POSTGRES_PORT","DB_PORT","DATABASE_PORT","PORT", default="5432"))
PG_DB   = _pg_env("PG_DB","PGDATABASE","POSTGRES_DB","DB_NAME","DATABASE_NAME","PGDATABASE", default="it_graph")
PG_USER = _pg_env("PG_USER","PGUSER","POSTGRES_USER","DB_USER","DATABASE_USER", default="it_user")
PG_PASS = _pg_env("PG_PASS","PGPASSWORD","PG_PASSWORD","POSTGRES_PASSWORD","DB_PASS","DB_PASSWORD","DATABASE_PASSWORD", default="it_pass")

DATABASE_URL = os.getenv("DATABASE_URL") or f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
