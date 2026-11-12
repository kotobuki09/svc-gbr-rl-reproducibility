import shutil
from pathlib import Path

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
