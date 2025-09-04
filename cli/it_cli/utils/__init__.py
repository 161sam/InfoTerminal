from __future__ import annotations

import typer


class NaturalOrderGroup(typer.core.TyperGroup):
    """Typer group preserving command registration order."""

    def list_commands(self, ctx: typer.Context) -> list[str]:  # pragma: no cover - simple override
        return list(self.commands.keys())
