"""Forensics and evidence management commands."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="Forensics & Evidence Management")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def ingest(
    file: Path = typer.Argument(..., help="Evidence file to ingest"),
    source: Optional[str] = typer.Option(None, "--source", "-s", help="Evidence source"),
    metadata: List[str] = typer.Option([], "--meta", "-m", help="Metadata key=value pairs"),
    chain_previous: Optional[str] = typer.Option(None, "--chain", "-c", help="Previous evidence hash"),
) -> None:
    """Ingest evidence into forensic chain."""
    if not file.exists():
        console.print(f"❌ File not found: {file}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        # Parse metadata
        meta_dict = {}
        for item in metadata:
            if "=" not in item:
                console.print(f"❌ Invalid metadata format: {item}")
                continue
            key, value = item.split("=", 1)
            meta_dict[key.strip()] = value.strip()

        # Read file content
        file_content = file.read_bytes()
        
        async with client() as c:
            # Use multipart form data for file upload
            files = {"file": (file.name, file_content)}
            data = {
                "source": source or str(file),
                "metadata": meta_dict
            }
            if chain_previous:
                data["previous_hash"] = chain_previous
                
            resp = await c.post(
                f"{settings.forensics_api}/v1/evidence/ingest",
                files=files,
                data=data
            )
            resp.raise_for_status()
            result = resp.json()
            
            console.print(f"✅ Evidence ingested")
            console.print(f"Hash: {result.get('evidence_hash')}")
            console.print(f"Chain Position: {result.get('chain_position')}")
            console.print(f"Timestamp: {result.get('timestamp')}")

    _run(_action)

@app.command()
def verify(
    evidence_hash: str = typer.Argument(..., help="Evidence hash to verify"),
    check_chain: bool = typer.Option(True, "--chain", "-c", help="Verify entire chain"),
) -> None:
    """Verify evidence integrity."""
    settings = get_settings()

    async def _action():
        payload = {
            "evidence_hash": evidence_hash,
            "verify_chain": check_chain
        }
        
        async with client() as c:
            resp = await c.post(
                f"{settings.forensics_api}/v1/evidence/verify",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"🔍 Verification: {evidence_hash}")
            console.print(f"Valid: {'✅' if data.get('valid', False) else '❌'}")
            console.print(f"Chain Valid: {'✅' if data.get('chain_valid', False) else '❌'}")
            
            if data.get("details"):
                table = Table(title="Verification Details")
                table.add_column("Check")
                table.add_column("Status")
                table.add_column("Details")
                
                for check, result in data.get("details", {}).items():
                    status = "✅" if result.get("valid", False) else "❌"
                    table.add_row(
                        check.replace("_", " ").title(),
                        status,
                        result.get("message", ""),
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def receipt(
    evidence_hash: str = typer.Argument(..., help="Evidence hash"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
) -> None:
    """Generate cryptographic receipt for evidence."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.forensics_api}/v1/evidence/{evidence_hash}/receipt")
            resp.raise_for_status()
            data = resp.json()
            
            if output:
                import json
                output.write_text(json.dumps(data, indent=2), encoding="utf-8")
                console.print(f"✅ Receipt saved to: {output}")
            else:
                console.print("📜 Cryptographic Receipt:")
                console.print_json(data=data)

    _run(_action)

