"""Graph rendering helpers."""
from __future__ import annotations

from rich.console import Console
from rich.tree import Tree


def adjacency_tree(adj: dict[str, list[str]], root: str | None = None) -> None:
    """Print a small adjacency tree using Rich."""
    console = Console()
    if not root:
        root = next(iter(adj)) if adj else "graph"
    tree = Tree(root)

    def add(node: str, branch: Tree) -> None:
        for nb in adj.get(node, []):
            child = branch.add(nb)
            # no recursion for demo; could add cycle guard

    add(root, tree)
    console.print(tree)
