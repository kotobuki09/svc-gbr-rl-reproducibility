#!/usr/bin/env python3
"""Run the public, synthetic-only smoke test."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from svc_release.features import engineer_features
from svc_release.metrics import summarize_demo


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "public_smoke_summary.json",
        help="summary JSON output path",
    )
    args = parser.parse_args()

    config = yaml.safe_load((ROOT / "configs" / "public_smoke_test.yml").read_text(encoding="utf-8"))
    sample_path = ROOT / config["sample_path"]
    frame = pd.read_csv(sample_path)
    if len(frame) != config["expected_rows"]:
        raise ValueError(f"expected {config['expected_rows']} demo rows, found {len(frame)}")
    if set(frame["source_type"]) != {config["expected_source_type"]}:
        raise ValueError("sample contains a non-synthetic source_type")

    featured = engineer_features(frame)
    summary = summarize_demo(frame)
    summary.update(
        {
            "feature_columns": [column for column in featured.columns if column not in frame.columns],
            "config_seed": config["seed"],
            "sample_path": config["sample_path"],
        }
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
