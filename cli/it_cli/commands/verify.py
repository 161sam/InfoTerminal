"""Verification and Fact-Checking commands."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="Verification & Fact-Checking")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def extract(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to analyze"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="File to analyze"),
    batch: bool = typer.Option(False, "--batch", "-b", help="Batch processing"),
) -> None:
    """Extract claims from text."""
    if not text and not file:
        console.print("❌ Either --text or --file must be provided")
        raise typer.Exit(1)
    
    if file and not file.exists():
        console.print(f"❌ File not found: {file}")
        raise typer.Exit(1)

    settings = get_settings()
    
    # Read text from file if provided
    if file:
        text = file.read_text(encoding="utf-8")

    async def _action():
        async with client() as c:
            endpoint = "/v1/claims/batch" if batch else "/v1/claims/extract"
            resp = await c.post(
                f"{settings.verification_api}{endpoint}",
                json={"text": text}
            )
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Extracted Claims")
            table.add_column("Claim")
            table.add_column("Confidence")
            table.add_column("Type")
            table.add_column("Source")
            
            for claim in data.get("claims", []):
                table.add_row(
                    claim.get("text", ""),
                    str(claim.get("confidence", 0)),
                    claim.get("type", ""),
                    claim.get("source", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def evidence(
    claim: str = typer.Argument(..., help="Claim to find evidence for"),
    sources: List[str] = typer.Option([], "--source", "-s", help="Evidence sources"),
    limit: int = typer.Option(10, "--limit", "-l", help="Results limit"),
) -> None:
    """Find evidence for a claim."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.post(
                f"{settings.verification_api}/v1/evidence/find",
                json={
                    "claim": claim,
                    "sources": sources,
                    "limit": limit
                }
            )
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title=f"Evidence for: {claim}")
            table.add_column("Evidence")
            table.add_column("Relevance")
            table.add_column("Source")
            table.add_column("URL")
            
            for evidence in data.get("evidence", []):
                table.add_row(
                    evidence.get("text", "")[:100] + "...",
                    str(evidence.get("relevance_score", 0)),
                    evidence.get("source", ""),
                    evidence.get("url", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def stance(
    claim: str = typer.Argument(..., help="Claim to classify"),
    evidence: List[str] = typer.Option([], "--evidence", "-e", help="Evidence texts"),
) -> None:
    """Classify stance between claim and evidence."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.post(
                f"{settings.verification_api}/v1/stance/classify",
                json={
                    "claim": claim,
                    "evidence": evidence
                }
            )
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Stance Classification")
            table.add_column("Evidence")
            table.add_column("Stance")
            table.add_column("Confidence")
            table.add_column("Reasoning")
            
            for result in data.get("classifications", []):
                table.add_row(
                    result.get("evidence", "")[:50] + "...",
                    result.get("stance", ""),
                    str(result.get("confidence", 0)),
                    result.get("reasoning", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def credibility(
    source: str = typer.Argument(..., help="Source to assess"),
    content: Optional[str] = typer.Option(None, "--content", "-c", help="Content to analyze"),
) -> None:
    """Assess credibility of a source."""
    settings = get_settings()

    async def _action():
        payload = {"source": source}
        if content:
            payload["content"] = content
            
        async with client() as c:
            resp = await c.post(
                f"{settings.verification_api}/v1/credibility/assess",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"🔍 Credibility Assessment: {source}")
            console.print(f"Score: {data.get('credibility_score', 0)}")
            console.print(f"Rating: {data.get('rating', 'Unknown')}")
            console.print(f"Factors: {', '.join(data.get('factors', []))}")
            console.print(f"Reasoning: {data.get('reasoning', '')}")

    _run(_action)

@app.command()
def verify(
    claim: str = typer.Argument(..., help="Claim to verify"),
    auto_evidence: bool = typer.Option(True, "--auto-evidence", "-a", help="Auto-find evidence"),
    sources: List[str] = typer.Option([], "--source", "-s", help="Evidence sources"),
) -> None:
    """Complete verification pipeline for a claim."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.post(
                f"{settings.verification_api}/v1/pipeline/verify",
                json={
                    "claim": claim,
                    "auto_evidence": auto_evidence,
                    "sources": sources
                }
            )
            resp.raise_for_status()
            data = resp.json()
            
            # Show verification result
            result = data.get("verification_result", {})
            console.print(f"🔍 Claim: {claim}")
            console.print(f"📊 Verdict: {result.get('verdict', 'Unknown')}")
            console.print(f"📈 Confidence: {result.get('confidence', 0)}")
            console.print(f"🔗 Evidence Count: {len(result.get('evidence', []))}")
            
            # Show evidence summary
            if result.get("evidence"):
                table = Table(title="Supporting Evidence")
                table.add_column("Evidence")
                table.add_column("Stance")
                table.add_column("Source")
                
                for evidence in result.get("evidence", [])[:5]:  # Top 5
                    table.add_row(
                        evidence.get("text", "")[:80] + "...",
                        evidence.get("stance", ""),
                        evidence.get("source", ""),
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def media(
    file: Path = typer.Argument(..., help="Media file to analyze"),
    compare_with: Optional[Path] = typer.Option(None, "--compare", "-c", help="Compare with another file"),
) -> None:
    """Analyze media files for verification."""
    if not file.exists():
        console.print(f"❌ File not found: {file}")
        raise typer.Exit(1)
    
    if compare_with and not compare_with.exists():
        console.print(f"❌ Compare file not found: {compare_with}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        # Read file content
        file_content = file.read_bytes()
        
        async with client() as c:
            if compare_with:
                # Compare two media files
                compare_content = compare_with.read_bytes()
                resp = await c.post(
                    f"{settings.verification_api}/v1/media/compare",
                    files={
                        "file1": (file.name, file_content),
                        "file2": (compare_with.name, compare_content)
                    }
                )
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"📷 Media Comparison")
                console.print(f"Similarity: {data.get('similarity_score', 0)}")
                console.print(f"Match: {data.get('is_match', False)}")
                console.print(f"Analysis: {data.get('analysis', '')}")
            else:
                # Analyze single media file
                resp = await c.post(
                    f"{settings.verification_api}/v1/media/analyze",
                    files={"file": (file.name, file_content)}
                )
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"📷 Media Analysis: {file.name}")
                console.print_json(data=data)

    _run(_action)

@app.command()
def sources() -> None:
    """List available evidence sources."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.verification_api}/v1/sources")
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Evidence Sources")
            table.add_column("Name")
            table.add_column("Type")
            table.add_column("Reliability")
            table.add_column("Status")
            
            for source in data.get("sources", []):
                table.add_row(
                    source.get("name", ""),
                    source.get("type", ""),
                    str(source.get("reliability_score", 0)),
                    source.get("status", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def stats() -> None:
    """Show verification statistics."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.verification_api}/v1/stats")
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Verification Statistics")
            table.add_column("Metric")
            table.add_column("Value")
            
            stats = data.get("stats", {})
            for key, value in stats.items():
                table.add_row(key.replace("_", " ").title(), str(value))
            
            console.print(table)

    _run(_action)
