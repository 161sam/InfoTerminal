import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SERVICE_DIRS = [
    "services/search-api",
    "services/graph-api",
    "services/graph-views",
]

for rel in SERVICE_DIRS:
    service_path = ROOT / rel
    if service_path.exists():
        sys.path.insert(0, str(service_path))
        src = service_path / "src"
        if src.exists():
            sys.path.insert(0, str(src))
