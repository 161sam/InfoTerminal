from __future__ import annotations
import os, sys, shlex, json, socket, time, subprocess
from pathlib import Path
import typer
from rich import print
from rich.table import Table
from rich.console import Console

app = typer.Typer(add_completion=False, help="InfoTerminal CLI (dev-local & docker orchestration)")

console = Console()
ROOT_MARKERS = ["docker-compose.yml", ".git"]

# ---- Port-Policy (keine Standard-Host-Ports) ----
PORTS = {
    "frontend": 3411,
    "gateway":  8610,
    "search":   8611,
    "graph":    8612,
    "aleph":    8613,
    "grafana":  3412,
    "loki":     3413,
    "tempo":    3414,
    "prom":     3415,
    "otel":     3416,
    "flowise":  3417,
    "pg":       55432,
    "neo4j_http": 8744,
    "neo4j_https":8743,
    "neo4j_bolt": 8767,
}

# ---- Compose Projekte / Files ----
MAIN_PROJ = "infoterminal"
OBS_PROJ  = "infoterminal_obs"
AG_PROJ   = "infoterminal_agents"
GW_PROJ   = "infoterminal_gateway"
OPA_PROJ  = "infoterminal_opa"

MAIN_FILE = "docker-compose.yml"
OBS_FILE  = "docker-compose.observability.yml"
AG_FILE   = "docker-compose.agents.yml"
GW_FILE   = "docker-compose.gateway.yml"
OPA_FILE  = "docker-compose.opa.yml"

def repo_root() -> Path:
    p = Path.cwd()
    while p != p.parent:
        if any((p / m).exists() for m in ROOT_MARKERS):
            return p
        p = p.parent
    raise SystemExit("❌ Repo-Root nicht gefunden – hier existiert kein docker-compose.yml")

def run(cmd:list[str], cwd:Path|None=None, check=True, env:dict|None=None, capture=False):
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    r = subprocess.run(cmd, cwd=str(cwd or repo_root()), env={**os.environ, **(env or {})},
                      check=check, text=True, capture_output=capture)
    return r.stdout if capture else r.returncode

def port_open(host:str, port:int, timeout=0.5)->bool:
    try:
        with socket.create_connection((host,port), timeout=timeout):
            return True
    except OSError:
        return False

def compose_services(compose_file:str, project:str|None=None) -> list[str]:
    args = ["docker","compose","-f",compose_file,"config","--services"]
    if project: args = ["docker","compose","-p",project,"-f",compose_file,"config","--services"]
    out = run(args, capture=True)
    return [s.strip() for s in out.splitlines() if s.strip()]

def compose_up(project:str, file:str, services:list[str]|None=None, profile:str|None=None, build=False, remove_orphans=True):
    args = ["docker","compose","-p",project,"-f",file,"up","-d"]
    if profile: args.insert(-1, "--profile"); args.insert(-1, profile)
    if remove_orphans: args.insert(-1,"--remove-orphans")
    if not build: args.insert(-1,"--no-build")
    if services: args += services
    return run(args)

def compose_build(project:str, file:str, services:list[str]):
    args = ["docker","compose","-p",project,"-f",file,"build"] + services
    return run(args)

def compose_down(project:str, file:str, volumes=False):
    args = ["docker","compose","-p",project,"-f",file,"down","--remove-orphans"]
    if volumes: args.append("-v")
    return run(args)

def wait_port(host, port, tries=30, sleep=1.0, label=""):
    for i in range(tries):
        if port_open(host, port): return True
        time.sleep(sleep)
    if label:
        console.print(f"[yellow]⚠ Timeout auf {label} ({host}:{port})[/]")
    return False

# ---------------- Commands ----------------

@app.command("ports")
def ports():
    "Zeigt die festgelegten Host-Ports."
    t = Table(title="InfoTerminal Ports (Host)")
    t.add_column("Service"); t.add_column("Port", justify="right")
    for k,v in PORTS.items():
        t.add_row(k, str(v))
    console.print(t)

@app.command("status")
def status(all: bool = typer.Option(False, "--all", help="Alle Projekte zeigen (main/obs/agents/gateway/opa)")):
    "Zeigt Laufstatus & wichtige Health-Ports."
    root = repo_root()
    rows = []
    def add(label, host, port):
        rows.append((label, f"{host}:{port}", "up" if port_open(host,port) else "down"))

    add("frontend","127.0.0.1",PORTS["frontend"])
    add("gateway","127.0.0.1",PORTS["gateway"])
    add("search","127.0.0.1",PORTS["search"])
    add("graph","127.0.0.1",PORTS["graph"])
    add("flowise","127.0.0.1",PORTS["flowise"])
    add("grafana","127.0.0.1",PORTS["grafana"])
    add("prometheus","127.0.0.1",PORTS["prom"])
    add("tempo","127.0.0.1",PORTS["tempo"])
    add("loki","127.0.0.1",PORTS["loki"])

    table = Table(title="Status (Port-Probes)")
    table.add_column("Service"); table.add_column("Addr"); table.add_column("State")
    for r in rows: table.add_row(*r)
    console.print(table)

    if all:
        for proj,file in [(MAIN_PROJ,MAIN_FILE),(OBS_PROJ,OBS_FILE),(AG_PROJ,AG_FILE),(GW_PROJ,GW_FILE),(OPA_PROJ,OPA_FILE)]:
            if (root/file).exists():
                print(f"[bold]docker compose ps ({proj})[/]")
                run(["docker","compose","-p",proj,"-f",file,"ps"])

