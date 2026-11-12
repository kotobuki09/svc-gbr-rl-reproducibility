import pandas as pd
import pytest

from svc_release.demo_data import generate_demo_frame, validate_demo_frame


EXPECTED_COLUMNS = [
    "record_id",
    "Qt",
    "Pt",
    "Alpha_t",
    "source_type",
    "split_role",
]


def test_demo_sample_is_deterministic():
    first = generate_demo_frame()
    second = generate_demo_frame()

    pd.testing.assert_frame_equal(first, second)


def test_demo_sample_has_public_schema():
    frame = generate_demo_frame()

    assert len(frame) == 48
    assert list(frame.columns) == EXPECTED_COLUMNS
    assert frame["record_id"].is_unique


def test_demo_sample_is_explicitly_synthetic():
    frame = generate_demo_frame()

    assert set(frame["source_type"]) == {"synthetic_demo"}
    assert set(frame["split_role"]) == {"demo_only"}


def test_demo_sample_has_no_source_identifiers():
    frame = generate_demo_frame()

    forbidden_fragments = ("station", "timestamp", "parent", "event")
    assert not any(
        any(fragment in column.lower() for fragment in forbidden_fragments)
        for column in frame.columns
    )
    assert frame["Qt"].between(20, 100).all()
    assert frame["Pt"].between(20, 100).all()
    assert frame["Alpha_t"].between(2.1, 3.2).all()


def test_validate_demo_frame_rejects_out_of_range_values():
    frame = generate_demo_frame(2)
    frame.loc[0, "Qt"] = 999999

    with pytest.raises(ValueError, match="Qt"):
        validate_demo_frame(frame)


def test_validate_demo_frame_rejects_missing_values():
    frame = generate_demo_frame(2)
    frame.loc[0, "Pt"] = float("nan")

    with pytest.raises(ValueError, match="missing"):
        validate_demo_frame(frame)
