#!/usr/bin/env python3
"""Audit the public repository boundary before a release or archive."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


REQUIRED_FILES = (
    "README.md",
    "CITATION.cff",
    "LICENSE-CODE",
    "LICENSE-DATA",
    "data/sample/svc_demo_synthetic.csv",
    "data/schema/data_dictionary.csv",
    "data/schema/data_lineage.yml",
    "docs/DATA_CARD.md",
    "docs/DATA_ACCESS.md",
    "docs/LIMITATIONS.md",
    "docs/REPRODUCIBILITY.md",
    "docs/reviewer-data-note.md",
    "results/aggregate_metrics.csv",
    "results/ablation_summary.csv",
    "results/figure_manifest.csv",
    "scripts/run_public_smoke_test.py",
)

FORBIDDEN_BASENAMES = {
    "bsl.csv",
    "augmented_dataset.csv",
    "bang so lieu.xls",
    "real_time_svc_control.zip",
}
FORBIDDEN_EXTENSIONS = {".xlsx", ".xls", ".zip", ".docx", ".pdf", ".log", ".pkl", ".joblib", ".h5"}
FORBIDDEN_DIRECTORY_NAMES = {"raw", "private", "restricted"}
IGNORED_DIRECTORIES = {".git", ".pytest_cache", "__pycache__", ".superpowers"}


def _iter_public_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRECTORIES for part in relative.parts):
            continue
        yield path, relative


def audit_public_release(root: Path) -> dict[str, Any]:
    """Return a machine-readable release audit report."""

    root = Path(root)
    missing = [relative for relative in REQUIRED_FILES if not (root / relative).is_file()]
    forbidden: list[str] = []
    for path, relative in _iter_public_files(root):
        lower_name = path.name.lower()
        if lower_name in FORBIDDEN_BASENAMES or path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            forbidden.append(relative.as_posix())
        if any(part.lower() in FORBIDDEN_DIRECTORY_NAMES for part in relative.parts[:-1]):
            forbidden.append(relative.as_posix())

    content_violations: list[str] = []
    readme_path = root / "README.md"
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8").lower()
        required_phrases = {
            "internal benchmark": "README must state internal benchmark scope",
            "independent out-of-sample generalization": "README must reject unsupported generalization claims",
            "synthetic demonstration": "README must explain the synthetic sample",
            "data_access.md": "README must link the access policy",
        }
        for phrase, message in required_phrases.items():
            if phrase not in readme:
                content_violations.append(message)

    sample_path = root / "data/sample/svc_demo_synthetic.csv"
    if sample_path.is_file():
        sample = pd.read_csv(sample_path)
        if set(sample.get("source_type", [])) != {"synthetic_demo"}:
            content_violations.append("public sample must contain only source_type=synthetic_demo")
        if len(sample) > 64:
            content_violations.append("public sample must remain small (64 rows or fewer)")

    lineage_path = root / "data/schema/data_lineage.yml"
    if lineage_path.is_file():
        lineage = yaml.safe_load(lineage_path.read_text(encoding="utf-8")) or {}
        public_sample = lineage.get("public_sample", {})
        if public_sample.get("is_real_data_subset") is not False:
            content_violations.append("lineage must state that the public sample is not real data")
        for layer_name, layer in lineage.get("paper_data_layers", {}).items():
            if layer.get("public") is not False:
                content_violations.append(f"paper data layer must remain restricted: {layer_name}")
            if layer.get("status") != "pending_author_confirmation":
                content_violations.append(f"unconfirmed layer status must remain explicit: {layer_name}")

    return {
        "root": str(root),
        "required_files_missing": sorted(set(missing)),
        "forbidden_paths": sorted(set(forbidden)),
        "content_violations": sorted(set(content_violations)),
        "passed": not (missing or forbidden or content_violations),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = audit_public_release(args.root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
