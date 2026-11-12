"""Deterministic synthetic data for the public repository smoke test.

The generator is intentionally independent of the private working directory.
It produces plausible schema-shaped values for demonstration only; it never
reads or samples the operational records.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


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
