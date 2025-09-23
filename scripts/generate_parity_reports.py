#!/usr/bin/env python3
"""Generate CLI/API parity inventory documentation.

This helper scans the repository for FastAPI routers and Typer commands to
produce three markdown reports:

* ``docs/API_INVENTORY.md`` – Service endpoints with metadata
* ``docs/CLI_INVENTORY.md`` – CLI command groups and the API paths they touch
* ``docs/PARITY_GAP_REPORT.md`` – Gaps between API endpoints and CLI coverage

The script is idempotent. Running it again will only rewrite the output files
when the generated content changes. For safety, use ``--dry-run`` to preview
updates without touching the filesystem.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import sys
import textwrap
import itertools
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
SERVICES_DIR = REPO_ROOT / "services"
CLI_DIR = REPO_ROOT / "cli" / "it_cli"
DEFAULT_API_DOC = REPO_ROOT / "docs" / "API_INVENTORY.md"
DEFAULT_CLI_DOC = REPO_ROOT / "docs" / "CLI_INVENTORY.md"
DEFAULT_GAP_DOC = REPO_ROOT / "docs" / "PARITY_GAP_REPORT.md"

HTTP_METHODS = {
    "get",
    "post",
    "put",
    "delete",
    "patch",
    "options",
    "head",
}
PATH_REGEX = re.compile(r"/(?:v\d+/)?[A-Za-z0-9_\-{}\/]+")

# Some service modules build very deep ASTs (e.g. nested JSON fixtures), so we
# gently bump the recursion limit to avoid ``RecursionError`` while walking the
# tree.
sys.setrecursionlimit(max(4000, sys.getrecursionlimit()))


@dataclass
class Endpoint:
    """Metadata about an API endpoint discovered in a service."""

    service: str
    method: str
    path: str
    source: str
    lineno: int
    router_name: str
    summary: Optional[str] = None
    status_codes: Sequence[str] = field(default_factory=list)
    response_model: Optional[str] = None


@dataclass
class CLICommand:
    """Metadata about a CLI command and the API paths it references."""

    module: str
    group: str
    name: str
    source: str
    lineno: int
    doc: Optional[str]
    params: Sequence[str]
    services: Set[str] = field(default_factory=set)
    api_paths: Set[str] = field(default_factory=set)


def read_python(path: Path) -> Optional[ast.AST]:
    """Parse ``path`` into an AST, returning ``None`` on syntax errors."""

    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):  # pragma: no cover - defensive
        return None


def is_apirouter_call(call: ast.Call) -> bool:
    func = call.func
    if isinstance(func, ast.Name):
        return func.id == "APIRouter"
    if isinstance(func, ast.Attribute):
        return func.attr == "APIRouter"
    return False


def is_fastapi_app(call: ast.Call) -> bool:
    func = call.func
    if isinstance(func, ast.Name):
        return func.id == "FastAPI"
    if isinstance(func, ast.Attribute):
        return func.attr == "FastAPI"
    return False


def literal_or_unparse(node: ast.AST) -> Optional[str]:
    """Convert ``node`` to a human readable string when possible."""

    try:
        value = ast.literal_eval(node)
    except Exception:
        try:
            return ast.unparse(node)  # type: ignore[attr-defined]
        except Exception:  # pragma: no cover
            return None
    if isinstance(value, str):
        return value
    return str(value)


def extract_path_arg(call: ast.Call) -> Optional[str]:
    """Return the first positional path argument if it is constant-like."""

    if call.args:
        return literal_or_unparse(call.args[0])
    for kw in call.keywords:
        if kw.arg == "path":
            return literal_or_unparse(kw.value)
    return None


def extract_status_codes(call: ast.Call) -> List[str]:
    codes: List[str] = []
    for kw in call.keywords:
        if kw.arg == "status_code":
            value = literal_or_unparse(kw.value)
            if value:
                codes.append(value)
        elif kw.arg == "responses":
            raw = literal_or_unparse(kw.value)
            if raw:
                codes.extend(_parse_status_codes_from_responses(raw))
    return codes


def _parse_status_codes_from_responses(raw: str) -> List[str]:
    """Extract response codes from an ``responses=`` string representation."""

    codes: List[str] = []
    for token in re.findall(r"\b[0-9]{3}\b", raw):
        codes.append(token)
    return codes


def extract_response_model(call: ast.Call) -> Optional[str]:
    for kw in call.keywords:
        if kw.arg == "response_model":
            return literal_or_unparse(kw.value)
    return None


def extract_summary(call: ast.Call, func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> Optional[str]:
    for kw in call.keywords:
        if kw.arg == "summary":
            summary = literal_or_unparse(kw.value)
            if summary:
                return summary.strip()
    doc = ast.get_docstring(func_node)
    if doc:
        return doc.strip().splitlines()[0]
    return None


def normalize_path(prefix: Optional[str], path: Optional[str]) -> Optional[str]:
    if prefix is None and path is None:
        return None
    prefix = (prefix or "").rstrip("/")
    path = (path or "").strip()
    if path == "" or path == "/":
        combined = prefix or "/"
    elif path.startswith("/"):
        combined = f"{prefix}{path}" if prefix else path
    else:
        combined = f"{prefix}/{path}" if prefix else f"/{path}"
    combined = re.sub(r"//+", "/", combined)
    if not combined.startswith("/"):
        combined = f"/{combined}"
    return combined


class RouterCollector(ast.NodeVisitor):
    """Collect APIRouter metadata within a module."""

    def __init__(self) -> None:
        self.router_prefix: Dict[str, Optional[str]] = {}
        self.router_aliases: Set[str] = set()
        self.app_names: Set[str] = set()
        self.routes: List[Tuple[str, ast.Call, ast.FunctionDef | ast.AsyncFunctionDef]] = []

    def visit_Assign(self, node: ast.Assign) -> None:  # pragma: no branch - simple matching
        if isinstance(node.value, ast.Call):
            if is_apirouter_call(node.value):
                prefix = None
                for kw in node.value.keywords:
                    if kw.arg == "prefix":
                        prefix = literal_or_unparse(kw.value)
                        break
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.router_prefix[target.id] = prefix
                        self.router_aliases.add(target.id)
            elif is_fastapi_app(node.value):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.app_names.add(target.id)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.value, ast.Call):
            if is_apirouter_call(node.value) and isinstance(node.target, ast.Name):
                prefix = None
                for kw in node.value.keywords:
                    if kw.arg == "prefix":
                        prefix = literal_or_unparse(kw.value)
                        break
                self.router_prefix[node.target.id] = prefix
                self.router_aliases.add(node.target.id)
            elif is_fastapi_app(node.value) and isinstance(node.target, ast.Name):
                self.app_names.add(node.target.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._inspect_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._inspect_function(node)

    def _inspect_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                base = decorator.func.value
                if isinstance(base, ast.Name) and base.id in self.router_aliases.union(self.app_names):
                    method = decorator.func.attr.lower()
                    if method not in HTTP_METHODS:
                        continue
                    self.routes.append((base.id, decorator, node))
        self.generic_visit(node)


def collect_service_endpoints(service_dir: Path) -> List[Endpoint]:
    endpoints: List[Endpoint] = []
    service_name = service_dir.name
    py_files = [p for p in service_dir.rglob("*.py") if "tests" not in p.parts and "__pycache__" not in p.parts]
    for path in py_files:
        tree = read_python(path)
        if not tree:
            continue
        collector = RouterCollector()
        collector.visit(tree)
        for router_name, decorator, func in collector.routes:
            raw_path = extract_path_arg(decorator)
            prefix = collector.router_prefix.get(router_name)
            full_path = normalize_path(prefix, raw_path)
            if not full_path:
                continue
            method = decorator.func.attr.upper()  # type: ignore[union-attr]
            summary = extract_summary(decorator, func)
            status_codes = extract_status_codes(decorator) or ["200"]
            response_model = extract_response_model(decorator)
            endpoint = Endpoint(
                service=service_name,
                method=method,
                path=full_path,
                source=str(path.relative_to(REPO_ROOT)),
                lineno=decorator.lineno,
                router_name=router_name,
                summary=summary,
                status_codes=status_codes,
                response_model=response_model,
            )
            endpoints.append(endpoint)
    return endpoints


def joinedstr_to_template(node: ast.JoinedStr) -> str:
    parts: List[str] = []
    for value in node.values:
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            parts.append(value.value)
        else:
            parts.append("{}")
    return "".join(parts)


def iter_string_literals(node: ast.AST) -> Iterator[str]:
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            yield child.value
        elif isinstance(child, ast.JoinedStr):
            yield joinedstr_to_template(child)


def collect_services_from_function(node: ast.AST) -> Set[str]:
    services: Set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Attribute):
            chain: List[str] = []
            current: ast.AST = child
            while isinstance(current, ast.Attribute):
                chain.append(current.attr)
                current = current.value  # type: ignore[assignment]
            if isinstance(current, ast.Name):
                chain.append(current.id)
                chain.reverse()
                if chain and chain[0] == "settings" and len(chain) >= 2:
                    service_name = chain[1].replace("_", "-")
                    services.add(service_name)
    return services


def collect_cli_commands(module_path: Path) -> List[CLICommand]:
    tree = read_python(module_path)
    if not tree:
        return []

    typer_apps: Set[str] = set()
    commands: List[CLICommand] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            value = node.value if isinstance(node, ast.Assign) else node.value
            if isinstance(value, ast.Call):
                func = value.func
                func_name = None
                if isinstance(func, ast.Name):
                    func_name = func.id
                elif isinstance(func, ast.Attribute):
                    func_name = func.attr
                if func_name == "Typer":
                    if isinstance(node, ast.Assign):
                        targets = [t for t in node.targets if isinstance(t, ast.Name)]
                    else:
                        targets = [node.target] if isinstance(node.target, ast.Name) else []
                    for target in targets:
                        if isinstance(target, ast.Name):
                            typer_apps.add(target.id)

    class CommandVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, func: ast.FunctionDef) -> None:
            self._inspect(func)

        def visit_AsyncFunctionDef(self, func: ast.AsyncFunctionDef) -> None:
            self._inspect(func)

        def _inspect(self, func: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            for decorator in func.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    base = decorator.func.value
                    if isinstance(base, ast.Name) and base.id in typer_apps and decorator.func.attr == "command":
                        if decorator.args:
                            command_name = literal_or_unparse(decorator.args[0]) or func.name
                        else:
                            command_name = func.name
                        params = [arg.arg for arg in func.args.args]
                        doc = ast.get_docstring(func)
                        strings = list(iter_string_literals(func))
                        api_paths = extract_paths_from_strings(strings)
                        services = collect_services_from_function(func)
                        commands.append(
                            CLICommand(
                                module=str(module_path.relative_to(REPO_ROOT)),
                                group=base.id,
                                name=command_name,
                                source=str(module_path.relative_to(REPO_ROOT)),
                                lineno=decorator.lineno,
                                doc=doc,
                                params=params,
                                services=services,
                                api_paths=api_paths,
                            )
                        )
            # recurse into nested definitions if any
            self.generic_visit(func)

    CommandVisitor().visit(tree)
    return commands


def extract_paths_from_strings(strings: Sequence[str]) -> Set[str]:
    paths: Set[str] = set()
    for text in strings:
        for match in PATH_REGEX.findall(text):
            paths.add(match)
    return paths


def _utc_timestamp() -> str:
    """Return an ISO-8601 timestamp in UTC with ``Z`` suffix."""

    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def generate_api_markdown(endpoints: List[Endpoint]) -> str:
    ts = _utc_timestamp()
    lines = [
        "# API Inventory",
        "",
        f"_Generated on {ts} by `scripts/generate_parity_reports.py`_",
        "",
    ]
    endpoints_by_service: Dict[str, List[Endpoint]] = {}
    for ep in endpoints:
        endpoints_by_service.setdefault(ep.service, []).append(ep)
    for service, eps in sorted(endpoints_by_service.items()):
        lines.append(f"## {service}")
        lines.append(
            "| Method | Path | Status Codes | Response Model | Summary | Source |"
        )
        lines.append("|---|---|---|---|---|---|")
        for ep in sorted(eps, key=lambda e: (e.path, e.method)):
            status = ", ".join(str(code) for code in ep.status_codes)
            response_model = ep.response_model or "—"
            summary = (ep.summary or "").replace("|", "\\|")
            source = f"{ep.source}:{ep.lineno}"
            lines.append(
                f"| {ep.method} | {ep.path} | {status or '—'} | {response_model} | {summary} | {source} |"
            )
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def generate_cli_markdown(commands: List[CLICommand]) -> str:
    ts = _utc_timestamp()
    lines = [
        "# CLI Inventory",
        "",
        f"_Generated on {ts} by `scripts/generate_parity_reports.py`_",
        "",
    ]
    commands_by_module: Dict[str, List[CLICommand]] = {}
    for cmd in commands:
        commands_by_module.setdefault(cmd.module, []).append(cmd)
    for module, cmds in sorted(commands_by_module.items()):
        group_names = {cmd.group for cmd in cmds}
        groups_fmt = ", ".join(sorted(group_names))
        lines.append(f"## {module} (groups: {groups_fmt})")
        lines.append("| Command | Description | Parameters | API Paths | Services | Source |")
        lines.append("|---|---|---|---|---|---|")
        for cmd in sorted(cmds, key=lambda c: c.name):
            desc = (cmd.doc or "").strip().splitlines()[0] if cmd.doc else ""
            desc = desc.replace("|", "\\|") or "—"
            params = ", ".join(cmd.params) or "—"
            api_paths = ", ".join(sorted(cmd.api_paths)) or "—"
            services = ", ".join(sorted(cmd.services)) or "—"
            source = f"{cmd.source}:{cmd.lineno}"
            lines.append(
                f"| {cmd.name} | {desc} | {params} | {api_paths} | {services} | {source} |"
            )
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def generate_gap_report(endpoints: List[Endpoint], commands: List[CLICommand]) -> str:
    ts = _utc_timestamp()
    lines = [
        "# API ↔ CLI Parity Gap Report",
        "",
        f"_Generated on {ts} by `scripts/generate_parity_reports.py`_",
        "",
        "This report highlights API endpoints without a matching CLI command (and vice versa).",
        "",
    ]
    endpoints_by_service: Dict[str, List[Endpoint]] = {}
    for ep in endpoints:
        endpoints_by_service.setdefault(ep.service, []).append(ep)

    cli_paths_by_service: Dict[str, Set[str]] = {}
    for cmd in commands:
        for service in cmd.services:
            cli_paths_by_service.setdefault(service, set()).update(cmd.api_paths)

    for service, eps in sorted(endpoints_by_service.items()):
        cli_paths = cli_paths_by_service.get(service, set())
        unmapped = []
        for ep in eps:
            if not cli_paths:
                unmapped.append(ep)
                continue
            if not any(_paths_match(ep.path, cli_path) for cli_path in cli_paths):
                unmapped.append(ep)
        lines.append(f"## {service}")
        lines.append(f"- Total endpoints: {len(eps)}")
        lines.append(f"- CLI-covered endpoints: {len(eps) - len(unmapped)}")
        lines.append(f"- Missing CLI coverage: {len(unmapped)}")
        if unmapped:
            lines.append("- Endpoints without CLI coverage:")
            for ep in sorted(unmapped, key=lambda e: (e.path, e.method)):
                lines.append(
                    f"  - `{ep.method}` {ep.path} ({ep.source}:{ep.lineno})"
                )
        else:
            lines.append("- All endpoints covered 🎉")
        lines.append("")

    covered_services = set(cli_paths_by_service)
    api_services = set(endpoints_by_service)
    for extra_service in sorted(covered_services - api_services):
        lines.append(f"## {extra_service}")
        lines.append("- CLI commands reference this service, but no API endpoints were discovered.")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def _paths_match(api_path: str, cli_path: str) -> bool:
    if api_path == cli_path:
        return True
    return api_path.rstrip("/") == cli_path.rstrip("/")


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.write_text(content, encoding="utf-8")


def collect_all_endpoints() -> List[Endpoint]:
    endpoints: List[Endpoint] = []
    if not SERVICES_DIR.exists():
        return endpoints
    for child in sorted(SERVICES_DIR.iterdir()):
        if child.is_dir() and not child.name.startswith("_"):
            endpoints.extend(collect_service_endpoints(child))
    return endpoints


def collect_all_cli_commands() -> List[CLICommand]:
    commands: List[CLICommand] = []
    commands_dir = CLI_DIR / "commands"
    if not commands_dir.exists():
        return commands
    for module in sorted(commands_dir.glob("*.py")):
        if module.name == "__init__.py":
            continue
        commands.extend(collect_cli_commands(module))
    return commands


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate CLI/API parity reports")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files")
    parser.add_argument("--api-doc", type=Path, default=DEFAULT_API_DOC)
    parser.add_argument("--cli-doc", type=Path, default=DEFAULT_CLI_DOC)
    parser.add_argument("--gap-doc", type=Path, default=DEFAULT_GAP_DOC)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    endpoints = collect_all_endpoints()
    commands = collect_all_cli_commands()

    api_md = generate_api_markdown(endpoints)
    cli_md = generate_cli_markdown(commands)
    gap_md = generate_gap_report(endpoints, commands)

    write_file(args.api_doc, api_md, args.dry_run)
    write_file(args.cli_doc, cli_md, args.dry_run)
    write_file(args.gap_doc, gap_md, args.dry_run)

    if args.dry_run:
        preview = textwrap.dedent(
            f"""
            == Dry-run preview ==
            API doc would be written to: {args.api_doc}
            CLI doc would be written to: {args.cli_doc}
            Gap report would be written to: {args.gap_doc}
            """
        ).strip()
        print(preview)
    else:
        print(f"Wrote {args.api_doc.relative_to(REPO_ROOT)}")
        print(f"Wrote {args.cli_doc.relative_to(REPO_ROOT)}")
        print(f"Wrote {args.gap_doc.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
