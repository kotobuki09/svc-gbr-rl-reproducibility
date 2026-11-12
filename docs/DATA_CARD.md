# Data card

## Summary

This release contains a small synthetic demonstration sample for the SVC
firing-angle prediction workflow. It exists to document the public schema and
to exercise the public smoke test. It is not a redacted or randomly selected
subset of operational SCADA records.

## Data status

| Layer | Status | Notes |
|---|---|---|
| Synthetic demo sample | Public | Generated deterministically from a documented formula |
| Parent operational records | Restricted | Exact count pending author confirmation |
| Augmented records | Restricted | Derived from parent records; exact count pending author confirmation |
| Training/evaluation records | Restricted | Shared-parent relationship must remain explicit |

## Schema

See [`data_dictionary.csv`](../data/schema/data_dictionary.csv). Values use
engineering-style names from the paper, but the public values are synthetic.

## Provenance

Every demo row carries `source_type=synthetic_demo`. The demo has no station
identifier, timestamp, parent-record identifier, or operational event ID.

## Intended use

- Test the public feature-engineering code.
- Learn the column names, units, and roles.
- Verify the repository's public smoke test.

## Prohibited interpretation

Do not use the demo rows to estimate the paper's reported performance. Do not
describe them as real measurements, anonymized real measurements, or an
independent test set.

## Missing values and exclusions

The demo generator emits complete rows. Missing-value policy for the restricted
records is documented here only after the authors confirm the authoritative
analysis run.

## Versioning

The lineage and checksum fields are maintained in
[`data_lineage.yml`](../data/schema/data_lineage.yml). A tagged release must
freeze the sample, schema, code version, and aggregate artifact manifest.
