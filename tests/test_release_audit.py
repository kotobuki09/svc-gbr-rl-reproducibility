import shutil
from pathlib import Path

import pandas as pd
import yaml

from scripts.audit_public_release import audit_public_release


ROOT = Path(__file__).resolve().parents[1]


def test_release_audit_accepts_current_public_tree():
    report = audit_public_release(ROOT)

    assert report["required_files_missing"] == []
    assert report["forbidden_paths"] == []
    assert report["content_violations"] == []


def test_release_audit_rejects_forbidden_augmented_file(tmp_path):
    copy_root = tmp_path / "release"
    shutil.copytree(
        ROOT,
        copy_root,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__", ".superpowers"),
    )
    (copy_root / "augmented_dataset.csv").write_text("private\n", encoding="utf-8")

    report = audit_public_release(copy_root)

    assert "augmented_dataset.csv" in report["forbidden_paths"]


def _copy_release(tmp_path):
    copy_root = tmp_path / "release"
    shutil.copytree(
        ROOT,
        copy_root,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__", ".superpowers"),
    )
    return copy_root


def test_release_audit_rejects_unallowlisted_evaluation_rows(tmp_path):
    copy_root = _copy_release(tmp_path)
    (copy_root / "results" / "evaluation_records.csv").write_text("Qt,Pt\n1,2\n", encoding="utf-8")

    report = audit_public_release(copy_root)

    assert "results/evaluation_records.csv" in report["forbidden_paths"]


def test_release_audit_rejects_empty_required_metadata(tmp_path):
    copy_root = _copy_release(tmp_path)
    (copy_root / "CITATION.cff").write_text("", encoding="utf-8")

    report = audit_public_release(copy_root)

    assert any("CITATION.cff" in item for item in report["content_violations"])


def test_release_audit_rejects_authoritative_snapshot_status(tmp_path):
    copy_root = _copy_release(tmp_path)
    path = copy_root / "results" / "aggregate_metrics.csv"
    frame = pd.read_csv(path)
    frame["status"] = "authoritative"
    frame.to_csv(path, index=False, lineterminator="\n")

    report = audit_public_release(copy_root)

    assert any("author_confirmation_required" in item for item in report["content_violations"])


def test_release_audit_rejects_missing_lineage_layers(tmp_path):
    copy_root = _copy_release(tmp_path)
    path = copy_root / "data" / "schema" / "data_lineage.yml"
    lineage = yaml.safe_load(path.read_text(encoding="utf-8"))
    lineage["paper_data_layers"] = {}
    path.write_text(yaml.safe_dump(lineage, sort_keys=False), encoding="utf-8")

    report = audit_public_release(copy_root)

    assert any("paper data layers" in item for item in report["content_violations"])
