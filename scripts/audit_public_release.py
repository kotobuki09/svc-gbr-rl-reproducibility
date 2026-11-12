#!/usr/bin/env python3
"""Audit the public repository boundary before a release or archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


REQUIRED_FILES = (
    "README.md",
    "CITATION.cff",
    "LICENSE-CODE",
    "LICENSE-DATA",
    ".gitattributes",
    "data/sample/svc_demo_synthetic.csv",
    "data/schema/data_dictionary.csv",
    "data/schema/data_lineage.yml",
    "data/schema/checksums.sha256",
    "docs/DATA_CARD.md",
    "docs/DATA_ACCESS.md",
    "docs/LIMITATIONS.md",
    "docs/REPRODUCIBILITY.md",
    "docs/REPOSITORY_PATTERNS.md",
    "docs/reviewer-data-note.md",
    "results/aggregate_metrics.csv",
    "results/ablation_summary.csv",
    "results/figure_manifest.csv",
    "results/public_demo_features.csv",
    "scripts/run_public_smoke_test.py",
)

ALLOWED_PATHS = set(REQUIRED_FILES) | {
    ".gitignore",
    "configs/public_smoke_test.yml",
    "data/sample/README.md",
    "docs/RELEASE_CHECKLIST.md",
    "environment.yml",
    "figures/README.md",
    "pyproject.toml",
    "requirements.txt",
    "results/README.md",
    "results/public_smoke_summary.json",
    "scripts/__init__.py",
    "scripts/audit_public_release.py",
    "scripts/make_demo_sample.py",
    "src/svc_release/__init__.py",
    "src/svc_release/demo_data.py",
    "src/svc_release/features.py",
    "src/svc_release/metrics.py",
    "tests/test_demo_data.py",
    "tests/test_public_pipeline.py",
    "tests/test_release_audit.py",
}
ALLOWED_DIRECTORIES = {
    parent.as_posix()
    for relative in ALLOWED_PATHS
    for parent in Path(relative).parents
    if parent.as_posix() != "."
}

FORBIDDEN_BASENAMES = {
    "bsl.csv",
    "augmented_dataset.csv",
    "bang so lieu.xls",
    "real_time_svc_control.zip",
}
FORBIDDEN_EXTENSIONS = {".xlsx", ".xls", ".zip", ".docx", ".pdf", ".log", ".pkl", ".joblib", ".h5"}
FORBIDDEN_DIRECTORY_NAMES = {"raw", "private", "restricted"}
IGNORED_DIRECTORIES = {".git", ".pytest_cache", "__pycache__", ".superpowers"}
EXPECTED_PAPER_LAYERS = {
    "parent_operational_records",
    "augmented_records",
    "training_records",
    "evaluation_records",
}


def _iter_public_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRECTORIES for part in relative.parts):
            continue
        yield path, relative


def _git_history_paths(root: Path) -> list[str]:
    if not (root / ".git").is_dir():
        return []
    result = subprocess.run(
        ["git", "-C", str(root), "rev-list", "--objects", "--all"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    paths = []
    for line in result.stdout.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            paths.append(parts[1].replace("\\", "/"))
    return paths


def _is_path_forbidden(relative: str) -> bool:
    path = Path(relative)
    if relative in ALLOWED_DIRECTORIES:
        return False
    lower_name = path.name.lower()
    return (
        lower_name in FORBIDDEN_BASENAMES
        or path.suffix.lower() in FORBIDDEN_EXTENSIONS
        or any(part.lower() in FORBIDDEN_DIRECTORY_NAMES for part in path.parts[:-1])
        or relative not in ALLOWED_PATHS
    )


def _check_checksums(root: Path, violations: list[str]) -> None:
    manifest_path = root / "data/schema/checksums.sha256"
    if not manifest_path.is_file():
        return
    for line_number, raw_line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or len(parts[0]) != 64:
            violations.append(f"invalid checksum manifest line {line_number}")
            continue
        expected_hash, relative = parts
        target = root / relative
        if not target.is_file():
            violations.append(f"checksum target is missing: {relative}")
            continue
        actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            violations.append(f"checksum mismatch: {relative}")


def audit_public_release(root: Path) -> dict[str, Any]:
    """Return a machine-readable release audit report."""

    root = Path(root)
    missing = [relative for relative in REQUIRED_FILES if not (root / relative).is_file()]
    forbidden: list[str] = []
    for path, relative_path in _iter_public_files(root):
        relative = relative_path.as_posix()
        if _is_path_forbidden(relative):
            forbidden.append(relative)
    for history_path in _git_history_paths(root):
        if _is_path_forbidden(history_path):
            forbidden.append(history_path)

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

    cff_path = root / "CITATION.cff"
    if cff_path.is_file():
        try:
            cff = yaml.safe_load(cff_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            content_violations.append(f"CITATION.cff is invalid YAML: {exc}")
            cff = {}
        for key in ("cff-version", "title", "message", "authors", "repository-code", "license"):
            if not cff.get(key):
                content_violations.append(f"CITATION.cff is missing {key}")
        if not isinstance(cff.get("authors"), list) or not cff["authors"]:
            content_violations.append("CITATION.cff must contain at least one author")
        if cff.get("repository-code", "").startswith("<"):
            content_violations.append("CITATION.cff repository-code must be a visible URL or explicit placeholder URL")

    access_path = root / "docs/DATA_ACCESS.md"
    if access_path.is_file():
        access = access_path.read_text(encoding="utf-8").lower()
        for phrase in ("institutional_data_custodian_email", "not a working address", "not guaranteed"):
            if phrase not in access:
                content_violations.append(f"DATA_ACCESS.md must contain: {phrase}")

    sample_path = root / "data/sample/svc_demo_synthetic.csv"
    if sample_path.is_file():
        sample = pd.read_csv(sample_path)
        if set(sample.get("source_type", [])) != {"synthetic_demo"}:
            content_violations.append("public sample must contain only source_type=synthetic_demo")
        if len(sample) > 64:
            content_violations.append("public sample must remain small (64 rows or fewer)")
        if not sample.get("split_role", pd.Series(dtype=str)).eq("demo_only").all():
            content_violations.append("public sample must contain only split_role=demo_only")
        for column, low, high in (("Qt", 20.0, 100.0), ("Pt", 20.0, 100.0), ("Alpha_t", 2.1, 3.2)):
            if column not in sample or not pd.api.types.is_numeric_dtype(sample[column]) or not sample[column].between(low, high).all():
                content_violations.append(f"public sample violates the documented range for {column}")

    lineage_path = root / "data/schema/data_lineage.yml"
    if lineage_path.is_file():
        lineage = yaml.safe_load(lineage_path.read_text(encoding="utf-8")) or {}
        public_sample = lineage.get("public_sample", {})
        if public_sample.get("is_real_data_subset") is not False:
            content_violations.append("lineage must state that the public sample is not real data")
        if not public_sample.get("sha256"):
            content_violations.append("lineage must record the public sample SHA-256")
        layers = lineage.get("paper_data_layers")
        if set(layers or {}) != EXPECTED_PAPER_LAYERS:
            content_violations.append("lineage must list all four paper data layers")
        for layer_name in EXPECTED_PAPER_LAYERS:
            layer = (layers or {}).get(layer_name, {})
            if layer.get("public") is not False:
                content_violations.append(f"paper data layer must remain restricted: {layer_name}")
            if layer.get("status") != "pending_author_confirmation":
                content_violations.append(f"unconfirmed layer status must remain explicit: {layer_name}")
            if layer.get("count") is not None:
                content_violations.append(f"unconfirmed layer count must remain null: {layer_name}")

    for result_name in ("aggregate_metrics.csv", "ablation_summary.csv"):
        result_path = root / "results" / result_name
        if result_path.is_file():
            result = pd.read_csv(result_path)
            if set(result.get("status", [])) != {"author_confirmation_required"}:
                content_violations.append(f"{result_name} must keep author_confirmation_required status")
            if set(result.get("scope", [])) != {"internal_benchmark"}:
                content_violations.append(f"{result_name} must keep internal_benchmark scope")

    _check_checksums(root, content_violations)

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
