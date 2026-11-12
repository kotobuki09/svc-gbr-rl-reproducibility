# Release checklist

## Data and governance

- [ ] Authoritative parent/augmented/training/evaluation counts confirmed.
- [ ] Public sample confirmed synthetic-only or formally approved otherwise.
- [ ] Disclosure/data-governance review completed.
- [ ] Restricted data absent from Git history and release archive.
- [ ] Institutional data custodian and request channel confirmed.

## Scientific consistency

- [ ] Internal-benchmark limitation appears in README and manuscript.
- [ ] No claim of independent unseen-SCADA generalization remains unsupported.
- [ ] Authoritative code/run/result artifacts selected.
- [ ] Aggregate result tables reconciled with the selected run.

## Archive metadata

- [ ] Author names, affiliations, ORCIDs, and citation metadata confirmed.
- [ ] Code and demo-data licenses confirmed.
- [ ] GitHub URL added.
- [ ] Zenodo DOI added to README and manuscript.
- [ ] Release tag and checksum manifest frozen.

## Verification evidence

- [ ] `pytest -q`
- [ ] `python scripts/run_public_smoke_test.py`
- [ ] `python scripts/audit_public_release.py`
- [ ] Rendered README inspected on the hosting platform.
