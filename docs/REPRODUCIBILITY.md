# Reproducibility guide

## Level 1 — public smoke test

This level runs from the committed synthetic demo sample and verifies:

- required columns and types;
- synthetic provenance labels;
- feature-engineering output;
- deterministic summary metadata;
- public release boundaries.

Run:

```bash
python scripts/run_public_smoke_test.py
pytest -q
```

## Level 2 — public artifact review

Aggregate tables and the figure manifest can be inspected without access to
row-level operational records. Each artifact must identify its provenance and
whether it is authoritative or pending author confirmation.

## Level 3 — restricted-data reproduction

Full paper reproduction requires controlled access to the complete data and an
authoritative experiment manifest. Request access using
[`DATA_ACCESS.md`](DATA_ACCESS.md). A grant of access does not change the
internal-benchmark limitation.

## Environment

The supported public environment is Python 3.10 or newer. Install the pinned
major-version ranges from `requirements.txt` or `environment.yml`.
