# SVC control research repository

Public reproducibility companion for **Gradient Boosting for Real-Time SVC
Control: Superior Accuracy, SHAP Interpretability, and Edge Deployability over
Deep RL**.

[![Code: MIT](https://img.shields.io/badge/code-MIT-0b7285.svg)](LICENSE-CODE)
[![Demo data: CC BY 4.0](https://img.shields.io/badge/demo%20data-CC%20BY%204.0-f59f00.svg)](LICENSE-DATA)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](environment.yml)
[![Public smoke test](https://img.shields.io/badge/smoke%20test-public-2f9e44.svg)](docs/REPRODUCIBILITY.md)
[![Archive](https://img.shields.io/badge/archive-DOI%20pending-6c757d.svg)](CITATION.cff)

> **Scope note — read first.** The reported results are an **internal
> benchmark**. Training and evaluation records share parent SCADA records, so
> this release does **not** establish independent out-of-sample generalization.

## At a glance

| Item | Release status |
|---|---|
| Research question | Can gradient-boosted regression support interpretable SVC firing-angle prediction under the study protocol? |
| Public data | A small synthetic demonstration sample with the documented schema |
| Full operational records | Restricted; available only through a reviewed request |
| Public code path | Feature engineering, schema checks, provenance checks, and smoke test |
| Paper artifacts | Curated aggregate summaries and figure manifest; authoritative counts pending author confirmation |
| Archive | Zenodo DOI to be assigned after the public release is reviewed |

## What is public and what is restricted?

### Public

- Synthetic demonstration data in [`data/sample/`](data/sample/)
- Data dictionary and lineage statement in [`data/schema/`](data/schema/)
- Public feature and metrics code in [`src/svc_release/`](src/svc_release/)
- Reproducibility and limitation notes in [`docs/`](docs/)
- Repository design rationale in [`docs/REPOSITORY_PATTERNS.md`](docs/REPOSITORY_PATTERNS.md)
- Curated aggregate artifacts in [`results/`](results/)

### Restricted

The complete parent SCADA records, full augmented records, full evaluation
records, operational spreadsheets, and any row-level derivatives remain outside
this repository. See [`docs/DATA_ACCESS.md`](docs/DATA_ACCESS.md) for the
request process. Access is not automatic and is subject to the data
custodian's review.

## Run the public smoke test

The public path uses only the synthetic sample. It does not read a private
file, reproduce the paper's restricted-data metrics, or imply that the sample
is a real-data subset.

```bash
python -m pip install -r requirements.txt
python scripts/run_public_smoke_test.py \
  --output results/public_smoke_summary.json \
  --features-output results/public_demo_features.csv
python scripts/audit_public_release.py
pytest -q
```

## Repository map

```text
data/sample/       synthetic demonstration data only
data/schema/       field definitions and data lineage
src/svc_release/   public feature and summary functions
scripts/           smoke test, sample generation, and release audit
configs/           public execution settings
results/           curated aggregate artifacts, not row-level records
figures/           figure manifest and release notes
docs/              data card, limitations, access policy, and reproduction guide
tests/             public-boundary and deterministic behavior tests
```

## Interpretation guardrails

- The evaluation protocol is an internal benchmark because training and
  evaluation records share parent SCADA records.
- The synthetic sample demonstrates schema and code behavior. It is not a
  statistical substitute for the restricted records.
- Edge-deployment statements in the paper are simulation results unless a
  separately documented physical deployment is released.
- Counts for parent, augmented, training, and evaluation records are pending
  author confirmation in [`data_lineage.yml`](data/schema/data_lineage.yml).

## Reproducibility levels

1. **Public smoke test:** schema, provenance, feature engineering, and
   deterministic output shape run from the synthetic sample.
2. **Public demo artifact regeneration:** the synthetic feature artifact and
   smoke summary can be rebuilt without row-level operational data; aggregate
   paper tables remain inspection-only snapshots until confirmed.
3. **Restricted-data reproduction:** a qualified researcher may request the
   full data under the conditions in [`docs/DATA_ACCESS.md`](docs/DATA_ACCESS.md).

Details are in [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).

## Results map

| Paper-facing artifact | Public release location | Status |
|---|---|---|
| Model and RL aggregate metrics | [`results/aggregate_metrics.csv`](results/aggregate_metrics.csv) | Snapshot values; author confirmation required |
| Feature ablation summary | [`results/ablation_summary.csv`](results/ablation_summary.csv) | Snapshot values; author confirmation required |
| Figure/source mapping | [`results/figure_manifest.csv`](results/figure_manifest.csv) | Manifest only; figures not bundled yet |
| Public schema and feature path | [`data/schema/`](data/schema/) and [`src/svc_release/`](src/svc_release/) | Public smoke-test path |

The status labels are intentional. The current working directory contains
conflicting result snapshots, so the repository does not silently promote one
snapshot to the authoritative paper result.

## Citation

Please cite this repository and the associated paper. The machine-readable
metadata are in [`CITATION.cff`](CITATION.cff). The Zenodo DOI will be added to
the tagged release and this file after archival publication.

## Contact for the complete data

Use the request template in [`docs/DATA_ACCESS.md`](docs/DATA_ACCESS.md). The
institutional contact is intentionally a placeholder until the authors select
the approved data custodian and channel.

## License

Code is released under the MIT License. The synthetic demonstration data and
its documentation are released under CC BY 4.0. These licenses do not grant
access to restricted operational data.
