import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

from svc_release.demo_data import generate_demo_frame
from svc_release.features import engineer_features
from svc_release.metrics import summarize_demo


def test_engineer_features_adds_documented_columns_without_mutating_input():
    source = generate_demo_frame(4)
    original = source.copy(deep=True)

    featured = engineer_features(source)

    assert list(source.columns) == list(original.columns)
    pd.testing.assert_frame_equal(source, original)
    assert {"Qt_sq", "Pt_sq", "Qt_Pt_interaction", "Qt_Pt_ratio", "Total_power"}.issubset(
        featured.columns
    )
    assert featured["Qt_Pt_interaction"].iloc[0] == featured["Qt"].iloc[0] * featured["Pt"].iloc[0]
    assert featured["Qt_Pt_ratio"].iloc[0] == pytest.approx(
        featured["Qt"].iloc[0] / (featured["Pt"].iloc[0] + 1e-6)
    )


def test_summarize_demo_returns_stable_public_metadata():
    frame = generate_demo_frame()

    summary = summarize_demo(frame)

    assert summary["schema_version"] == "0.1"
    assert summary["row_count"] == 48
    assert summary["source_types"] == ["synthetic_demo"]
    assert summary["evaluation_scope"] == "internal_benchmark"
    assert len(summary["canonical_csv_checksum_sha256"]) == hashlib.sha256().digest_size * 2


def test_summarize_demo_rejects_non_synthetic_rows():
    frame = generate_demo_frame(2)
    frame.loc[0, "source_type"] = "operational"

    try:
        summarize_demo(frame)
    except ValueError as exc:
        assert "synthetic_demo" in str(exc)
    else:
        raise AssertionError("summarize_demo must reject non-synthetic rows")


def test_public_smoke_script_writes_scope_safe_summary(tmp_path):
    root = Path(__file__).resolve().parents[1]
    output = tmp_path / "summary.json"

    completed = subprocess.run(
        [sys.executable, "scripts/run_public_smoke_test.py", "--output", str(output)],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    summary = json.loads(output.read_text(encoding="utf-8"))
    assert summary["evaluation_scope"] == "internal_benchmark"
    assert summary["source_types"] == ["synthetic_demo"]
    assert len(summary["file_checksum_sha256"]) == hashlib.sha256().digest_size * 2


def test_public_smoke_script_rebuilds_feature_artifact(tmp_path):
    root = Path(__file__).resolve().parents[1]
    output = tmp_path / "summary.json"
    features_output = tmp_path / "public_demo_features.csv"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_public_smoke_test.py",
            "--output",
            str(output),
            "--features-output",
            str(features_output),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    rebuilt = pd.read_csv(features_output)
    assert len(rebuilt) == 48
    assert "Qt_Pt_interaction" in rebuilt.columns
