"""InfoTerminal CLI package."""
__all__ = ["get_version"]


def get_version() -> str:
    """Return the CLI version from environment or fallback."""
    import os

    return os.environ.get("IT_VERSION", "dev")