@app.command("up")
def up(
    dev_local: bool = typer.Option(True, help="App-Services lokal (dev_run.sh) starten"),
    obs: bool = typer.Option(False, help="Observability-Stack starten"),
    agents: bool = typer.Option(False, help="Flowise-Connector starten"),
    gateway: bool = typer.Option(False, help="Gateway + OPA starten"),
    build_agents: bool = typer.Option(False, help="Agents-Images vor Start bauen"),
):
    """
    Startet InfoTerminal:
    - dev_local=True: nutzt scripts/dev_up.sh (versteckt Orchestrierung)
    - dev_local=False: dockerisierte App-Services (setzt Dockerfiles voraus)
    Extras: --obs, --agents, --gateway
    """
    root = repo_root()

    if dev_local:
        env = os.environ.copy()
        env.update({
            "OBS": "1" if obs else "0",
            "AGENTS": "1" if agents else "0",
            "GW": "1" if gateway else "0",
            "DEV_LOCAL": "1",
        })
        script = root/"scripts"/"dev_up.sh"
        if not script.exists():
            raise SystemExit("❌ scripts/dev_up.sh nicht gefunden")
        print("[bold]→ Dev-Mode (lokal) via scripts/dev_up.sh[/]")
        run(["bash", str(script)], env=env, check=True)
        return

    # dockerized mode
    print("[bold]→ Dockerized Mode[/]")

    # Main infra/services (nur falls vorhanden)
    services = []
    if (root/MAIN_FILE).exists():
        svcs = compose_services(MAIN_FILE)
        for s in ["opensearch","neo4j","postgres","search-api","graph-api","graph-views","entity-resolution","aleph"]:
            if s in svcs: services.append(s)
        if services:
            run(["docker","compose","-p",MAIN_PROJ,"-f",MAIN_FILE,"up","-d","--remove-orphans"] + services)

    # Observability
    if obs and (root/OBS_FILE).exists():
        compose_up(OBS_PROJ, OBS_FILE, services=["otel-collector","loki","promtail","tempo","prometheus","grafana"], profile="obs", build=False)

    # Agents
    if agents and (root/AG_FILE).exists():
        if build_agents: compose_build(AG_PROJ, AG_FILE, ["flowise-connector"])
        compose_up(AG_PROJ, AG_FILE, services=["flowise-connector"], profile="agents", build=not build_agents)

    # Gateway + OPA
    if gateway:
        if (root/OPA_FILE).exists():
            compose_up(OPA_PROJ, OPA_FILE, services=["opa"], build=False)
        if (root/GW_FILE).exists():
            env = os.environ.copy()
            env["USE_LOCAL_UPSTREAMS"] = "0"  # dockerized
            run(["docker","compose","-p",GW_PROJ,"-f",GW_FILE,"up","-d","--remove-orphans","gateway"], env=env)

@app.command("down")
def down(
    all: bool = typer.Option(False, help="Alles stoppen und entfernen"),
    obs: bool = typer.Option(False), agents: bool = typer.Option(False),
    gateway: bool = typer.Option(False), opa: bool = typer.Option(False),
    apps: bool = typer.Option(False, help="App-Services im Hauptprojekt stoppen"),
    volumes: bool = typer.Option(False, help="Mit Volumes")
):
    "Stoppt Teile oder alles."
    root = repo_root()
    if all or apps:
        if (root/MAIN_FILE).exists():
            compose_down(MAIN_PROJ, MAIN_FILE, volumes=volumes)
    if all or obs:
        if (root/OBS_FILE).exists():
            compose_down(OBS_PROJ, OBS_FILE, volumes=volumes)
    if all or agents:
        if (root/AG_FILE).exists():
            compose_down(AG_PROJ, AG_FILE, volumes=volumes)
    if all or gateway:
        if (root/GW_FILE).exists():
            compose_down(GW_PROJ, GW_FILE, volumes=volumes)
    if all or opa:
        if (root/OPA_FILE).exists():
            compose_down(OPA_PROJ, OPA_FILE, volumes=volumes)

