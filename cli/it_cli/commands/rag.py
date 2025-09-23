"""RAG (Retrieval-Augmented Generation) commands."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="RAG & Document Retrieval")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    method: str = typer.Option("hybrid", "--method", "-m", help="Search method: text|vector|hybrid"),
    limit: int = typer.Option(10, "--limit", "-l", help="Results limit"),
    threshold: float = typer.Option(0.7, "--threshold", "-t", help="Relevance threshold"),
) -> None:
    """Search documents using various RAG methods."""
    settings = get_settings()

    async def _action():
        endpoint_map = {
            "text": "/v1/documents/search",
            "vector": "/v1/documents/knn", 
            "hybrid": "/v1/documents/hybrid"
        }
        
        endpoint = endpoint_map.get(method, "/v1/documents/hybrid")
        
        async with client() as c:
            resp = await c.post(
                f"{settings.rag_api}{endpoint}",
                json={
                    "query": query,
                    "limit": limit,
                    "threshold": threshold
                }
            )
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title=f"Search Results ({method.upper()})")
            table.add_column("Document")
            table.add_column("Score")
            table.add_column("Source")
            table.add_column("Summary")
            
            for doc in data.get("documents", []):
                table.add_row(
                    doc.get("title", doc.get("id", ""))[:50],
                    str(doc.get("score", 0))[:6],
                    doc.get("source", "")[:20],
                    doc.get("content", "")[:100] + "...",
                )
            
            console.print(table)

    _run(_action)

@app.command()
def embed(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to embed"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="File to embed"),
    model: str = typer.Option("default", "--model", "-m", help="Embedding model"),
) -> None:
    """Generate embeddings for text."""
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
            resp = await c.post(
                f"{settings.rag_api}/v1/embed",
                json={
                    "text": text,
                    "model": model
                }
            )
            resp.raise_for_status()
            data = resp.json()
            
            embedding = data.get("embedding", [])
            console.print(f"📊 Embedding generated")
            console.print(f"Dimensions: {len(embedding)}")
            console.print(f"Model: {data.get('model', model)}")
            console.print(f"Preview: {embedding[:10]}...")

    _run(_action)

@app.command()
def retrieve(
    query: str = typer.Argument(..., help="Retrieval query"),
    entity: Optional[str] = typer.Option(None, "--entity", "-e", help="Target entity"),
    context_size: int = typer.Option(3, "--context", "-c", help="Context window size"),
    include_graph: bool = typer.Option(False, "--graph", "-g", help="Include graph context"),
) -> None:
    """Retrieve contextual information."""
    settings = get_settings()

    async def _action():
        if entity:
            # Entity-specific context retrieval
            async with client() as c:
                resp = await c.get(
                    f"{settings.rag_api}/v1/entities/{entity}/context",
                    params={
                        "query": query,
                        "context_size": context_size,
                        "include_graph": include_graph
                    }
                )
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"🎯 Context for entity: {entity}")
                console.print(f"Query: {query}")
                
                table = Table(title="Contextual Information")
                table.add_column("Type")
                table.add_column("Content")
                table.add_column("Relevance")
                
                for item in data.get("context", []):
                    table.add_row(
                        item.get("type", ""),
                        item.get("content", "")[:100] + "...",
                        str(item.get("relevance", 0)),
                    )
                
                console.print(table)
        else:
            # General document retrieval
            async with client() as c:
                resp = await c.post(
                    f"{settings.rag_api}/v1/retrieve",
                    json={
                        "query": query,
                        "context_size": context_size
                    }
                )
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"📄 Retrieved Documents")
                console.print_json(data=data)

    _run(_action)

@app.command()
def rag(
    question: str = typer.Argument(..., help="Question to answer"),
    context_docs: int = typer.Option(5, "--docs", "-d", help="Number of context documents"),
    model: str = typer.Option("default", "--model", "-m", help="LLM model to use"),
    temperature: float = typer.Option(0.7, "--temperature", "-temp", help="Generation temperature"),
) -> None:
    """Run complete RAG pipeline (Retrieve + Generate)."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.post(
                f"{settings.rag_api}/v1/rag",
                json={
                    "question": question,
                    "context_docs": context_docs,
                    "model": model,
                    "temperature": temperature
                }
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"❓ Question: {question}")
            console.print(f"🤖 Answer: {data.get('answer', '')}")
            console.print(f"📚 Sources: {len(data.get('sources', []))}")
            
            # Show sources
            if data.get("sources"):
                table = Table(title="Sources")
                table.add_column("Document")
                table.add_column("Relevance")
                table.add_column("Excerpt")
                
                for source in data.get("sources", []):
                    table.add_row(
                        source.get("title", "")[:40],
                        str(source.get("relevance", 0)),
                        source.get("excerpt", "")[:80] + "...",
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def index(
    file: Path = typer.Argument(..., help="Document file to index"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Document title"),
    source: Optional[str] = typer.Option(None, "--source", "-s", help="Document source"),
    metadata: List[str] = typer.Option([], "--meta", "-m", help="Metadata key=value pairs"),
) -> None:
    """Index document for RAG retrieval."""
    if not file.exists():
        console.print(f"❌ File not found: {file}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        text = file.read_text(encoding="utf-8")
        
        # Parse metadata
        meta_dict = {}
        for item in metadata:
            if "=" not in item:
                console.print(f"❌ Invalid metadata format: {item}")
                continue
            key, value = item.split("=", 1)
            meta_dict[key.strip()] = value.strip()
        
        async with client() as c:
            resp = await c.post(
                f"{settings.rag_api}/v1/documents",
                json={
                    "content": text,
                    "title": title or file.name,
                    "source": source or str(file),
                    "metadata": meta_dict
                }
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"✅ Document indexed")
            console.print(f"ID: {data.get('id')}")
            console.print(f"Chunks: {data.get('chunk_count', 0)}")

    _run(_action)

@app.command()
def graph(
    entity: Optional[str] = typer.Option(None, "--entity", "-e", help="Entity to explore"),
    depth: int = typer.Option(2, "--depth", "-d", help="Graph traversal depth"),
    limit: int = typer.Option(50, "--limit", "-l", help="Results limit"),
) -> None:
    """Explore graph-based document relationships."""
    settings = get_settings()

    async def _action():
        params = {"depth": depth, "limit": limit}
        if entity:
            params["entity"] = entity
            
        async with client() as c:
            resp = await c.get(
                f"{settings.rag_api}/v1/graph/documents",
                params=params
            )
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Graph Document Relationships")
            table.add_column("Document")
            table.add_column("Connections")
            table.add_column("Centrality")
            table.add_column("Topics")
            
            for doc in data.get("documents", []):
                topics = ", ".join(doc.get("topics", [])[:3])
                table.add_row(
                    doc.get("title", "")[:40],
                    str(doc.get("connection_count", 0)),
                    str(doc.get("centrality_score", 0)),
                    topics,
                )
            
            console.print(table)

    _run(_action)

@app.command()
def events(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to analyze"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="File to analyze"),
    event_types: List[str] = typer.Option([], "--type", help="Event types to extract"),
) -> None:
    """Extract events from text."""
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
        payload = {"text": text}
        if event_types:
            payload["event_types"] = event_types
            
        async with client() as c:
            resp = await c.post(
                f"{settings.rag_api}/v1/events/extract",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Extracted Events")
            table.add_column("Event")
            table.add_column("Type")
            table.add_column("Date")
            table.add_column("Entities")
            table.add_column("Confidence")
            
            for event in data.get("events", []):
                entities = ", ".join(event.get("entities", [])[:3])
                table.add_row(
                    event.get("description", "")[:50],
                    event.get("type", ""),
                    event.get("date", ""),
                    entities,
                    str(event.get("confidence", 0)),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def feedback(
    query: str = typer.Argument(..., help="Original query"),
    result_id: str = typer.Argument(..., help="Result ID"),
    rating: int = typer.Argument(..., help="Rating (1-5)"),
    comment: Optional[str] = typer.Option(None, "--comment", "-c", help="Feedback comment"),
) -> None:
    """Provide feedback on RAG results."""
    if not 1 <= rating <= 5:
        console.print("❌ Rating must be between 1 and 5")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.post(
                f"{settings.rag_api}/v1/feedback",
                json={
                    "query": query,
                    "result_id": result_id,
                    "rating": rating,
                    "comment": comment
                }
            )
            resp.raise_for_status()
            console.print("✅ Feedback submitted")

    _run(_action)

@app.command()
def stats() -> None:
    """Show RAG service statistics."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.rag_api}/v1/stats")
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="RAG Statistics")
            table.add_column("Metric")
            table.add_column("Value")
            
            stats = data.get("stats", {})
            for key, value in stats.items():
                table.add_row(key.replace("_", " ").title(), str(value))
            
            console.print(table)

    _run(_action)
