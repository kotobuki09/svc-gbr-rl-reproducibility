"""Release-safe metadata summaries for the public demonstration sample."""

from __future__ import annotations

import hashlib
from typing import Any

import pandas as pd

from .features import REQUIRED_COLUMNS


def _canonical_csv_bytes(frame: pd.DataFrame) -> bytes:
    return frame.loc[:, REQUIRED_COLUMNS].to_csv(index=False, lineterminator="\n").encode("utf-8")


def summarize_demo(frame: pd.DataFrame) -> dict[str, Any]:
    """Return deterministic metadata and checksum for a synthetic demo frame."""

    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")
    source_types = sorted(frame["source_type"].dropna().unique().tolist())
    if source_types != ["synthetic_demo"]:
        raise ValueError("public summaries require source_type=synthetic_demo")
    if set(frame["split_role"]) != {"demo_only"}:
        raise ValueError("public summaries require split_role=demo_only")

    checksum = hashlib.sha256(_canonical_csv_bytes(frame)).hexdigest()
    return {
        "schema_version": "0.1",
        "row_count": int(len(frame)),
        "input_columns": list(REQUIRED_COLUMNS),
        "source_types": source_types,
        "evaluation_scope": "internal_benchmark",
        "independent_out_of_sample_generalization_established": False,
        "data_checksum_sha256": checksum,
    }
