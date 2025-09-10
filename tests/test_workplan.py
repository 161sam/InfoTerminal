from pathlib import Path
import json
from scripts.generate_workplan import parse_todo_index, categorize, build_workplan

SAMPLE = """
| ID | File | Line | Text |
|---|---|---|---|
| T0001-aaaa | services/nlp/readme.md | 10 | - [ ] implement NER |
| T0002-bbbb | services/geo/readme.md | 5 | - [ ] add map viewer |
| T0003-cccc | docs/security.md | 7 | - [ ] fix vulnerabilities |
"""

def test_parse_and_categorize(tmp_path: Path):
    todo_file = tmp_path / "todo_index.md"
    todo_file.write_text(SAMPLE)
    tasks = parse_todo_index(todo_file)
    assert {t['id'] for t in tasks} == {"T0001-aaaa", "T0002-bbbb", "T0003-cccc"}

    epics = categorize(tasks)
    assert "T0001-aaaa" in epics["nlp"]
    assert "T0002-bbbb" in epics["geo"]
    assert "T0003-cccc" in epics["security"]


def test_build_workplan(tmp_path: Path):
    todo_file = tmp_path / "todo_index.md"
    todo_file.write_text(SAMPLE)
    output = tmp_path / "workplan.json"
    build_workplan(todo_file, output)
    data = json.loads(output.read_text())
    assert data["epics"]
    keys = {e["key"] for e in data["epics"]}
    assert "nlp" in keys
