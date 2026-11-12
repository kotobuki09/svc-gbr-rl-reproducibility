"""Deterministic synthetic data for the public repository smoke test.

The generator is intentionally independent of the private working directory.
It produces plausible schema-shaped values for demonstration only; it never
reads or samples the operational records.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


PUBLIC_COLUMNS = ("record_id", "Qt", "Pt", "Alpha_t", "source_type", "split_role")


def generate_demo_frame(n: int = 48, seed: int = 20261112) -> pd.DataFrame:
    """Return a deterministic, synthetic SVC-like demonstration frame."""

    if n <= 0:
        raise ValueError("n must be positive")

    rng = np.random.default_rng(seed)
    qt = rng.uniform(25.0, 95.0, size=n)
    pt = rng.uniform(25.0, 95.0, size=n)
    qt_norm = (qt - 25.0) / 70.0
    pt_norm = (pt - 25.0) / 70.0
    noise = rng.normal(loc=0.0, scale=0.012, size=n)
    alpha = np.clip(2.22 + 0.55 * qt_norm + 0.30 * pt_norm + noise, 2.1, 3.2)

    return pd.DataFrame(
        {
            "record_id": [f"demo-{index:04d}" for index in range(1, n + 1)],
            "Qt": np.round(qt, 3),
            "Pt": np.round(pt, 3),
            "Alpha_t": np.round(alpha, 6),
            "source_type": "synthetic_demo",
            "split_role": "demo_only",
        }
    )


def validate_demo_frame(frame: pd.DataFrame) -> None:
    """Raise ``ValueError`` when a frame violates the public demo contract."""

    missing_columns = [column for column in PUBLIC_COLUMNS if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"missing required columns: {', '.join(missing_columns)}")
    if frame.loc[:, PUBLIC_COLUMNS].isna().any().any():
        raise ValueError("missing values are not allowed in the public demo sample")
    for column in ("Qt", "Pt", "Alpha_t"):
        if not pd.api.types.is_numeric_dtype(frame[column]):
            raise ValueError(f"{column} must be numeric")
    if not frame["record_id"].is_unique or not frame["record_id"].astype(str).str.fullmatch(r"demo-\d{4}").all():
        raise ValueError("record_id must contain unique demo-#### identifiers")
    if not frame["source_type"].eq("synthetic_demo").all():
        raise ValueError("source_type must be synthetic_demo")
    if not frame["split_role"].eq("demo_only").all():
        raise ValueError("split_role must be demo_only")
    if not frame["Qt"].between(20.0, 100.0).all():
        raise ValueError("Qt is outside the documented demo range")
    if not frame["Pt"].between(20.0, 100.0).all():
        raise ValueError("Pt is outside the documented demo range")
    if not frame["Alpha_t"].between(2.1, 3.2).all():
        raise ValueError("Alpha_t is outside the documented demo range")
