import pathlib
import subprocess


def test_patch_ports_generates_keys(tmp_path):
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    env_file = repo_root / ".env.dev.ports"
    original = env_file.read_text()
    try:
        subprocess.run(["scripts/patch_ports.sh"], cwd=repo_root, check=True)
        content = env_file.read_text()
        assert "PROMETHEUS_PORT=3412" in content
        assert "GRAFANA_PORT=3413" in content
        assert "ALERTMANAGER_PORT=3414" in content
    finally:
        env_file.write_text(original)

        subprocess.run(
            [
                "git",
                "checkout",
                "--",
                "docker-compose.yml",
                "docker-compose.observability.yml",
                "docker-compose.agents.yml",
                "charts/infoterminal/values.yaml",
                "apps/frontend/.env.local",
                "apps/frontend/package.json",
            ],
            cwd=repo_root,
            check=False,
        )
