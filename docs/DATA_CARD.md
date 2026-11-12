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

The following release fields remain pending because the authoritative run and
data custodian have not yet been confirmed:

- data custodian and institutional access channel;
- exact augmentation and preprocessing parameters for the authoritative run;
- exclusions and missing-value handling for the authoritative run; and
- the row-level parent-to-derived mapping.

The current evidence establishes the high-level relationship: augmented
training samples and evaluation records share parent SCADA records. The full
mapping is restricted and is not reconstructed from the public demo.

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

## Public transformation note

`Qt_Pt_ratio` uses the same small denominator epsilon as the local experiment
scripts. The public feature path remains a demo-only transformation until the
authoritative paper run is selected; it is not a claim that the private
pipeline is fully reproduced here.

## Versioning

The lineage and checksum fields are maintained in
[`data_lineage.yml`](../data/schema/data_lineage.yml) and the SHA-256 manifest
in [`checksums.sha256`](../data/schema/checksums.sha256). A tagged release must
freeze the sample, schema, code version, and public data/artifact checksums.
