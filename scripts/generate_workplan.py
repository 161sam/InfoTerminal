import json
import re
from datetime import datetime, timezone
from pathlib import Path

EPIC_KEYWORDS = {
    "nlp": ["nlp"],
    "geo": ["geo", "ais", "adsb"],
    "graph": ["graph"],
    "ingest/nifi": ["nifi", "ingest"],
    "n8n": ["n8n"],
    "superset": ["superset"],
    "auth/oidc": ["oidc", "auth", "keycloak"],
    "verification": ["verification", "verif"],
    "mediaforensics": ["mediaforensics", "media forensics", "forensic"],
    "sdk": ["sdk"],
    "observability": ["observability", "metrics", "slo", "sli"],
    "security": ["security", "vault", "trivy", "sbom", "cosign"],
    "dossier": ["dossier"],
    "active-learning": ["active learning", "retrain"],
}

TABLE_LINE = re.compile(r"^\|\s*(T\d+-[0-9a-f]+)\s*\|\s*([^|]+)\|\s*\d+\s*\|\s*(.*)\|\s*$")


def parse_todo_index(path: Path):
    tasks = []
    for line in path.read_text().splitlines():
        m = TABLE_LINE.match(line)
        if not m:
            continue
        task_id, file_path, text = m.groups()
        if "- [ ]" not in text and "TODO" not in text:
            continue
        tasks.append({"id": task_id, "file": file_path.strip(), "text": text.strip()})
    return tasks


def categorize(tasks):
    epics = {key: [] for key in EPIC_KEYWORDS}
    for t in tasks:
        haystack = f"{t['file']} {t['text']}".lower()
        for key, keywords in EPIC_KEYWORDS.items():
            if any(kw in haystack for kw in keywords):
                epics[key].append(t["id"])
    return epics


def build_workplan(todo_index_path: Path, output_path: Path):
    tasks = parse_todo_index(todo_index_path)
    categorized = categorize(tasks)
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "epics": [
            {"key": key, "todo_ids": ids, "status": "pending"} for key, ids in categorized.items()
        ],
        "done_ids": [],
        "skipped_ids": [],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    todo_index = repo_root / "WORK-ON-new_docs/out/todo_index.md"
    output = repo_root / "WORK-ON-new_docs/dev_progress/workplan.json"
    build_workplan(todo_index, output)
    print(f"Workplan written to {output}")