@app.command("logs")
def logs(
    target: str = typer.Argument(..., help="z.B. grafana, prometheus, flowise-connector, gateway, opa"),
    project: str = typer.Option("auto", help="main|obs|agents|gateway|opa|auto"),
    follow: bool = typer.Option(True, "--follow/--no-follow", help="Follow logs"),
):
    "Zeigt Logs eines Dienstes (auto wählt Projekt anhand gängiger Namen)."
    def proj_for(name:str)->tuple[str,str]:
        name = name.lower()
        if project != "auto":
            pmap = {"main":MAIN_PROJ,"obs":OBS_PROJ,"agents":AG_PROJ,"gateway":GW_PROJ,"opa":OPA_PROJ}
            return pmap.get(project, MAIN_PROJ), {"main":MAIN_FILE,"obs":OBS_FILE,"agents":AG_FILE,"gateway":GW_FILE,"opa":OPA_FILE}.get(project, MAIN_FILE)
        if name in ("grafana","loki","tempo","promtail","prometheus","otel-collector"):
            return OBS_PROJ, OBS_FILE
        if name in ("flowise-connector","opa-audit-sink"):
            return AG_PROJ, AG_FILE
        if name in ("gateway",):
            return GW_PROJ, GW_FILE
        if name in ("opa",):
            return OPA_PROJ, OPA_FILE
        return MAIN_PROJ, MAIN_FILE

    proj,file = proj_for(target)
    args = ["docker","compose","-p",proj,"-f",file,"logs"]
    if follow: args.append("-f")
    args.append(target)
    os.execvp(args[0], args)

@app.command("health")
def health():
    "Pingt die wichtigsten Endpunkte."
    checks = [
        ("Frontend", f"http://localhost:{PORTS['frontend']}"),
        ("Grafana",  f"http://localhost:{PORTS['grafana']}/login"),
        ("Prometheus",f"http://localhost:{PORTS['prom']}/-/ready"),
        ("Loki",     f"http://localhost:{PORTS['loki']}/loki/api/v1/status/buildinfo"),
        ("Tempo",    f"http://localhost:{PORTS['tempo']}"),  # simple port probe
        ("Flowise",  f"http://localhost:{PORTS['flowise']}/healthz"),
        ("Gateway",  f"http://localhost:{PORTS['gateway']}/healthz"),
        ("Search",   f"http://localhost:{PORTS['search']}/healthz"),
        ("Graph",    f"http://localhost:{PORTS['graph']}/healthz"),
    ]
    table = Table(title="Health")
    table.add_column("Service"); table.add_column("URL"); table.add_column("Status")
    for name,url in checks:
        try:
            host = "localhost"; port = int(url.split(":")[-1].split("/")[0])
            ok = port_open(host, port)
            table.add_row(name, url, "up" if ok else "down")
        except Exception:
            table.add_row(name, url, "n/a")
    console.print(table)

@app.command("neo4j-reset")
def neo4j_reset(new_password: str = typer.Option("test123", help="Neues Passwort"),
                current: str = typer.Option("neo4j", help="Aktuelles Passwort ('neo4j' nach Reset)")):
    """
    Setzt das Neo4j-Passwort im Container zurück (DEV-Only).
    """
    root = repo_root()
    if not (root/MAIN_FILE).exists():
        raise SystemExit("❌ docker-compose.yml nicht gefunden")
    # sicherstellen, dass neo4j läuft
    run(["docker","compose","-p",MAIN_PROJ,"-f",MAIN_FILE,"up","-d","neo4j"])
    # alter auth ggf. entfernen (setzt login auf neo4j/neo4j zurück)
    try:
        run(["docker","compose","-p",MAIN_PROJ,"-f",MAIN_FILE,"exec","-u","root","neo4j","bash","-lc","rm -f /data/dbms/auth"], check=False)
    except Exception:
        pass
    # restart + pass setzen
    run(["docker","compose","-p",MAIN_PROJ,"-f",MAIN_FILE,"restart","neo4j"])
    time.sleep(2)
    cmd = ['docker','compose','-p',MAIN_PROJ,'-f',MAIN_FILE,'exec','neo4j','cypher-shell','-u','neo4j','-p',current,
           f'ALTER CURRENT USER SET PASSWORD FROM "{current}" TO "{new_password}"']
    run(cmd, check=True)
    print(f"[green]✓ Neo4j Passwort gesetzt: {new_password}[/]")

@app.command("agents-call")
def agents_call(agent_id: str = typer.Argument(..., help="Flowise Agent/Chat ID"),
                payload: str = typer.Option(..., "--json", help="JSON-Payload (als String)"),
                base: str = typer.Option(f"http://localhost:{PORTS['flowise']}", help="Connector Base URL")):
    """
    Ruft den Flowise-Connector auf: POST /chat/{agent_id} mit JSON-Payload.
    Beispiel:
      it agents-call abc123 --json '{"question":"Hello"}'
    """
    import urllib.request
    url = f"{base}/chat/{agent_id}"
    req = urllib.request.Request(url, data=payload.encode("utf-8"), headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read().decode("utf-8")
            print(data)
    except Exception as e:
        print(f"[red]✗ call failed:[/] {e}")

