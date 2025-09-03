import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB = os.getenv("PG_DB", "infoterminal")
PG_USER = os.getenv("PG_USER", "app")
PG_PASS = os.getenv("PG_PASS", "app")

DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
