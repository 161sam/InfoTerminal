"""Analytics and KPI commands."""
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
def kpis(chart: bool = False) -> None:
    """Fetch KPIs from analytics endpoint and display them."""
    settings = get_settings()

    async def _run():
        async with client() as c:
            data = {"kpis": []}
            try:
                r = await c.get(f"{settings.views_api}/analytics/kpis")
                r.raise_for_status()
                data = r.json()
            except Exception:
                pass
            table = Table(title="KPIs")
            table.add_column("Name")
            table.add_column("Value")
            values: list[float] = []
            for kpi in data.get("kpis", []):
                values.append(float(kpi.get("value", 0)))
                table.add_row(str(kpi.get("name")), str(kpi.get("value")))
            console.print(table)
            if chart and values:
                line(values)

    asyncio.run(_run())
