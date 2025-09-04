"""Search commands."""
from __future__ import annotations

import asyncio

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client
from ..renderers.charts import line

app = typer.Typer()
console = Console()


@app.command()
def query(q: str, sort: str = "relevance", limit: int = 20, chart: bool = False) -> None:
    """Run a search query against search-api."""
    settings = get_settings()

    async def _run():
        async with client() as c:
            url = f"{settings.search_api}/search"
            r = await c.get(url, params={"q": q, "sort": sort, "limit": limit})
            r.raise_for_status()
            data = r.json()
            rows = data.get("hits") or data.get("items") or []
            table = Table(title=f"Search: {q} ({len(rows)})")
            table.add_column("Title")
            table.add_column("Score")
            table.add_column("Date")
            scores: list[float] = []
            for item in rows:
                title = item.get("title") or item.get("id", "<no-title>")
                score = item.get("score") or item.get("_score") or 0
                date = item.get("date") or ""
                scores.append(float(score))
                table.add_row(str(title), str(score), str(date))
            console.print(table)
            if chart and scores:
                line(scores[:50])

    asyncio.run(_run())
