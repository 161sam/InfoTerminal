#!/usr/bin/env python3
"""Minimal OpenBB data pull stub."""
import argparse
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--symbols", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()

symbols = args.symbols.split(",")
Path(args.out).mkdir(parents=True, exist_ok=True)
for sym in symbols:
    df = pd.DataFrame({"symbol": [sym], "price": [0]})
    df.to_csv(Path(args.out) / f"{sym}.csv", index=False)
