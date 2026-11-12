"""Public feature engineering for the documented demonstration schema."""

from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = ("record_id", "Qt", "Pt", "Alpha_t", "source_type", "split_role")
FEATURE_COLUMNS = (
    "Qt_sq",
    "Pt_sq",
    "Qt_Pt_interaction",
    "Qt_Pt_ratio",
    "Total_power",
)


def engineer_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with deterministic, documented derived features."""

    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")

    result = frame.copy(deep=True)
    result["Qt_sq"] = result["Qt"] ** 2
    result["Pt_sq"] = result["Pt"] ** 2
    result["Qt_Pt_interaction"] = result["Qt"] * result["Pt"]
    result["Qt_Pt_ratio"] = result["Qt"] / (result["Pt"] + 1e-12)
    result["Total_power"] = np.sqrt(result["Qt"] ** 2 + result["Pt"] ** 2)
    return result
