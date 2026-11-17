#!/usr/bin/env python3
"""Deterministic log-quantile forecast for GTA VI Twitch category viewers."""

import glob
import json
import math
import os
from pathlib import Path


# UTC hour-of-day multiplier, indexed 0..23. Comparable launches support an
# overnight trough and a sustained North American evening plateau.
SHAPE = (
    1.00, 0.88, 0.79, 0.77, 0.79, 0.84, 0.89, 0.94,
    0.96, 0.98, 1.01, 1.06, 1.15, 1.31, 1.53, 1.76,
    1.98, 2.17, 2.31, 2.38, 2.35, 2.27, 2.13, 1.96,
)

LEVELS = (0.05, 0.25, 0.50, 0.75, 0.95)
Z = (-1.645, -0.674, 0.0, 0.674, 1.645)


def read_cases(folder):
    paths = sorted(glob.glob(str(Path(folder) / "*.in")))
    if not paths:
        raise ValueError("no .in case files found")
    return [(Path(path).stem, json.loads(Path(path).read_text())) for path in paths]


def forecast(case):
    first = case.get("known")
    if isinstance(first, list):
        first = next((row for row in first if row.get("hour") == 1), None)
    if not isinstance(first, dict):
        raise ValueError("missing hour-1 print")
    anchor = max(1.0, float(first["viewers"]))
    rows = []

    for item in case.get("forecast", []):
        hour = int(item["hour"])
        utc_hour = (hour - 1) % 24
        median = anchor * SHAPE[utc_hour]

        # Uncertainty grows with forecast distance and is widest across the
        # launch's regional hand-off, where the comparable curves disagree.
        horizon = hour - 1
        peak_bump = 0.045 if 13 <= utc_hour <= 22 else 0.0
        spread = 0.205 + 0.020 * math.sqrt(horizon) + peak_bump
        quantiles = [median * math.exp(z * spread) for z in Z]
        quantiles = [min(1_000_000_000.0, max(0.01, value)) for value in quantiles]
        rows.append({"hour": hour, "q": quantiles})

    if len(rows) != 23:
        raise ValueError("forecast must contain exactly 23 hours")
    return {"hours": rows}


def main():
    input_dir = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    for case_id, case in read_cases(input_dir):
        result = forecast(case)
        target = output_dir / f"{case_id}.out"
        target.write_text(json.dumps(result, separators=(",", ":"), allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
