"""Minimal Textual TUI for infra management."""
from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def run() -> None:
    """Run the Textual TUI."""
    try:  # pragma: no cover - optional dependency
        from textual.app import App, ComposeResult
        from textual.widgets import DataTable, Footer, Header
    except Exception:  # pragma: no cover - textual not installed
        console.print("TUI not available")
        raise typer.Exit(0)

    from . import infra

    class ITUI(App):
        BINDINGS = [
            ("r", "refresh", "Refresh"),
            ("u", "up", "Up"),
            ("d", "down", "Down"),
            ("s", "status", "Status"),
            ("l", "logs", "Logs"),
            ("f", "follow_logs", "Follow"),
        ]

        def compose(self) -> ComposeResult:  # pragma: no cover - UI
            yield Header()
            self.table = DataTable(zebra_stripes=True)
            yield self.table
            yield Footer()

        async def on_mount(self) -> None:  # pragma: no cover - UI
            await self.update_status()
            self.set_interval(3, self.update_status)

        async def update_status(self) -> None:  # pragma: no cover - UI
            rows = await infra.gather_status()
            self.table.clear(columns=True)
            self.table.add_columns("Service", "Status", "Port", "Latency")
            for r in rows:
                self.table.add_row(
                    r["service"],
                    r["status"],
                    str(r.get("port", "")),
                    r.get("latency", ""),
                )

        async def action_refresh(self) -> None:  # pragma: no cover - UI
            await self.update_status()

        def action_up(self) -> None:  # pragma: no cover - UI
            infra.up()

        def action_down(self) -> None:  # pragma: no cover - UI
            infra.down()

        async def action_status(self) -> None:  # pragma: no cover - UI
            await self.update_status()

        def action_logs(self) -> None:  # pragma: no cover - UI
            if not self.table.rows:
                return
            service = str(self.table.get_row_at(self.table.cursor_row)[0])
            try:
                infra.show_logs(service, lines=200, follow=False)
            except FileNotFoundError:
                console.print(f"No logs found for {service}")

        def action_follow_logs(self) -> None:  # pragma: no cover - UI
            if not self.table.rows:
                return
            service = str(self.table.get_row_at(self.table.cursor_row)[0])
            try:
                infra.show_logs(service, lines=200, follow=True)
            except FileNotFoundError:
                console.print(f"No logs found for {service}")

    ITUI().run()