@app.command()
def chain(
    start_hash: Optional[str] = typer.Option(None, "--start", "-s", help="Start from hash"),
    limit: int = typer.Option(50, "--limit", "-l", help="Results limit"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table|json"),
) -> None:
    """Show evidence chain."""
    settings = get_settings()

    async def _action():
        params = {"limit": limit}
        if start_hash:
            params["start_hash"] = start_hash
            
        async with client() as c:
            resp = await c.get(f"{settings.forensics_api}/v1/chain/report", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            if format == "json":
                console.print_json(data=data)
            else:
                table = Table(title="Evidence Chain")
                table.add_column("Position")
                table.add_column("Hash")
                table.add_column("Source")
                table.add_column("Timestamp")
                table.add_column("Size")
                
                for item in data.get("chain", []):
                    table.add_row(
                        str(item.get("position", "")),
                        item.get("hash", "")[:16] + "...",
                        item.get("source", "")[:30],
                        item.get("timestamp", ""),
                        str(item.get("size_bytes", 0)),
                    )
                
                console.print(table)
                console.print(f"Chain Length: {data.get('chain_length', 0)}")
                console.print(f"Valid: {'✅' if data.get('chain_valid', False) else '❌'}")

    _run(_action)

@app.command()
def list(
    source: Optional[str] = typer.Option(None, "--source", "-s", help="Filter by source"),
    start_date: Optional[str] = typer.Option(None, "--from", help="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, "--to", help="End date (YYYY-MM-DD)"),
    limit: int = typer.Option(20, "--limit", "-l", help="Results limit"),
) -> None:
    """List evidence entries."""
    settings = get_settings()

    async def _action():
        params = {"limit": limit}
        if source:
            params["source"] = source
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
            
        async with client() as c:
            resp = await c.get(f"{settings.forensics_api}/v1/evidence", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title=f"Evidence Entries ({data.get('total', 0)})")
            table.add_column("Hash")
            table.add_column("Source")
            table.add_column("Size")
            table.add_column("Timestamp")
            table.add_column("Chain Pos")
            
            for item in data.get("items", []):
                table.add_row(
                    item.get("hash", "")[:16] + "...",
                    item.get("source", "")[:30],
                    str(item.get("size_bytes", 0)),
                    item.get("timestamp", ""),
                    str(item.get("chain_position", "")),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def integrity(
    start_hash: Optional[str] = typer.Option(None, "--start", "-s", help="Start from hash"),
    full_check: bool = typer.Option(False, "--full", "-f", help="Full integrity check"),
) -> None:
    """Check chain integrity."""
    settings = get_settings()

    async def _action():
        payload = {"full_check": full_check}
        if start_hash:
            payload["start_hash"] = start_hash
            
        async with client() as c:
            resp = await c.post(
                f"{settings.forensics_api}/v1/chain/integrity",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print("🔗 Chain Integrity Check")
            console.print(f"Valid: {'✅' if data.get('valid', False) else '❌'}")
            console.print(f"Checked: {data.get('checked_count', 0)} entries")
            console.print(f"Errors: {len(data.get('errors', []))}")
            
            if data.get("errors"):
                table = Table(title="Integrity Errors")
                table.add_column("Position")
                table.add_column("Hash")
                table.add_column("Error")
                
                for error in data.get("errors", []):
                    table.add_row(
                        str(error.get("position", "")),
                        error.get("hash", "")[:16] + "...",
                        error.get("message", ""),
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def export(
    output_dir: Path = typer.Argument(..., help="Output directory"),
    evidence_hash: Optional[str] = typer.Option(None, "--hash", "-h", help="Specific evidence hash"),
    format: str = typer.Option("json", "--format", "-f", help="Export format: json|csv"),
    include_files: bool = typer.Option(False, "--files", help="Include evidence files"),
) -> None:
    """Export evidence data."""
    settings = get_settings()

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    async def _action():
        payload = {
            "format": format,
            "include_files": include_files
        }
        if evidence_hash:
            payload["evidence_hash"] = evidence_hash
            
        async with client() as c:
            resp = await c.post(
                f"{settings.forensics_api}/v1/evidence/export",
                json=payload
            )
            resp.raise_for_status()
            
            # Handle different response types
            if resp.headers.get("content-type", "").startswith("application/json"):
                data = resp.json()
                export_file = output_dir / f"evidence_export.{format}"
                
                if format == "json":
                    import json
                    export_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
                else:
                    export_file.write_text(str(data), encoding="utf-8")
                
                console.print(f"✅ Evidence exported to: {export_file}")
            else:
                # Binary/zip response
                export_file = output_dir / "evidence_export.zip"
                export_file.write_bytes(resp.content)
                console.print(f"✅ Evidence archive saved to: {export_file}")

    _run(_action)

@app.command()
def stats() -> None:
    """Show forensics statistics."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.forensics_api}/v1/stats")
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Forensics Statistics")
            table.add_column("Metric")
            table.add_column("Value")
            
            stats = data.get("stats", {})
            for key, value in stats.items():
                table.add_row(key.replace("_", " ").title(), str(value))
            
            console.print(table)

    _run(_action)
