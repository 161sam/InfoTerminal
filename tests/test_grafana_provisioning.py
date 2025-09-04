import pathlib
import yaml


def test_datasources_yaml_parses():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    f = repo_root / "deploy/grafana/provisioning/datasources/datasources.yml"
    data = yaml.safe_load(f.read_text())
    names = {d.get("name") for d in data.get("datasources", [])}
    assert {"Prometheus", "Loki", "Tempo"}.issubset(names)
