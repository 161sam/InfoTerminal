"""Create demo collection in Aleph and store ID in .env."""
from __future__ import annotations
import os
import sys
from pathlib import Path
import requests

def main() -> None:
    api_url = os.getenv("ALEPH_API_URL", "http://localhost:8082")
    api_key = os.getenv("ALEPH_API_KEY")
    if not api_key:
        print("ALEPH_API_KEY missing", file=sys.stderr)
        sys.exit(1)
    resp = requests.post(
        f"{api_url}/api/2/collections",
        headers={"Authorization": f"ApiKey {api_key}"},
        json={"label": "InfoTerminal Demo"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    cid = data.get("id") or data.get("collection", {}).get("id")
    if not cid:
        print("could not determine collection id", file=sys.stderr)
        sys.exit(1)
    env_path = Path(".env")
    lines: list[str] = []
    if env_path.exists():
        lines = env_path.read_text().splitlines()
    keyline = f"COLLECTION_ID={cid}"
    found = False
    for i, line in enumerate(lines):
        if line.startswith("COLLECTION_ID="):
            lines[i] = keyline
            found = True
            break
    if not found:
        lines.append(keyline)
    env_path.write_text("\n".join(lines) + "\n")
    print(cid)

if __name__ == "__main__":
    main()
