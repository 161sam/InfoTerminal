import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
from db import build_database_url_from_env


def test_build_from_parts():
    env = {
        "GV_DATABASE_URL": "",
        "GV_PG_HOST": "dbhost",
        "GV_PG_PORT": "5555",
        "GV_PG_USER": "u",
        "GV_PG_PASSWORD": "p",
        "GV_PG_DB": "d",
    }
    url = build_database_url_from_env(env)
    assert url == "postgresql://u:p@dbhost:5555/d"


def test_take_url_directly():
    env = {"GV_DATABASE_URL": "postgresql://x"}
    assert build_database_url_from_env(env) == "postgresql://x"
