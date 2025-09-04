"""Test configuration."""
from __future__ import annotations

import pathlib
import sys

# Ensure cli package is importable
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "cli"))
