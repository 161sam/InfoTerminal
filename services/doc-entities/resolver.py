"""Background entity resolver skeleton.

Future implementation will pull pending entities from the database and
resolve them against Neo4j. The functions here are stubs so that the API
can schedule work without crashing.
"""
from typing import Iterable


def resolve_entities(entity_ids: Iterable[str]) -> None:
    """Placeholder resolver.

    Parameters
    ----------
    entity_ids: Iterable[str]
        IDs of entities that should be resolved. The current implementation
        is a no-op and simply exists so that future workers can hook in.
    """
    # TODO: implement resolver logic in v0.1.0
    for _ in entity_ids:
        pass
