"""NLP and Document Processing commands."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="NLP & Document Processing")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def extract(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to analyze"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="File to analyze"),
    entities: bool = typer.Option(True, "--entities", "-e", help="Extract entities"),
    relations: bool = typer.Option(False, "--relations", "-r", help="Extract relations"),
    summary: bool = typer.Option(False, "--summary", "-s", help="Generate summary"),
) -> None:
    """Extract entities, relations, or summary from text."""
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
            # Extract entities
            if entities:
                resp = await c.post(
                    f"{settings.nlp_api}/v1/extract/entities",
                    json={"text": text}
                )
                resp.raise_for_status()
                data = resp.json()
                
                table = Table(title="Extracted Entities")
                table.add_column("Text")
                table.add_column("Type")
                table.add_column("Confidence")
                table.add_column("Start")
                table.add_column("End")
                
                for entity in data.get("entities", []):
                    table.add_row(
                        entity.get("text", ""),
                        entity.get("label", ""),
                        str(entity.get("confidence", 0)),
                        str(entity.get("start", 0)),
                        str(entity.get("end", 0)),
                    )
                
                console.print(table)
            
            # Extract relations
            if relations:
                resp = await c.post(
                    f"{settings.nlp_api}/v1/extract/relations",
                    json={"text": text}
                )
                resp.raise_for_status()
                data = resp.json()
                
                table = Table(title="Extracted Relations")
                table.add_column("Subject")
                table.add_column("Predicate")
                table.add_column("Object")
                table.add_column("Confidence")
                
                for relation in data.get("relations", []):
                    table.add_row(
                        relation.get("subject", ""),
                        relation.get("predicate", ""),
                        relation.get("object", ""),
                        str(relation.get("confidence", 0)),
                    )
                
                console.print(table)
            
            # Generate summary
            if summary:
                resp = await c.post(
                    f"{settings.nlp_api}/v1/summarize",
                    json={"text": text}
                )
                resp.raise_for_status()
                data = resp.json()
                
                console.print("\n📋 Summary:")
                console.print(data.get("summary", ""))

    _run(_action)

@app.command()
def annotate(
    file: Path = typer.Argument(..., help="Document file to annotate"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
) -> None:
    """Annotate document with NLP analysis."""
    if not file.exists():
        console.print(f"❌ File not found: {file}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        text = file.read_text(encoding="utf-8")
        
        async with client() as c:
            resp = await c.post(
                f"{settings.nlp_api}/v1/documents/annotate",
                json={"text": text, "include_entities": True, "include_relations": True}
            )
            resp.raise_for_status()
            data = resp.json()
            
            if output:
                output.write_text(data.get("annotated_text", ""), encoding="utf-8")
                console.print(f"✅ Annotated document saved to: {output}")
            else:
                console.print("📄 Annotated Document:")
                console.print(data.get("annotated_text", ""))

    _run(_action)

@app.command()
def resolve(
    entities: List[str] = typer.Argument(..., help="Entity names to resolve"),
    threshold: float = typer.Option(0.8, "--threshold", "-t", help="Similarity threshold"),
    limit: int = typer.Option(10, "--limit", "-l", help="Results limit"),
) -> None:
    """Resolve entity mentions to canonical forms."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.post(
                f"{settings.nlp_api}/v1/resolve",
                json={
                    "entities": entities,
                    "threshold": threshold,
                    "limit": limit
                }
            )
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Entity Resolution")
            table.add_column("Input")
            table.add_column("Resolved")
            table.add_column("Similarity")
            table.add_column("Type")
            
            for result in data.get("resolved", []):
                table.add_row(
                    result.get("input", ""),
                    result.get("canonical", ""),
                    str(result.get("similarity", 0)),
                    result.get("type", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def match(
    query: str = typer.Argument(..., help="Entity to match"),
    candidates: List[str] = typer.Option([], "--candidate", "-c", help="Candidate entities"),
    method: str = typer.Option("fuzzy", "--method", "-m", help="Matching method"),
    threshold: float = typer.Option(0.8, "--threshold", "-t", help="Similarity threshold"),
) -> None:
    """Match entities using fuzzy matching."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.post(
                f"{settings.nlp_api}/v1/match",
                json={
                    "query": query,
                    "candidates": candidates,
                    "method": method,
                    "threshold": threshold
                }
            )
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title=f"Fuzzy Matches for: {query}")
            table.add_column("Match")
            table.add_column("Score")
            table.add_column("Method")
            
            for match in data.get("matches", []):
                table.add_row(
                    match.get("text", ""),
                    str(match.get("score", 0)),
                    match.get("method", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def stats() -> None:
    """Show NLP service statistics."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.nlp_api}/v1/stats")
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="NLP Statistics")
            table.add_column("Metric")
            table.add_column("Value")
            
            stats = data.get("stats", {})
            for key, value in stats.items():
                table.add_row(key.replace("_", " ").title(), str(value))
            
            console.print(table)

    _run(_action)
