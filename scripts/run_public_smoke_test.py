#!/usr/bin/env python3
"""Run the public, synthetic-only smoke test."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd
import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from svc_release.demo_data import validate_demo_frame
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
    parser.add_argument(
        "--features-output",
        type=Path,
        help="optional CSV path for regenerated public demo features",
    )
    args = parser.parse_args()

    config = yaml.safe_load((ROOT / "configs" / "public_smoke_test.yml").read_text(encoding="utf-8"))
    sample_path = ROOT / config["sample_path"]
    frame = pd.read_csv(sample_path)
    validate_demo_frame(frame)
    if len(frame) != config["expected_rows"]:
        raise ValueError(f"expected {config['expected_rows']} demo rows, found {len(frame)}")
    if set(frame["source_type"]) != {config["expected_source_type"]}:
        raise ValueError("sample contains a non-synthetic source_type")

    featured = engineer_features(frame)
    summary = summarize_demo(frame)
    file_checksum = hashlib.sha256(sample_path.read_bytes()).hexdigest()
    lineage = yaml.safe_load((ROOT / "data" / "schema" / "data_lineage.yml").read_text(encoding="utf-8"))
    expected_checksum = lineage["public_sample"].get("sha256")
    if expected_checksum and file_checksum != expected_checksum:
        raise ValueError("public sample checksum does not match data_lineage.yml")
    summary.update(
        {
            "feature_columns": [column for column in featured.columns if column not in frame.columns],
            "config_seed": config["seed"],
            "sample_path": config["sample_path"],
            "file_checksum_sha256": file_checksum,
        }
    )

    if args.features_output:
        args.features_output.parent.mkdir(parents=True, exist_ok=True)
        featured.to_csv(args.features_output, index=False, lineterminator="\n")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
